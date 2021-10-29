import requests
import regex
from random import randint
import urllib.request
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, font
from functools import partial
import os


URL_MOVIES = 'https://www.imdb.com/chart/top/'
URL_TV_SHOWS = 'https://www.imdb.com/chart/toptv/'


REGEX_ALL_TITLE = r'<td class="titleColumn">[\s\n]*.*[\s\n]*<a href=".*"[\s\n]title=".*"\s*>.*</a>[\s\n]*<span class="secondaryInfo">.*</span>[\s\n]*</td>'

REGEX_TITLE = r'(?<=<td class="titleColumn">[\s\n]*[0-9]{1,3}\.[\s\n]*<a href="[\w/]+"\ntitle="[\w\u00C0-\u017F\s\\,\(\.\)\-]+"\s*>)(.*)(?=</a>)'

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
        movie_director = f'Director: {movie_director}'
        movie_main_cast = regex.search(REGEX_MOVIE_MAIN_CAST,movie_match).group(0)
        movie_main_cast = f'Cast: {movie_main_cast}'
    except:
        movie_director = ''
        movie_main_cast = ''
    movie_rating = rating_matches[num_movie]
    movie_poster = poster_matches[num_movie]
    label_title_year['text'] = movie_title + '\n' + 'Año: ' + movie_year
    label_extra_info['text'] = movie_director + '\n' + movie_main_cast
    label_rating['text'] = f'Puntuación: {movie_rating}'

    urllib.request.urlretrieve(movie_poster,"poster.jpg")
    image_movie = Image.open('poster.jpg')
    image_movie = image_movie.resize((300,500))
    new_image = ImageTk.PhotoImage(image_movie)
    label_image = Label(root,image=new_image)
    label_image.image = new_image
    label_image.place(x=900,y=100)
    os.remove('poster.jpg')

def main(choice):
    if choice == 'P':
        response = requests.get(URL_MOVIES)
        label1['text'] = 'Pelicula recomendada:'
    elif choice == 'TV':
        response = requests.get(URL_TV_SHOWS)
        label1['text'] = 'Serie de TV recomendada:'
    if response.status_code == 200:
        title_matches = regex.findall(REGEX_ALL_TITLE,response.text)
        rating_matches = regex.findall(REGEX_RATING,response.text)
        poster_matches = regex.findall(REGEX_POSTER,response.text)
        show_movie(title_matches,rating_matches,poster_matches)

if __name__ == '__main__':
    root = Tk()
    root.title('Sistema de Recomendaciones')
    root.geometry('1280x720')
    
    btn_movie = Button(root,text='Recomendar película',height=1,command=partial(main,'P'),font=font.Font(size=13))
    btn_movie.place(x=0,y=100)

    btn_tv_show = Button(root,text='Recomendar serie de TV',height=1,command=partial(main,'TV'),font=font.Font(size=13))
    btn_tv_show.place(x=0,y=300)

    label1 = Label(root,height=1,width=30,font=font.Font(size=14))
    label1.place(x=300,y=50)

    label_title_year = Label(root,height=2,width=35,text='',font=font.Font(size=13))
    label_title_year.place(x=400,y=200)

    label_extra_info = Label(root,height=2,width=35,text='',font=font.Font(size=13))
    label_extra_info.place(x=400,y=350)

    label_rating = Label(root,height=2,width=35,text='',font=font.Font(size=13))
    label_rating.place(x=400,y=500)

    root.mainloop()