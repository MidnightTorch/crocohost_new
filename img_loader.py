import os
import pymysql


HOST = 'localhost'
USER = 'root'
PASSWORD = 'password'
DATABASE = 'pictures'

def connect_to_db(func):
    def wrapper(*args, **kwargs):
        with pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cursor:
                sql = func(*args, **kwargs)
                cursor.execute(sql, args[1::])
                conn.commit()
                return cursor.fetchall()

    return wrapper


class Img_loader:
    def __init__(self):
        self.curr_year = ''
        self.curr_publication = ''
        self.curr_screen = ''
        self.dir_tree = {}
        self.screens_path = ''

    @connect_to_db
    def get_description_from_db(self, path_to_file):
        sql = 'SELECT description FROM `data` WHERE `path_to_picture` LIKE (%s)'
        return sql



    def choose_first_img(self):
        first_year = sorted(list(self.dir_tree.keys()), key=lambda num: int(num))[0]
        first_publication = sorted(self.dir_tree[f'{first_year}'], key=lambda num: int(num))[0]
        fisrt_screen = sorted(self.dir_tree[f'{first_year}'][f'{first_publication}'],
                              key=lambda num: int(num.split('.')[0]))[0]
        self.curr_year = first_year
        self.curr_publication = first_publication
        self.curr_screen = fisrt_screen



    def create_tree_of_screens(self):
        for year in sorted(os.listdir(f'{self.screens_path}')):
            self.dir_tree[f'{year}'] = {}
            for publication in sorted(os.listdir(f'{self.screens_path}/{year}'), key=lambda val: int(val)):
                for screen in sorted(os.listdir(f'{self.screens_path}/{year}/{publication}')):
                    if f'{publication}' in self.dir_tree[f'{year}'].keys():
                        self.dir_tree[f'{year}'][f'{publication}'].append(screen)
                    else:
                        self.dir_tree[f'{year}'][f'{publication}'] = [screen]

    def next_image(self):
        # check of null image
        if self.curr_screen == '':
            return 0

        current_publication_list = sorted(self.dir_tree[f'{self.curr_year}'][f'{self.curr_publication}'],
                                          key=lambda num: int(num.split('.')[0]))
        current_year_list = sorted(list(self.dir_tree[f'{self.curr_year}'].keys()),
                                   key=lambda num: int(num))
        list_of_years = sorted(list(self.dir_tree.keys()), key=lambda num: int(num))

        ### case needed next_image
        if self.curr_screen != current_publication_list[-1]:
            inx_of_current_screen = current_publication_list.index(self.curr_screen)
            self.curr_screen = current_publication_list[inx_of_current_screen + 1]

        ### case current screen is the last one in the publication
        elif self.curr_screen == current_publication_list[-1] and self.curr_publication != current_year_list[-1]:
            inx_of_current_publication = current_year_list.index(self.curr_publication)
            self.curr_publication = current_year_list[inx_of_current_publication + 1]
            new_publication_list = sorted(self.dir_tree[f'{self.curr_year}'][f'{self.curr_publication}'])
            self.curr_screen = new_publication_list[0]


        ### case need to change year
        elif self.curr_screen == current_publication_list[-1] and self.curr_publication == current_year_list[-1] and \
                list_of_years[-1] != self.curr_year:
            inx_current_year = list_of_years.index(self.curr_year)
            self.curr_year = list_of_years[inx_current_year + 1]
            self.curr_publication = sorted(self.dir_tree[f'{self.curr_year}'])[0]
            self.curr_screen = sorted(self.dir_tree[f'{self.curr_year}'][f'{self.curr_publication}'])[0]


    def previous_image(self):
        if self.curr_screen == '':
            return 0
        current_publication_list = sorted(self.dir_tree[f'{self.curr_year}'][f'{self.curr_publication}'],
                                          key=lambda num: int(num.split('.')[0]))
        current_year_list = sorted(list(self.dir_tree[f'{self.curr_year}'].keys()),
                                   key=lambda num: int(num))
        list_of_years = sorted(list(self.dir_tree.keys()), key=lambda num: int(num))

        ### case needed rpevious image
        if self.curr_screen != current_publication_list[0]:
            inx_of_current_screen = current_publication_list.index(self.curr_screen)
            self.curr_screen = current_publication_list[inx_of_current_screen - 1]

        ### case current screen is the first one in the publication
        elif self.curr_screen == current_publication_list[0] and self.curr_publication != current_year_list[0]:
            inx_of_current_publication = current_year_list.index(self.curr_publication)
            self.curr_publication = current_year_list[inx_of_current_publication - 1]
            new_publication_list = sorted(self.dir_tree[f'{self.curr_year}'][f'{self.curr_publication}'])
            self.curr_screen = new_publication_list[-1]

        ### case need to change year
        elif self.curr_screen == current_publication_list[0] and self.curr_publication == current_year_list[0] and \
                list_of_years[0] != self.curr_year:
            inx_current_year = list_of_years.index(self.curr_year)
            self.curr_year = list_of_years[inx_current_year - 1]
            self.curr_publication = sorted(self.dir_tree[f'{self.curr_year}'])[-1]
            self.curr_screen = sorted(self.dir_tree[f'{self.curr_year}'][f'{self.curr_publication}'])[-1]
