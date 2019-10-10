import requests
from bs4 import BeautifulSoup
from scrapping import workflow, download, parse, extract_table

@step
def extract_urls(soup):
    # TODO
    # new_links = soup.find('section', {'id': 'page-content'}) \
    #     .find('div', {'class': 'view-content'}) \
    #     .find_all('a')
    # return set([urljoin('http://www.tesoro.es', x.attrs['href']) for x in new_links])

@workflow
def get_calendar_treasury_letters():
    url = 'http://www.tesoro.es/en/deuda-publica'
    html = download(url)
    soup = parse(html)
    urls = extract_urls(soup)

    datas = []
    for url in urls:
        html = download(url)
        soup = parse(html)
        data = extract_table(soup)
        datas.append(data)
    
    return datas

if __name__ == '__main__':
    # err, data = get_calendar_bonds_and_obligations()
    # err, data = get_calendar_treasury_letters()
    # if err:    
    #     print(err)
    # else:
    #     print(data)