import requests
from bs4 import BeautifulSoup
import pandas as pd

blog_url = "https://floranativadeuruguay.blogspot.com"
texto_link_siguiente = "Entradas antiguas"
CSV_FILE = "links.csv"
COLUMNS = [
    'titulo',
    'link'
]


next_page = blog_url
posts = []
while next_page:
    response = requests.get(next_page)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Procesar los posts de la página actual
    titulos = soup.find_all('h3','entry-title')
    for titulo in titulos:
        link = titulo.find("a")
        title = link.get_text(strip=True)
        url = link['href']
        print(title)
        print(url)
        posts.append((title, url))

    # Encontrar el enlace a la página siguiente
    next_button = soup.find('a', string=texto_link_siguiente)
    if next_button and next_button['href']:
        next_page = next_button['href']
        if next_page.startswith('/'):
            next_page = blog_url + next_page
    else:
        next_page = None  # Termina el bucle si no hay más páginas

df = pd.DataFrame(posts, columns=COLUMNS)
df.to_csv(CSV_FILE, index=False)
