import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

def download_font(url):
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,uk-UA;q=0.8,uk;q=0.7,ru;q=0.6",
    "Connection": "keep-alive",
    "Host": "fonts3.bj.bcebos.com",
    "Purpose": "prefetch",
    "Referer": "http://fonts3.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    filename = url.split("/")[-1]
    with open(filename, "wb") as file:
        file.write(response.content)

def get_font_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if soup.find_all("a", class_="downlist"):
        href = soup.find("a", class_="downlist").get("href")
        return href


def get_font_page_links(url):
    base_url = 'http://fonts3.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    font_links = []
    for link in soup.find_all("a", class_="dl"):
        href = link.get("href")
        font_links.append(urllib.parse.urljoin(base_url, href))
    return font_links

def pages_total(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if soup.find_all("div", class_="list_page"):
        pages_num = soup.find("div", class_="list_page").text.split('/')[-1]
        return int(pages_num)

def download_fonts_from_url(url):
    pages_num = pages_total(url)
    for i in range(1,pages_num+1):
        font_links = get_font_page_links(url + str(i))
        print(url + str(i))
        for font_page_link in font_links:
            font_link = get_font_link(font_page_link)
            print("Downloading:", font_link)
            download_font(font_link)

# Посилання на сторінку зі шрифтами
url = "http://fonts3.com/search/?/HelveticaNeueLTW1G/"

# Створення папки для збереження шрифтів
folder_name = url.rstrip('/').split("/")[-1]
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
os.chdir(folder_name)

download_fonts_from_url(url)

print("All fonts downloaded successfully.")
