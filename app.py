from flask_apscheduler import APScheduler
from flask import Flask, request, Response, jsonify
from scrape import scrape_data
from datetime import date, timedelta
from models import DB, Post, DATABASE_URI


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JSON_AS_ASCII'] = False
    with app.app_context():
        DB.init_app(app)
    cron = APScheduler()
    cron.init_app(app)
    cron.add_job(id='scraper', func=scrape_data, trigger='interval', seconds=10, args=(app,))
    cron.start()

    @app.route('/metro/news')
    def show_news():
        args = request.args
        key = "day"
        if "day" in args and len(request.args) < 2:
            value = args.get("day", type=int)
            if isinstance(value, int):
                response_date = date.today() - timedelta(days=value)
                posts = Post.query.filter(Post.published_date > response_date)
                response = [{
                    'title': post.title,
                    'news_url': post.news_url,
                    'image_url': post.image_url,
                    'published_date': post.published_date.strftime("%Y-%m-%d")
                    }
                    for post in posts
                ]
                return Response(jsonify(response).data)
            else:
                return Response("Incorrect day. Try /metro/news?day=5", 403)
        else:
            return Response("Incorrect query. Try /metro/news?day=5", 403)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    with app.app_context():
        DB.create_all()

    return app


if __name__ == '__main__':
    APP = create_app()
    APP.run(host="0.0.0.0", debug=True, port=5010)
