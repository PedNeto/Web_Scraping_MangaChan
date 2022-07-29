# Script feito por Pedro Neto
# Inicio do trabalho: 11/07/2022
# Termino do trabalho: 26/07/2022

from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib.request
import requests
import csv
import re
import os

# Insere o nome do manga para fazer uma busca no site
# traz informações do manga selecionado e manda para as funções
name = input('Digite o nome do manga: ')
search = name.replace(" ", "-")
response = requests.get(f'https://mangaschan.com/manga/{search}')
soupe = BeautifulSoup(response.text, 'html.parser')

try:
    os.mkdir(f'{name}')
except FileExistsError:
    print(f'O Arquivo {name} Já Existe')
    exit
else:
    # Traz o nome formatdo
    # Cria um arquivo .txt e salva esse nome dentro dele
    def MangaName():
        class_name = soupe.find('div', class_='seriestuheader')
        h1_name = class_name.find('h1').text
        with open(f'{name}/1#{h1_name}.txt', 'a', encoding='utf8') as file:
            file.write(f'Nome do manga: {h1_name}\n\nSinopse:\n')
        return h1_name

    name_mg = MangaName()

    # Traz a Sinopse Formatada e insere o texto dentro do arquivo .txt
    def Sinopse():
        class_sinops = soupe.find(class_='entry-content entry-content-single')
        p = class_sinops.find_all('p')
        p2 = len(p)
        for count in range(p2):
            inf = p[count]
            inf = re.sub('<[^>]+?>', '', str(inf))
            with open(f'{name}/1#{name_mg}.txt', 'a', encoding='utf8') as file:
                file.write(f'{inf}\n')

    # Busca os capitulos e armazena na variavel (sch_cp)
    def Capitulos():
        class_cap = soupe.find(class_='eplister')
        cap_num = class_cap.find_all('li')
        sch_cp = re.findall(r'data-num="([\w\.]+)', str(cap_num))
        sch_cp = sch_cp[::-1]
        return sch_cp

    # Busca os Links de cada capitulo e armazena na variavel (href_cp)
    def LinkMg():
        class_cap = soupe.find(class_='eplister')
        cap_num = class_cap.find_all('li')
        href_cap = re.findall(r'a href="(https[://\w\.-]+)', str(cap_num))
        href_cap = href_cap[::-1]
        return href_cap

    # Traz os capitulos e links armazenados e salva em um .csv
    def CsvCL():
        num = len(Capitulos())
        for count in range(num):
            sch_cap = Capitulos()[count]
            href_cap = LinkMg()[count]
            link_Cap = f'{sch_cap},{href_cap}'
            with open(f'{name}/2#MangaLinks.csv', 'a')as file:
                file.write(f'{link_Cap}\n')

    # Cria umpa pasta para cada Capitulo
    # Pega os links das imgens, Faz o download e salva na pasta Capitulo
    def Img():
        try:
            os.mkdir(f'{name}/Capitulo-{cpt}')
            num = len(src_link)
        except Exception as erro:
            if erro.__class__ == FileExistsError:
                print(f'O Arquivo Capitulo-{cpt} já Existe')
                exit
        else:
            for c in range(num):
                s = src_link[c]
                image_url = s  # Url da imagem
                # Local e nome da imagem
                save_name = f'{name}/Capitulo-{cpt}/Pagina-{c}.jpg'
                urllib.request.urlretrieve(image_url, save_name)
            print(f'CAPITULO-{cpt} BAIXADO COM SUCESSO')

    Sinopse()
    Capitulos()
    LinkMg()
    CsvCL()

    # Entra no csv e traz o link do Capitulo e a numeração
    # faz uma requisição no site para trazer o link das imgs dos Capitulos
    # e em seguida manda para a Função img() para fazer o donwload dessas imgs
    with open(f'{name}/2#MangaLinks.csv', 'r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            cpt = lines[0]
            link = lines[1]
            res_link = requests.get(f'{link}')
            soupe2 = BeautifulSoup(res_link.text, 'html.parser')
            id_link = soupe2.find(id='readerarea')
            img_link = id_link.find_all('img')
            src_link = re.findall(r'src="(https[://\w\.-]+)', str(img_link))
            Img()
