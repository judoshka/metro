import requests
from bs4 import BeautifulSoup
from datetime import date
from models import DB, Post

BASE_URL = "https://mosmetro.ru"


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None


def get_date(url):
    content = get_html(url)
    soup = BeautifulSoup(content, 'html.parser')
    date_string = soup.select_one("div[class='pagetitle__content-date']")
    if date_string:
        return date_string.text
    else:
        return None


def parse(markup, last_news_number):
    date_values = {
        'Января': 1,
        'Февраля': 2,
        'Марта': 3,
        'Апреля': 4,
        'Мая': 5,
        'Июня': 6,
        'Июля': 7,
        'Августа': 8,
        'Сентября': 9,
        'Октября': 10,
        'Ноября': 11,
        'Декабря': 12
    }
    data = markup.find_all(class_="newslist__list-item")
    for i in data:
        href = i.find("a")["href"]
        href = BASE_URL + href

        news_number = int(href.split("/")[-2])
        news = Post.query.filter(Post.news_number == news_number).first()
        if news:
            break
        if last_news_number >= news_number:  # новые новости закончились
            break

        image_url = i.find("img")["src"]
        image_url = BASE_URL + image_url

        title = i.select_one("span[class='newslist__text-title']").text

        published_date = get_date(href)
        if not published_date:   # новость https://mosmetro.ru/press/news/4068/ не кликабельна
            continue
        day, month, year = published_date.split()
        day = int(day)
        month = date_values.get(month)
        year = int(year)
        published_date = date(year, month, day)

        scraped_date = date.today()

        DB.session.add(Post(news_number, title, image_url, href, published_date, scraped_date))
    DB.session.commit()


def scrape_data(app):
    with app.app_context():
        records = Post.query.all()
        last_record_id = max([i.news_number for i in records]) if records else 0
        search_url = BASE_URL + '/press/news/'
        content = get_html(search_url)
        soup = BeautifulSoup(content, 'html.parser')
        parse(soup, last_news_number=last_record_id)


if __name__ == '__main__':
    scrape_data()
