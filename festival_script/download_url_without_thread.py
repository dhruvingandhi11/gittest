import os
import pandas
import threading 
import requests
import time
import os 
import requests
import io
from PIL import Image
import hashlib
import glob
import random
import json


download_parent_folder_path = os.getcwd() + '/Download_images/'


def check_config_json_created():
    file_exists = os.path.isfile('config.json')
    if file_exists:
        print('Json file already created')
    else:
        config_dic = {"counter": 0 , 'appended_column_list' : []}
        with open ('config.json','w') as file:
            json.dump(config_dic,file)

    with open('config.json') as file:
        data = json.load(file)
        return data


def overwrite_json(counter,download_path_list):
    with open('config.json', 'w') as f:
        data = {
                "counter": counter,
                'appended_column_list': download_path_list}
        json.dump(data, f)

def persist_image(folder_path:str,url:str,count:str,new_column:list):
    # print('Folder_path ===== ', folder_path)
    # print('URL==========', url)
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        
        # file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10]+str(count)+str(random.randint(1, 1000)) + '.jpg')
        
        # print('=============================================================',file_path)

        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=100)
        new_column.append(file_path)
        # print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        # print(f"ERROR - Could not save {url} - {e}")
        new_column.append('None')
        with open(os.getcwd() +'/images not downloaded.txt', 'a+') as f:
            f.write(str(folder_path)+'=========' + str(url) + '\n')


def run_csv_file(file_name):
    df_list = []
    # path = "D:/dhruvin_project/brand_live/csv_files/"
    path = os.getcwd() + '/csv_files/'

    
    full_list_url = []
    print(file_name)
    download_sub_folder_path = file_name.split('.')[0]
    df = pandas.read_csv(path+file_name) 

    download_full_folder_path = download_parent_folder_path + download_sub_folder_path
    if not os.path.exists(download_full_folder_path):
        os.makedirs(download_full_folder_path)

    category_list = df['Category'].to_list()
    business_category_list = df['Business Category'].to_list()
    url_list = df['Image URL'].to_list()
    print(len(category_list))

    json_data = check_config_json_created()


    print(f"{json_data = }")
    print(json_data['counter'])

    start = json_data['counter']
    end = len(category_list)


    print('START =====',start , end)

    new_column = json_data['appended_column_list']

    for each_row_count in range(start,end):
       
        start += 1
       
        # time.sleep(2)
        try:
            download_partition_folder = download_full_folder_path + os.sep + category_list[each_row_count] + os.sep + business_category_list[each_row_count]
   
            print('In for loop ====' ,start, file_name)

            if not os.path.exists(download_partition_folder):
                os.makedirs(download_partition_folder)
                
            persist_image(download_partition_folder,url_list[each_row_count],start,new_column)
            # overwrite_json(start,new_column)
        except:
            pass


    df['Downloaded Img Path'] = json_data['appended_column_list']
    
    partial_updated_csv_path = os.getcwd() + '/updated_csv/'
    if not os.path.exists(partial_updated_csv_path):
        os.makedirs(partial_updated_csv_path)

    df.to_csv(partial_updated_csv_path+'output_'+ str(download_sub_folder_path) + '.csv', index=False)

    

if __name__ == '__main__':

    # file_name = ['Festival Images.csv' , 'Festival Images.csv']
    # json_path = os.getcwd() + '/config.json'
    # # time.sleep(5)
    # # with open(json_path) as file:
    # #     data = json.load(file)
    # # print(data)
    # # print(json_path)
    # for i in file_name:
    #     run_csv_file(i)
    #     os.remove(json_path)
    #     time.sleep(5)


    run_csv_file("festival Images without content text.csv")
    # delete first Json file
    # run_csv_file('Festival Images.csv')


