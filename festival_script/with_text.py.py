import os
import pytesseract as tess
tess.pytesseract.tesseract_cmd = "C:/Users/WOT-Dhruvin/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
from PIL import Image
import pandas as pd
import json
import time

import csv
from csv import DictWriter
from csv import writer

from googletrans import Translator

def read_language_json():
    with open('languages.json') as file:
            json_data = json.load(file)
            # print(data['Dutch'])
            return json_data
json_data = read_language_json()

def read_google_language_json():
    with open('google_language_json.json') as file:
        json_data = json.load(file)
        return json_data
google_language = read_google_language_json()
# print(google_language['English'])
# print(type(json_data['Odia']))
# exit(0)

def google_translator(string,source_lang,dest_lang):
    translator = Translator()
    # print('sgjnwiueofhiuowqejhnoi===============',source_lang,dest_lang)
    translate= translator.translate(string, src = source_lang, dest=dest_lang)
    # print(translate)
    return translate.text


def check_config_json_created():
    file_exists = os.path.isfile('ocr_counter_json.json') 
    # print(file_exists)
    if file_exists:
        # print('Json file already created')
        print('')
    else:
        config_dic = { 
                        'for_loop_counter_ocr' : 0,
                        }
        with open ('ocr_counter_json.json','w') as file:
            json.dump(config_dic,file)

def load_json():
    check_config_json_created()
    with open('ocr_counter_json.json') as file:
        data = json.load(file)
        return data

def overwrite_json(counter):
    with open('ocr_counter_json.json', 'w') as f:
        data = {
                "for_loop_counter_ocr": counter,
                }
        json.dump(data, f)

def create_csv(file_name):
    # print(file_name)
    # print(f'ocr_{file_name}')
    file_name = f'ocr_{file_name}'
    file_exists = os.path.isfile(file_name)
    # print(file_exists)
    if file_exists:
        # print('Json file already created')
        print('')
    else:
        # print('Not created')
        with open(file_name, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Category", "Business Category", "Language","Image URL","Downloaded Img Path","OCR/Text","Translated to English"])

    return file_name

def append_csv(file_name,list_data):
    
    new_ocr_csv_file_name = create_csv(file_name)
    with open(new_ocr_csv_file_name, 'a', newline='',encoding='utf-8') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_data)
        f_object.close()


load_json_counter = load_json()
x = load_json_counter['for_loop_counter_ocr']
# print(x)

def read__csv(file_name):



    path = os.getcwd() + '/updated_csv/' + file_name

    df = pd.read_csv(path)
    # df = pd.read_csv(r"updated_csv/output_Daily Category Images.csv")
    # print(df.head())


    category_list = df['Category'].to_list()
    business_category_list = df['Business Category'].to_list()
    languages_list = df['Language'].to_list()
    downloaded_img_path = df['Downloaded Img Path'].to_list()
    url_list = df['Image URL'].to_list()
    text_list = df['Text'].to_list()


    print(len(category_list),len(business_category_list),len(languages_list),len(downloaded_img_path),len(url_list))


    
    start = load_json_counter['for_loop_counter_ocr']
    for each_row_count in range(start,len(downloaded_img_path)):
        print(each_row_count, file_name)

        if downloaded_img_path[each_row_count] != 'None':
            # print(downloaded_img_path[each_row_count] ,'=====' ,json_data[languages_list[each_row_count]] , '====', languages_list[each_row_count], '====',each_row_count)

            if languages_list[each_row_count] != "odia":
                # img = Image.open(downloaded_img_path[each_row_count])
                # text = tess.image_to_string(img, lang = json_data[languages_list[each_row_count]] )

                # img = Image.open('C:/Users/WOT-Dhruvin/Downloads/8264b0da5d5129281.jpg')
                # text = tess.image_to_string(img, lang = 'guj' )
    
                # text = text.strip('\n')
                # text = text.replace('\n',' ')
                # print('TEXT ====',text, type(text))
                text = text_list[each_row_count]
                # print(text,'----------------',type(text))
                get_translated_text = google_translator(text,google_language[languages_list[each_row_count]],'en')
                # get_translated_text = google_translator(text,'gu','en')

                # print(get_translated_text)
            else:
                text = ' '
                get_translated_text = ''
            
            # print({category_list[each_row_count]},'-----------')


        elif downloaded_img_path[each_row_count] == 'None':
            # print(downloaded_img_path[each_row_count] ,'=====' ,json_data['Dutch'] , '====', languages_list[each_row_count], '====',each_row_count)
            text = ' '
            get_translated_text = ''

        dict_ = [category_list[each_row_count] ,business_category_list[each_row_count] ,languages_list[each_row_count],
                url_list[each_row_count],downloaded_img_path[each_row_count],text,get_translated_text]
        # print(dict_, len(dict_))

        append_csv(file_name,dict_)
        # print(each_row_count)
        each_row_count += 1
        overwrite_json(each_row_count)
        # time.sleep(3)

        # if each_row_count == 10:
            # break




if __name__ == '__main__':

    read__csv('output_Festival Images.csv')