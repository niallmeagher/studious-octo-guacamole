import re
from typing import Optional, List

class QueryParser:
    '''Converts natural language questions into SQL queries'''
    def __init__(self) -> None:
        self.genres = ['Action', 'Adventure', 'Animation', 'Comedy',
                        'Crime', 'Documentary', 'Drama', 'Family',
                        'Fantasy', 'Foreign', 'History', 'Horror',
                        'Music', 'Mystery', 'Romance', 'Science Fiction',
                        'TV Movie', 'Thriller', 'War', 'Western']
        
        # Common movie-related questions: recommend, info, filter
        self.intent = { # Regex expressions taken from Claude
            # e.g. 'Recommend action movies from 2020'
            'recommend': [
                r'\b(recommend|suggest|find|show)\s+(me\s+)?(?P<genre>\w+)?\s*movies?',
                r'what\s+(?:should|can)\s+i\s+watch',
                r'looking\s+for\s+(?P<genre>\w+)?\s*(?:movies?|films?)'
                ],

            # e.g. 'Tell me about Inception'
            'info': [
                r'tell\s+me\s+about\s+(?P<title>.+)',
                r'what\s+is\s+(?P<title>.+)\s+about',
                r'(?:plot|synopsis|summary)\s+of\s+(?P<title>.+)'
                ],

            # e.g. 'What was the worst horror movie from 1995?'
            'filter': [ 
                r'(?:find|search)\s+(?:for\s+)?(?:the\s+)?movie\s+(?P<title>.+)',
                r'have\s+you\s+heard\s+of\s+(?P<title>.+)'
                ],
        }

    def parse_query(self, query: str):
        # Clean query text
        query = query.lower().strip()

        # Identify intent
        query_intent = None
        for intent, patterns in self.intent.items():
            for pattern in patterns:
                match = re.search(pattern, query)
                if match:
                    query_intent = intent
                    break
        
        # Find keywords (genre, year, attributes)
        genre = self._extract_genre(query)
        year = self._extract_year(query)
        movie_title = None
        if 'title' in match.groupdict():
            movie_title = match.group('title').strip()

        parsed_query = f'SELECT * FROM movies'

        query_filters = ''
        if any([genre, year, movie_title]):
            query_filters += f'\n WHERE '
        
        filter_list = []
        if genre:
            filter_list.append(f'genres CONTAINS {genre}')
        if year:
            filter_list.append(f'year == {year}')
        if movie_title:
            filter_list.append(f'title CONTAINS {movie_title}')

        filters = ' AND '.join(filter_list)

        query_filters += filters
        parsed_query += query_filters

        return {
            'raw': query,
            'parsed': parsed_query
        }



    # Extraction methods provided by Claude
    def _extract_genre(self, query: str) -> Optional[str]:
        """Extract genre from query (can currently only handle 1 genre)"""
        for genre in self.genres:
            if genre in query:
                return genre.title()
        return None
    
    def _extract_year(self, query: str) -> Optional[int]:
        """Extract year from query"""
        year_match = re.search(r'\b(19|20)\d{2}\b', query)
        return int(year_match.group()) if year_match else None
    
    # def _extract_attributes(self, query: str) -> List[str]:
    #     """Extract quality attributes"""
    #     attributes = []
    #     if any(kw in query for kw in ['highest rated', 'best', 'top rated']):
    #         attributes.append('highly_rated')
    #     if any(kw in query for kw in ['popular', 'famous', 'trending']):
    #         attributes.append('popular')
    #     if any(kw in query for kw in ['recent', 'new', 'latest']):
    #         attributes.append('recent')
    #     return attributes
