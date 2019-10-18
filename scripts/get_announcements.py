from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from scrapping import step, workflow, download, parse, extract_table

@step
def extract_urls(soup):
    new_links = soup.find('section', {'id': 'page-content'}) \
        .find('div', {'class': 'view-content'}) \
        .find_all('a')
    
    texts = [x.text for x in new_links]
    urls = [urljoin('http://www.tesoro.es', x.attrs['href']) for x in new_links]
 
    def keep(text):
        if 'announces' in text:
            return True
        return False

    return set([url for text, url in zip(texts, urls) if keep(text)])

@workflow
def get_announcements():
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
    # err, data = get_announcements()
    # if err:    
    #     print(err)
    # else:
    #     print(data)