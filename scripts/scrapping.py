from typing import Any, List
import requests
from bs4 import BeautifulSoup

class ScrappingException(Exception):
    pass

def workflow(f):
    def g(*args, **kwargs):
        try:
            err = None
            data = f(*args, **kwargs)
            return [err, data]
        except ScrappingException as e:
            err = 'Error in the workflow "{}", {}'.format(f.__name__, e)
            data = None
            return [err, data]
    return g

def step(f):
    def g(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ScrappingException as e:
            raise ScrappingException('at the step "{}, {}'.format(f.__name__, e))
        except Exception as e:
            raise ScrappingException('at the step "{}": {} {}'.format(f.__name__, type(e), e))
    return g

@step
def download(url: str) -> str:
    """Downloads the HTML code hosted at url"""
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception('Server returned status code {}'.format(res.status_code))
    return res.text

@step
def parse(html: str) -> Any:
    """Takes the HTML/text version of the DOM and returns a structured
    python object of the DOM"""
    return BeautifulSoup(html, 'html.parser')

# TODO: mouve this code in the transformation part
# @step
# def check_data_table(data: List[List[Any]]) -> bool:
#     """Checks if all the rows of a two-dimensional array have the same
#     number of columns as the header"""
#     len_header = len(data[0])
#     for line in data[1:]:
#         if len(line) != len_header:
#             raise Exception('{} columns expected but found {} at this line: {}'.format(
#                 len_header, len(line), line))

#----------------------------------------------------------------------#
# Project-specific code                                                #
#----------------------------------------------------------------------#

@step
def extract_table(soup):
    # find the table with the data
    raw_table = soup \
        .find('section', {'id': 'page-content'}) \
        .find_all('table')[0]
    
    # find the name of the columns
    header = raw_table.find('thead').find_all('th')
    header = [x.text.strip() for x in header]

    # find the data in the lines
    lines = raw_table.find('tbody').find_all('tr')
    lines = [[cell.text.strip() for cell in line.find_all('td')] for line in lines]

    return [header] + lines