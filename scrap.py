import json
import random
import time
import easyocr
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from bs4 import BeautifulSoup
import requests

def sleep_req():
    time.sleep(random.randint(2, 4))


url = 'https://www.spr.ru/all/'
headers = {'Accept': 'text/html,application/xhtml+xml, application/xml;q=0.9,image/avif,image/webp,image/apng,'
                    '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                    'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

req = requests.get(url,headers=headers,)
req.encoding = 'windows-1251'


with open('index.html', 'w', encoding='windows-1251') as file:
    file.write(req.text)

with open('index.html', 'r', encoding='windows-1251') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

category_links = soup.find(id="leftside").find_all(class_='zagolovok')
with open('data/category_links.txt', 'w') as file:

    for item in category_links:
       file.write(str(item.get('href')).replace('//', '') + '\n')


with open('data/category_links.txt', 'r') as file:
    category_list = file.read().strip().split('\n')

for link in category_list:
    url = f'http://{link}'
    req = requests.get(url, headers=headers)

    with open(f'data/{link[14:-1].replace("-", "_")}.html', 'w') as file:
        file.write(req.text)
    print(f'{link} done')
    sleep_req()

with open('data/avto.html', 'r') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

subcategory_list = soup.find(id='leftside').find_all(style='margin-bottom:7px;')
organization_links_list = []
for item in subcategory_list:
    organization_link = f'http:{item.find("a").get("href")}'
    organization_links_list.append(organization_link)
i = 1
for link in organization_links_list:
    url = link
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')

    cards_list = soup.find_all(class_='itemTitle')
    card_json = []
    sleep_req()
    for card in cards_list:
        url = f"http:{card.get('href')}"
        req = requests.get(url, headers=headers)

        soup = BeautifulSoup(req.text, 'lxml')

        org_name = soup.find(class_='firstHeader').text
        adress = soup.find(class_="contactBox_right").find(class_='firm_link').text
        good_review = soup.find(class_='good_review').text
        bad_review = soup.find(class_='bad_review').text
        phone_list = []

        image_links = soup.find(class_='contactBox_left general_info').find_all('img')
        sleep_req()
        for image in image_links:
            url = f'http:{image.get("src")}'
            req = requests.get(url, headers=headers)
            with open('ph.svg', 'wb') as file:
                file.write(req.content)

            drawing = svg2rlg("ph.svg")
            renderPM.drawToFile(drawing, "ph.png", fmt="PNG")

            image_path = 'ph.png'

            reader = easyocr.Reader(['ru'])
            phone_list.append(reader.readtext(image_path, detail=0)[0])


        card_dict = {
            'org_name': org_name,
            'adress' : adress,
            'good_review': good_review,
            'bad_review': bad_review,
            'phones': phone_list
        }
        card_json.append(card_dict)
        sleep_req()
    with open(f'data/{i}.json', 'w', encoding='UTF-8') as file:
        json.dump(card_json, file, indent=4, ensure_ascii=False)
    i += 1



