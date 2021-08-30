from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class Post(DB.Model):
    __tablename__ = "post"
    published_id = DB.Column(DB.Integer, primary_key=True)
    news_number = DB.Column(DB.Integer, unique=True)
    title = DB.Column(DB.String(80), nullable=False)
    image_url = DB.Column(DB.String(255), nullable=False)
    news_url = DB.Column(DB.String(255), nullable=False)
    published_date = DB.Column(DB.Date, nullable=False)
    scraped_date = DB.Column(DB.Date, nullable=False)

    def __init__(self, news_number, title, image_url, news_url, published_date, scraped_date):
        self.news_number = news_number
        self.title = title
        self.image_url = image_url
        self.published_date = published_date
        self.news_url = news_url
        self.scraped_date = scraped_date

    def __str__(self):
        return f'title: {self.title}\n URL: {self.news_url}'