# importing the module
import imdb
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os 
import folium
from folium import plugins
import warnings

from bs4 import BeautifulSoup
import pandas as pd

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")
chrome_options = webdriver.ChromeOptions()



# chrome_options.add_argument('--kiosk-printing')
CHROMEDRIVER_PATH ='D:/keval/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--log-level=3')
options.add_argument('--ignore-certificate-errors')

CHROMEDRIVER_PATH ='D:/keval/chromedriver'



ia = imdb.IMDb() 

''' --------------------------------------------------------------------------------For CODE Fetching---------------------------------------------------------------------'''


# Url_travel = requests.get(f'https://www.imdb.com/chart/top/?ref_=nv_mv_250')
# soup = BeautifulSoup(Url_travel.text)
# f2 = soup.find('table')
# id_codes = []
# for f in f2.findAll('a'):
#   id = (str(f)[18::].split("/"))[0]
#   if id not in id_codes:
#     id_codes.append(id)
# print(id_codes)
# record = pd.DataFrame({'code': id_codes})
# record.to_excel('Code.xlsx',index=False)
    

''' --------------------------------------------------------------------------------For Movie_Title Fetching---------------------------------------------------------------------'''
# def get_title(id_code):
#     id_code = pd.read_excel('D:\keval\movie_get\Code.xlsx')
#     code = id_code.iloc[:,0].to_list()
#     code = id_code
#     ia = imdb.IMDb()
#     movie = []
#     for i in range(len(code)):
#       print(f'----------------------{i}----------------------------')
#       movie.append(ia.get_movie(int(code[i])))
#       print(f'----------------------{i} Compeleted----------------------------')
 
    
    
    # record = pd.DataFrame({'Movie': movie})
    # record.to_excel('movie.xlsx',index=False)

''' --------------------------------------------------------------------------------For Location Fetching---------------------------------------------------------------------'''
id_code = pd.read_excel('D:\keval\movie_get\Code.xlsx')
code = id_code.iloc[:,0].to_list()

loc =[]
locm= []

corrdin = { }
for i in range(203,len(code)):

        coder = (code[i])
        movie = ia.get_movie(int((code[i])[1::]))
    
        print(f'---------------------Location-{i}----------------------------')

        x = requests.get(f'https://www.imdb.com/title/t{coder}/locations?ref_=tt_dt_loc')


       
       
        try:
            soup = BeautifulSoup(x.text)
            f2 = soup.find('section', id="filming_locations")
            for f in f2.findAll('dt'):
                loc.append((f.text.replace('&nbsp;', '')).replace('\n',''))

            locm.append(loc) 
            loc = []
      
            
          
        except Exception as err:
                print(f'{type(err).__name__} rasie error: {err}')
            
                loc.append(f'null')
                locm.append(loc)
            
                loc = []
             
                print(f'----------------Location------{i}- Completed---------------------------')
                
            
        
        

        print(f'-------------------Location---{i}- Completed---------------------------')

       
 
        
        
        if locm[0][0] == 'null':
            coder = coder if type(coder) is list else [coder]
            movie = movie if type(movie) is list else [movie]
            record2 = pd.DataFrame({'code':coder,'movie_tile':movie,'lat_lon':locm[0][0]}) 

            record2.to_csv('locations.csv',index=False,mode='a',header=False)
           
            locm = []
            continue

            
        else:
            print(len(locm[0]))
            coor = []

            wd = webdriver.Chrome(chrome_options=options,executable_path = CHROMEDRIVER_PATH)
            print("---------------------------Entering Location-------------------------------------")
            wd.get("https://www.distancesto.com/coordinates.php")

            for j in range(len(locm[0])):
                print(f"----------------------------------Main Function Running {j}-----------------------------------------------------------------------------------")
                row = locm[0]
               
                
                WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID,"doproc")))
                time.sleep(1)
                Place = wd.find_element_by_id("from-location")
                Place.send_keys(row[j])
                WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID,"doproc")))
                Submit = wd.find_element_by_id("doproc")
                Submit.click()
                print("---------------------------Fecthing Coordinates-------------------------------------")
                WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID,"doproc")))
                time.sleep(2)
                print("---------------------------Coordinates Fetched-------------------------------------")
                name = row[j]
                content = wd.page_source
                soup = BeautifulSoup(content)
                coord = []
                case = soup.find('form', id="CoordinatestoLocation")
                for k in case.findAll('input'):
                    t = k.get('value')
                    coord.append(t)
                time.sleep(2) 
                # lat,lon = float(coord[0]),float(coord[1])
                corrdin[name] =  coord 
                Place = wd.find_element_by_id("from-location")
                Place.clear()
                WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID,"doproc")))
                


            coor.append(corrdin)
            corrdin = { }
            print(f"-----------------------------Main Function Running {j}------Completed-----------------------------------------------------------------------------")
      
        record2 = pd.DataFrame({'code':coder,'movie_tile':movie,'lat_lon':coor}) 

        record2.to_csv('locations.csv',index=False,mode='a',header=False)
        locm.pop()
      
# record = pd.DataFrame({'lat,lon' : coor})
# record.to_excel('lat_lon.xlsx')



