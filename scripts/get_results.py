from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from scrapping import step, workflow, download, parse, extract_table

@step
def extract_urls(soup):
    new_links = soup.find('section', {'id': 'page-content'}) \
        .find('div', {'class': 'view-content'}) \
        .find_all('a')
    return set([urljoin('http://www.tesoro.es', x.attrs['href']) for x in new_links])

@step
def next_page(soup):
    current_page = soup.find('section', {'id': 'page-content'}) \
        .find('ul', {'class': 'pagination'}) \
        .find('li', {'class': 'active'})
    if 'last' in current_page['class']:
        return None
    else:
        return urljoin('http://www.tesoro.es', current_page.find_next('li').find('a').attrs['href'])

@workflow
def get_results_government_bonds():
    base_url = 'http://www.tesoro.es/en/deuda-publica/subastas/resultados-subastas-anteriores?type=bonos_del_estado'
    urls = set()
    while base_url:
        html = download(base_url)
        soup = parse(html)
        urls |= extract_urls(soup)
        base_url = next_page(soup)

    datas = []
    for url in urls:
        html = download(url)
        soup = parse(html)
        data = extract_table(soup)
        datas.append(data)
    
    return datas

@workflow
def get_results_government_obligations():
    base_url = 'http://www.tesoro.es/en/deuda-publica/subastas/resultados-subastas-anteriores?type=bonos_del_estado'
    urls = set()
    while base_url:
        html = download(base_url)
        soup = parse(html)
        urls |= extract_urls(soup)
        base_url = next_page(soup)

    datas = []
    for url in urls:
        html = download(url)
        soup = parse(html)
        data = extract_table(soup)
        datas.append(data)
    
    return datas

@workflow
def get_results_index_bond():
    base_url = 'http://www.tesoro.es/en/deuda-publica/subastas/resultados-subastas-anteriores?type=bonos_y_obligaciones_indexados'
    urls = set()
    while base_url:
        html = download(base_url)
        soup = parse(html)
        urls |= extract_urls(soup)
        base_url = next_page(soup)

    datas = []
    for url in urls:
        html = download(url)
        soup = parse(html)
        data = extract_table(soup)
        datas.append(data)

    return datas

@workflow
def get_results_liquidities():
    base_url = 'http://www.tesoro.es/en/deuda-publica/subastas/resultados-subastas-anteriores?type=subastas_de_liquidez'
    urls = set()
    while base_url:
        html = download(base_url)
        soup = parse(html)
        urls |= extract_urls(soup)
        base_url = next_page(soup)

    datas = []
    for url in urls:
        html = download(url)
        soup = parse(html)
        data = extract_table(soup)
        datas.append(data)
    
    return datas

@workflow
def get_results_treasury_letters():
    base_url = 'http://www.tesoro.es/en/deuda-publica/subastas/resultados-subastas-anteriores?type=letras_del_tesoro'
    urls = set()
    while base_url:
        html = download(base_url)
        soup = parse(html)
        urls |= extract_urls(soup)
        base_url = next_page(soup)

    datas = []
    for url in urls:
        html = download(url)
        soup = parse(html)
        data = extract_table(soup)
        datas.append(data)
    
    return datas

if __name__ == '__main__':
    err, data = get_results_government_bonds()
    err, data = get_results_government_obligations()
    err, data = get_results_index_bond()
    err, data = get_results_liquidities()
    err, data = get_results_treasury_letters()