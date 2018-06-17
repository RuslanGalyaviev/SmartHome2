from bs4 import BeautifulSoup
import requests




def get_html(url):
    r = requests.get(url)
    return r.text

def get_temperature(html):
    soup = BeautifulSoup(html, 'lxml')
    temperature = soup.find('div', class_="temp-and-cloudiness-cont").find('p', class_='temperature').text
    return temperature


def temp():
    html = "http://kazan.ru/pogoda"
    result = get_temperature(get_html(html))
    return result
