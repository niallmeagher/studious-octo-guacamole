from datasets import load_dataset
import sqlite3
import json
from tqdm import tqdm

''' References: https://huggingface.co/posts/aifeifei798/740101266283155
                https://huggingface.co/datasets/AiresPucrs/tmdb-5000-movies
'''

def get_cast_names(cast_field):
    """Extracts cast names from JSON field in TMDB dataset

    Args:
        cast_field (str): 'cast' attribute from tmdb dataset

    Returns:
        list[str]: list of names of cast members
    """
    data = json.loads(cast_field)
    cast_names = [person.get('name') for person in data if 'name' in person]

    return str(cast_names)

def get_director_names(crew_field):
    """Extracts director names from JSON field in TMDB dataset

    Args:
        crew_field (str): 'crew' attribute from tmdb dataset

    Returns:
        list[str]: list of names of directors
    """

    data = json.loads(crew_field)
    director_names = [person.get('name') for person in data if 'name' in person and person.get('job')=='Director']

    return str(director_names)

def get_genres(genres_field):
    """Extracts genre names from JSON field in TMDB dataset

    Args:
        genre_field (str): 'genres' attribute from tmdb dataset

    Returns:
        list[str]: list of names of genres
    """

    data = json.loads(genres_field)
    genre_names = [genre.get('name') for genre in data if 'name' in genre]

    return genre_names

if __name__ == '__main__':
    # Load dataset
    ds = load_dataset("AiresPucrs/tmdb-5000-movies", split='train')

    # Create SQL database
    try:
        conn = sqlite3.connect('movies.db')
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

    # Create table if not exists
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                    (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, genres TEXT, overview TEXT, rating FLOAT, cast TEXT, directors TEXT)
                ''')


    # # Add the relevant data from dataset into db
    for i, row in tqdm(enumerate(ds)):
        cast_names = get_cast_names(row['cast'])
        director_names = get_director_names(row['crew'])
        genre_names = str(get_genres(row['genres']))

        # Slice the year field from the release date
        release_date = row['release_date'] if 'release_date' in row else None
        year = release_date[:4] if release_date and len(str(release_date)) >= 4 else None


        cursor.execute("INSERT INTO movies (id, title, year, genres, overview, rating, cast, directors) VALUES (?,?,?,?,?,?,?,?)",
                       (i, row['title'], year, genre_names, row['overview'], row['vote_average'], cast_names, director_names))
        
    # Commit transaction, verify with sample query, and close connection
    conn.commit()
    cursor.execute("SELECT * FROM movies LIMIT 5")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


