from bs4 import BeautifulSoup
import requests
import pandas as pd

#leer csv de ids
photo_ids = pd.read_csv('ID-Dominio Publico FMH.csv', header=None).iloc[:, 0]

data_list = []

#headers para no ser identificades como bots
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

for photo_id in photo_ids:
    row_data = {}
    row_data["id"] = photo_id
    #obtener url
    url = "https://cdf.montevideo.gub.uy/catalogo/foto/"+photo_id.lower()
    print(url)
    #traer la página
    page_to_scrape = requests.get(url, headers=headers)

    #parsear con BeautifulSoup 
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    #todo lo que tenga texto lo guardamos
    rows = soup.findAll('tr')
    for row in rows:
        cells = row.findAll("td")
        if len(cells):
            column_name = cells[0].text
            cell_value = cells[1].text
            row_data[column_name] = cell_value
    
    # Encuentra el enlace con la clase "descarga_alta_resolucion"
    link_element = soup.find('a', class_='descarga_alta_resolucion')

    # Si se encuentra el enlace, agrega la URL a la fila
    if link_element:
        row_data['descarga_alta_resolucion'] = "https://cdf.montevideo.gub.uy"+link_element.get('href')
    else:
        row_data['descarga_alta_resolucion'] = None

    # Agregar la fila a la lista de datos
    data_list.append(row_data)

#crear dataframe
df = pd.DataFrame(data_list)
#crear csv
df.to_csv('scraped_photos.csv', index=False)
