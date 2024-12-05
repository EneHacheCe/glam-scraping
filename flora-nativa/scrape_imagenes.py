import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

LINKS_CSV = "links.csv"
IMAGENES_CSV = "imagenes.csv"
MAX_POSTS=2000
COLUMNS = [
    'titulo',
    'fecha',
    'descripcion',
    'nombre_de_archivo_para_commons',
    'enlace_imagen',
    'enlace_post',
]

imagenes_array=[]

if os.path.exists(LINKS_CSV):
    post_links = pd.read_csv(LINKS_CSV,header=0)

for index, row in post_links.iterrows():
    post_link = row["link"]
    response = requests.get(post_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    post_content = soup.find('div','post-body')
    
    fecha_array = post_link.replace("https://floranativadeuruguay.blogspot.com/","").split("/")
    fecha = fecha_array[0]+"-"+fecha_array[1]

    print(post_link)
    print(post_content)
    descripcion = post_content.get_text(strip=True)
    if descripcion=="": 'Fotografía provista por Andrés González, blog Flora Nativa de Uruguay';

    imagenes_a = post_content.find_all("a")
    for i, imagen_a in enumerate(imagenes_a):
        nombre_de_archivo_para_commons = row["titulo"]
        if i!=0:
            nombre_de_archivo_para_commons += (" "+str(i))
        nombre_de_archivo_para_commons += ".jpg"

        if (imagen_a.find("img")):
            imagenes_array.append([
                row["titulo"],
                fecha,
                descripcion,
                nombre_de_archivo_para_commons,
                imagen_a['href'],
                post_link
            ])
    
    if index==MAX_POSTS: break;

df = pd.DataFrame(imagenes_array, columns=COLUMNS)
df.to_csv(IMAGENES_CSV, index=False)
