import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
st. set_page_config(layout="wide")


record = pd.read_csv('D:\keval\movie_get\locations.csv')
map_map = folium.Map()


movie_name = record["movie_tile"].to_list()
na =  record["movie_tile"].to_list()

col1, col2 ,col3 = st.columns([2,4,4])
def get_option():
    option = st.selectbox(
    'Choose the movie you like!',
    movie_name)

    
    return option
def summary(name):
    print(name)
    lat_lon = (record[record["movie_tile"]== f"{name}"].lat_lon).to_list()
    print(lat_lon)
    if lat_lon[0] == 'no':
        pass

    else:
        lat_lon = eval(lat_lon[0])
        st.header(f'Fliming locations of {name}')
        for i in lat_lon.keys():
            st.write(i)


def map(name):
    
    lat_lon = (record[record["movie_tile"]== f"{name}"].lat_lon).to_list()
    
    if lat_lon[0] == 'no':
        pass

    else:
        lat_lon = eval(lat_lon[0])
 




# row = eval(cor[4])
        for j in lat_lon.keys():
    

            iframe = folium.IFrame(name+'\n'+j)
            Popup = folium.Popup(iframe,
                                 min_width=180,
                                 max_width=300)
            folium.Marker(
                    location=[float(lat_lon[j][0]),float(lat_lon[j][1])], # coordinates for the marker (Earth Lab at CU Boulder)

                    popup=Popup , # pop-up label for the marker

                    icon=folium.Icon()
                        ).add_to(map_map)
        st_data = st_folium(map_map, width= 725)




with col1:
    st.title('Movie Name')
    
    n = get_option()
    
with col2:
    st.title('Movie Summary')
    
    if n == 'Select the movie' :
            pass
    else:
        summary(n)

    
    

with col3:
    st.title('Fliming Locations')
    op = st.selectbox(
    'Choose Map type',
    ('basemap','satellite',))
    if op == 'satellite':

        tile = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
       ).add_to(map_map)
        map(n)
    else:
        if n == 'Select the movie':
            pass
        else:
            map(n)


     
   
    
        
   


               

                    

