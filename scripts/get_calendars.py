import requests
from bs4 import BeautifulSoup
from scrapping import workflow, download, parse, extract_table

@workflow
def get_calendar_bonds_and_obligations():
    url = 'http://www.tesoro.es/en/deuda-publica/subastas/calendario/bonos-y-obligacionesEN'
    html = download(url)
    soup = parse(html)
    data = extract_table(soup)
    return data

@workflow
def get_calendar_treasury_letters():
    url = 'http://www.tesoro.es/en/deuda-publica/subastas/calendario/letras-del-tesoroen'
    html = download(url)
    soup = parse(html)
    data = extract_table(soup)
    return data

if __name__ == '__main__':
    err, data = get_calendar_bonds_and_obligations()
    err, data = get_calendar_treasury_letters()