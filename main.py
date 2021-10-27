import requests
import re
import regex

URL_MOVIES = 'https://www.imdb.com/chart/top/'
URL_TV_SHOWS = 'https://www.imdb.com/chart/toptv/'


REGEX_ALL_TITLE = r'<td class="titleColumn">[\s\n]*.*[\s\n]*<a href=".*"[\s\n]title=".*"\s*>.*</a>[\s\n]*<span class="secondaryInfo">.*</span>[\s\n]*</td>'

REGEX_TITLE = r'(?<=<td class="titleColumn">[\s\n]*[0-9]{1,3}\.[\s\n]*<a href="[\w/]+"\ntitle="[\w\u00C0-\u017F\s\\,\(\.\)]+"\s*>)(.*)(?=</a>)'

REGEX_YEAR = r'(?<=<span class="secondaryInfo">)(.*)(?=</span>)'

REGEX_MOVIE_DIRECTOR = r'(?<=<a href=".*"[\s\n]*title=")(.*)(?=\s\(dir\.\))'

REGEX_MOVIE_MAIN_CAST = r'(?<=\(dir\.\),\s).*(?=")'

def show_5_movies():
    print('Peliculas recomendadas:\n')
    for i in range(5):
        movie_match = title_matches[i]
        movie_title = regex.search(REGEX_TITLE,movie_match).group(0)
        movie_year = regex.search(REGEX_YEAR,movie_match).group(0)
        movie_director = regex.search(REGEX_MOVIE_DIRECTOR,movie_match).group(0)
        movie_main_cast = regex.search(REGEX_MOVIE_MAIN_CAST,movie_match).group(0)
        print(f'{movie_title} - Año: {movie_year}\nDirector: {movie_director} - '+
        f'Cast: {movie_main_cast}')
def show_5_tv_shows():
    print('Series de TV recomendadas:\n')
    for i in range(5):
        show_match = title_matches[i]
        show_title = regex.search(REGEX_TITLE,show_match).group(0)
        show_year = regex.search(REGEX_YEAR,show_match).group(0)
        print(f'{show_title} - Año {show_year}')


if __name__ == '__main__':
    response = requests.get(URL_TV_SHOWS)
    if response.status_code == 200:
        titles = []
        title_matches = regex.findall(REGEX_ALL_TITLE,response.text)
        for title in title_matches:
            titles.append(title)
        print(len(titles))
        
        show_5_tv_shows()
        