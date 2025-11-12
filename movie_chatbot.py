from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed
from system_prompt import system_prompt
from query_parser import QueryParser
import sqlite3

class MovieChatbot():
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained('gpt2')
        self.model = AutoModelForCausalLM.from_pretrained('gpt2')
        self.parser = QueryParser()

    def __call__(self, prompt, max_tokens=100, temperature=0.7, top_k=0, top_p=1.0):
        # Parse query
        query = self.parser.parse_query(prompt)
        raw_query = query['raw']
        intent = query['intent']
        parsed_query = query['parsed']

        # Break query into intent, raw, and parsed
        user_prompt = f'<user_prompt>{raw_query}</user_prompt>'
        intent_prompt = f'<intent>{intent}</intent>'

        # Fetch parsed query from db
        database = self.query_database(parsed_query)
        db_prompt = f'<database>'
        for row in database:
            db_prompt += f'{row}\n'
        db_prompt += f'</database>'

        # Stitch it all into the system prompt
        input = ' '.join([system_prompt, user_prompt, intent_prompt, db_prompt])

        # provide an answer
        encoded_input = self.tokenizer(input, return_tensors='pt')

        output = self.model.generate(
            **encoded_input, 
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)[len(input):]

    def query_database(self, query):
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()
        for row in rows:
            print(row)
        return rows

