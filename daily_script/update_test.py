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


# download_parent_folder_path = 'D:/dhruvin_project/brand_live/Download_images/'
# download_sub_folder_path = 'Daily_Category_Images'
# download_full_folder_path = download_parent_folder_path + download_sub_folder_path
download_parent_folder_path = os.getcwd() + '/Download_images/'


def persist_image(folder_path:str,url:str,count:str,new_column:list):
    # print('Folder_path ===== ', folder_path)
    # print('URL==========', count)
   
    try:
        image_content = requests.get(url).content
    
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10]+str(count)+str(random.randint(1, 1000)) + '.jpg')
        print(file_path)

        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=100)
        # print(f"SUCCESS - saved {url} - as {file_path}")
       
        new_column.append(file_path)

    except Exception as e:
        # print(f"ERROR - Could not save {url} - {e}")
        
        new_column.append('None')
        with open(os.getcwd() +'/images not downloaded.txt', 'a+') as f:
            f.write(str(folder_path)+'=========' + str(url) + '\n')




def read__csv(each_csv):

# df_list = []

    path = os.getcwd() + '/csv_files/'



    new_column = []
    full_list_url_and_download_path = []
    
    download_sub_folder_path = each_csv.split('.')[0]
    df = pandas.read_csv(path+each_csv) 
   
    
    print('')

    download_full_folder_path = download_parent_folder_path + download_sub_folder_path

    
    i = 0
    for index,each_url in df.iterrows():
        i += 1
    
        try:
            download_partition_folder = download_full_folder_path + os.sep + each_url['Category'] + os.sep + each_url['Business Category']
            full_list_url_and_download_path.append((each_url['Image URL'],download_partition_folder))
            print()
        except:
            each_url['Category'] = 'Not Found'
            each_url['Business Category'] = 'Not Found'
            download_partition_folder = download_full_folder_path + os.sep + each_url['Category'] + os.sep + each_url['Business Category']
            full_list_url_and_download_path.append((each_url['Image URL'],download_partition_folder))

        
        # if i == 60:
        #     break
    # # break
    print('*****')

    skip = 1
    length = len(full_list_url_and_download_path)
    print(length,each_csv)
    i = 0

    each_count = 0
    while i < length:
        thread_list = []
       
        images_list = full_list_url_and_download_path[i: skip + i]
   
        i += skip

        for url in images_list:
            each_count += 1

            print('count ----- ',each_count, download_sub_folder_path)
        
    
            if not os.path.exists(url[1]):
                os.makedirs(url[1])
            t1 = threading.Thread(target=persist_image, args=(url[1],url[0],each_count,new_column, ))
            thread_list.append(t1)

        for t1 in thread_list:
            t1.start()

        for t1 in thread_list:
            t1.join()


    print('new_column=========', len(new_column))
    df['Downloaded Img Path'] = new_column

    partial_updated_csv_path = os.getcwd() + '/updated_csv/'
    if not os.path.exists(partial_updated_csv_path):
        os.makedirs(partial_updated_csv_path)

    df.to_csv(partial_updated_csv_path+'output_'+ str(download_sub_folder_path) + '.csv', index=False)
   





if __name__ == '__main__':
    read__csv('test.csv')
    # read__csv('Daily images without content text.csv')