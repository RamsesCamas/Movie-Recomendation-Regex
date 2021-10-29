import requests
import regex
from random import randint

"""
TODO: Implementar UI en Tkiner
"""

URL_MOVIES = 'https://www.imdb.com/chart/top/'
URL_TV_SHOWS = 'https://www.imdb.com/chart/toptv/'


REGEX_ALL_TITLE = r'<td class="titleColumn">[\s\n]*.*[\s\n]*<a href=".*"[\s\n]title=".*"\s*>.*</a>[\s\n]*<span class="secondaryInfo">.*</span>[\s\n]*</td>'

REGEX_TITLE = r'(?<=<td class="titleColumn">[\s\n]*[0-9]{1,3}\.[\s\n]*<a href="[\w/]+"\ntitle="[\w\u00C0-\u017F\s\\,\(\.\)]+"\s*>)(.*)(?=</a>)'

REGEX_YEAR = r'(?<=<span class="secondaryInfo">)(.*)(?=</span>)'

REGEX_MOVIE_DIRECTOR = r'(?<=<a href=".*"[\s\n]*title=")(.*)(?=\s\(dir\.\))'

REGEX_MOVIE_MAIN_CAST = r'(?<=\(dir\.\),\s).*(?=")'

REGEX_RATING = r'(?<=<td class="ratingColumn imdbRating">[\s\n]*<strong title=".*">)(.*)(?=</strong>)'

REGEX_POSTER = r'(?<=<td class="posterColumn">[\s\n]*<span name="rk" data-value=".*"></span>[\s\n]*<span name="ir" data-value=".*"></span>[\s\n]*<span name="us" data-value=".*"></span>[\s\n]*<span name="nv" data-value=".*"></span>[\s\n]*<span name="ur" data-value=".*"></span>[\s\n]<a href=".*"[\s\n]*>\s<img src=")(.*)(?=" width=".*" height=".*" alt=".*"/>[\s\n]*</a>[\s]*</td>)'

def show_movie(title_matches,rating_matches,poster_matches):
    num_movie = randint(0,len(title_matches)-1)
    movie_match = title_matches[num_movie]
    movie_title = regex.search(REGEX_TITLE,movie_match).group(0)
    movie_year = regex.search(REGEX_YEAR,movie_match).group(0)
    try:
        movie_director = regex.search(REGEX_MOVIE_DIRECTOR,movie_match).group(0)
        movie_director = f'\nDirector: {movie_director}'
        movie_main_cast = regex.search(REGEX_MOVIE_MAIN_CAST,movie_match).group(0)
        movie_main_cast = f'Cast: {movie_main_cast}\n'
    except:
        movie_director = ''
        movie_main_cast = ''
    movie_rating = rating_matches[num_movie]
    movie_poster = poster_matches[num_movie]
    print(f'{movie_title} - Año: {movie_year} - {movie_director}'+
    f'{movie_main_cast}Puntuación: {movie_rating}')
    print(movie_poster)

if __name__ == '__main__':
    recommendation = input('Peliculas (P) o Series de TV (S): ')
    if recommendation == 'P':
        response = requests.get(URL_MOVIES)
        print('Peliculas recomendadas:\n')
    elif recommendation == 'S':
        response = requests.get(URL_TV_SHOWS)
        print('Series de TV recomendadas:\n')
    if response.status_code == 200:
        title_matches = regex.findall(REGEX_ALL_TITLE,response.text)
        rating_matches = regex.findall(REGEX_RATING,response.text)
        poster_matches = regex.findall(REGEX_POSTER,response.text)
        show_movie(title_matches,rating_matches,poster_matches)