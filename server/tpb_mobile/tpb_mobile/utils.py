from tpb import CATEGORIES
from bs4 import BeautifulSoup
import urllib2

def match_category(category_name):
    '''
    returns the category class that matches category_name
    '''
    if category_name == "ALL":
        to_return = CATEGORIES.ALL
    elif category_name == "AUDIO":
        to_return = CATEGORIES.AUDIO
    elif category_name == "VIDEO":
        to_return = CATEGORIES.VIDEO
    elif category_name == "APPLICATIONS":
        to_return = CATEGORIES.APPLICATIONS
    elif category_name == "GAMES":
        to_return = CATEGORIES.GAMES
    elif category_name == "OTHER":
        to_return = CATEGORIES.OTHER
    else:
        to_return = None
    return to_return

def parse_torrent_page(url):
    '''
    parses the page for an individual torrent and returns:
    title, type, size, description
    '''
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    
    dd_list = soup.find_all('dd')
    
    result = {}
    result['title'] = soup.find(id="title").string
    result['description'] = soup.find('pre').getText()
    result['type'] = dd_list[0].string
    result['size'] = dd_list[2].string
    
    return result
