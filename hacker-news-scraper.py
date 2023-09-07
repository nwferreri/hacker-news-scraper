# Scrapes the first 3 pages of Hacker News for the top stories
# Filters for stories with 100 or more votes and displays them

# Import libraries
import requests
from bs4 import BeautifulSoup
import pprint


# Setup
url = 'https://news.ycombinator.com/news?p='
all_links = []
all_subtext = []

# Aggregate the first 3 pages of Hacker News articles
for page in range(1, 3):
    res = requests.get(f'{url}{page}')
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.titleline > a')
    subtext = soup.select('.subtext')
    all_links.extend(links)
    all_subtext.extend(subtext)


def sort_stories_by_votes(hnlist):
    '''
    Sorts the list of Hacker News articles by votes, descending
    '''
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    '''
    Extracts article titles, links, and votes,
    filters for 100 or more votes,
    and creates a dictionary of the information
    '''
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


# Output
pprint.pprint(create_custom_hn(all_links, all_subtext))
