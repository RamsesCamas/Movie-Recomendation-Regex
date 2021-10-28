import requests
import regex

"""
TODO: Implementar app de Flask
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

def show_5_movies(title_matches,rating_matches,poster_matches):
    print('Peliculas recomendadas:\n')
    for i in range(5):
        movie_match = title_matches[i]
        movie_title = regex.search(REGEX_TITLE,movie_match).group(0)
        movie_year = regex.search(REGEX_YEAR,movie_match).group(0)
        movie_director = regex.search(REGEX_MOVIE_DIRECTOR,movie_match).group(0)
        movie_main_cast = regex.search(REGEX_MOVIE_MAIN_CAST,movie_match).group(0)
        movie_rating = rating_matches[i]
        movie_poster = poster_matches[i]
        print(f'{movie_title} - Año: {movie_year}\nDirector: {movie_director} - '+
        f'Cast: {movie_main_cast}\nPuntuación: {movie_rating}')
        print(movie_poster)

def show_5_tv_shows(title_matches,rating_matches,poster_matches):
    print('Series de TV recomendadas:\n')
    for i in range(5):
        show_match = title_matches[i]
        show_title = regex.search(REGEX_TITLE,show_match).group(0)
        show_year = regex.search(REGEX_YEAR,show_match).group(0)
        show_rating = rating_matches[i]
        show_poster = poster_matches[i]
        print(f'{show_title} - Año {show_year} - Puntuación {show_rating}')
        print(show_poster)

if __name__ == '__main__':
    recommendation = input('Peliculas (P) o Series de TV (S): ')
    if recommendation == 'P':
        response = requests.get(URL_MOVIES)
    elif recommendation == 'S':
        response = requests.get(URL_TV_SHOWS)
    if response.status_code == 200:
        title_matches = regex.findall(REGEX_ALL_TITLE,response.text)
        rating_matches = regex.findall(REGEX_RATING,response.text)
        poster_matches = regex.findall(REGEX_POSTER,response.text)
        if recommendation == 'P':
            show_5_movies(title_matches,rating_matches,poster_matches)
        elif recommendation == 'S':
            show_5_tv_shows(title_matches,rating_matches,poster_matches)