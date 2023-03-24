import os
from flask import Flask, render_template, request
from configs import *
from img_loader import Img_loader
import json

app = Flask(__name__)

loader = Img_loader()
loader.screens_path = '/home/dev/projects/crocohost/crocohost/static/screens'
loader.create_tree_of_screens()


@app.route('/')
def index():
    return render_template('index.html')

def create_translation_dict(dict_to_translate):
    return_dict = {}
    for key in list(translations_dict.keys()):
        res_key = translations_dict[key]
        return_dict[res_key] = dict_to_translate[key]

    not_added_keys = set(translations_dict.keys()) - set(dict_to_translate.keys())
    for not_added_key in not_added_keys:
        return_dict[not_added_key] = False

    return return_dict


@app.route('/caricatures', methods=['GET'])
def caricatures():
    query_params = request.args
    img_to_display = ''
    description_to_display = ''
    countries = ''
    personalities = ''
    type = ''
    topic = ''



    if 'control_button' in query_params:
        if query_params['control_button'] == 'Next':
            loader.next_image()
            img_to_display = os.path.join('static', 'screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
            path_to_file = os.path.join('screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
            description_to_display = loader.get_description_from_db(path_to_file)

        if query_params['control_button'] == 'Previous':
            loader.previous_image()
            img_to_display = os.path.join('static', 'screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
            path_to_file = os.path.join('screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
            description_to_display = loader.get_description_from_db(path_to_file)

    elif 'specific_img' in query_params:
            loader.curr_year = query_params['year']
            loader.curr_publication = query_params['publication']
            loader.curr_screen = query_params['screen']
            img_to_display = os.path.join('static', 'screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
            path_to_file = os.path.join('screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
            description_to_display = loader.get_description_from_db(path_to_file)

    else:
        loader.choose_first_img()
        img_to_display = os.path.join('static', 'screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
        path_to_file = os.path.join('screens', loader.curr_year, loader.curr_publication, loader.curr_screen)
        description_to_display = loader.get_description_from_db(path_to_file)


    if len(description_to_display) != 0:
        description_to_display = json.loads(description_to_display[0]['description'])
        type = description_to_display['type']
        topic = description_to_display['topic']
        if description_to_display['country'] != '':
            countries = ', '.join(description_to_display['country'])
        if description_to_display['personality'] != '':
            personalities = ', '.join(description_to_display['personality'])
        description_to_display = create_translation_dict(description_to_display)

    else:
        description_to_display = 'Изображение еще не описано'

    print(img_to_display) 

    return render_template('caricature.html', image=img_to_display, descriprion=description_to_display,
        countries=countries, personalities=personalities,
        year=loader.curr_year, publication=loader.curr_publication, name=loader.curr_screen,
        type=type, topic=topic)


@app.route('/tree')
def tree():
    return render_template('tree.html', loader=loader)


if __name__ == '__main__':
    app.run(debug=True)
