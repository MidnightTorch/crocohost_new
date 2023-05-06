import os
from flask import Flask, render_template, request
from configs import *
from img_loader import Img_loader
import json
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

loader = Img_loader()
loader.screens_path = '/home/admnini/python_projs/crocohost/static/screens'
loader.create_tree_of_screens()


def create_translation_dict(dict_to_translate):
    return_dict = {}
    for key in list(translations_dict.keys()):
        res_key = translations_dict[key]
        return_dict[res_key] = dict_to_translate[key]

    not_added_keys = set(translations_dict.keys()) - set(dict_to_translate.keys())
    for not_added_key in not_added_keys:
        return_dict[not_added_key] = False

    return return_dict

def get_template_attr(flag='notfisrt'):
    img_to_display = ''
    description_to_display = ''
    countries = ''
    personalities = ''
    type = ''
    topic = ''
    loader.create_tree_of_screens()

    if flag != 'first':
        query_params = request.args.to_dict()['caricature']
        splited_params = query_params.split('&')
        loader.curr_year = splited_params[1].partition('=')[2]
        loader.curr_publication = splited_params[2].partition('=')[2]
        loader.curr_screen = splited_params[3].partition('=')[2]

    next = [str(i) for i in loader.next_image()]
    previous = [str(i) for i in loader.previous_image()]

    img_to_display = os.path.join('static', 'screens', loader.curr_year, loader.curr_publication,
                                  loader.curr_screen)
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


    return {'image': img_to_display,
            'description': description_to_display,
            'countries': countries,
            'personalities': personalities,
            'year': loader.curr_year,
            'publication': loader.curr_publication,
            'name': loader.curr_screen,
            'type': type,
            'topic': topic,
            'next': next,
            'previous': previous}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/caricatures', methods=['GET'])
def caricatures():
    # case entering via link on main page
    if len(request.args) == 0:
        loader.choose_first_img()
        render_dict = get_template_attr(flag='first')

    else: render_dict = get_template_attr(flag='notfisrt')

    return render_template('caricature.html',
                           image=render_dict['image'],
                           descriprion=render_dict['description'],
                           countries=render_dict['countries'],
                           personalities=render_dict['personalities'],
                           year=render_dict['year'],
                           publication=render_dict['publication'],
                           name=render_dict['name'],
                           type=render_dict['type'],
                           topic=render_dict['topic'],
                           next=render_dict['next'],
                           previous=render_dict['previous'])


@app.route('/tree')
def tree():
    return render_template('tree.html', loader=loader)


if __name__ == '__main__':
    app.run(debug=True)
