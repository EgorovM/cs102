import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    new_divs = parser.find_all("tr", {"class" : "athing"})
    stat_divs =  parser.find_all("td", {"class" : "subtext"})

    for ind, new_div in enumerate(new_divs):
        author_item = new_div.find("span", {"class" : "sitestr"})
        author = author_item.text if author_item else ""

        comments_item = stat_divs[ind].find_all("a")[-1].text.split()
        comments = comments_item[0] if len(comments_item) == 2 else 0

        points = int(stat_divs[ind].find("span", {"class" : "score"}).text.split()[0])
        title = new_div.find("a", {"class": "storylink"}).text
        url = new_div.find("a", {"class": "storylink"})["href"]

        if len(url.split(".")) == 1:
            url = "https://news.ycombinator.com/" + url

        news_list.append(
            {
                "author" : author,
                "comments" : comments,
                "points" : points,
                "title" : title,
                "url" : url
            }
        )

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """

    return parser.find('a', {"class": "morelink"})["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []

    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1

    return news
