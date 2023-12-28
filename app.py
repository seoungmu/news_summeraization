from flask import Flask, render_template, request
from database.news_information import fetch_news_information, get_news_by_genre, get_total_news_count

app = Flask(__name__)

@app.route('/')
def index():
    genres = ['정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '연예']
    return render_template('home.html', genres=genres)

@app.route('/news/<genre>')
@app.route('/news/<genre>/<int:page>')
def show_news(genre, page=1):
    genre = genre.replace('_', '/')
    per_page = request.args.get('per_page', default=20, type=int)
    search_query = request.args.get('search_query', '')
    total_news_count = get_total_news_count(genre)
    total_pages = (total_news_count + per_page - 1) // per_page
    news_items = get_news_by_genre(genre, page, per_page, search_query)
    genre = genre.replace('/', '_')
    genres = ['정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '연예']
    page_range = 10
    start_page = max(1, ((page - 1) // page_range) * page_range + 1)
    end_page = min(start_page + page_range - 1, total_pages)

    return render_template('news.html', news_items=news_items, current_genre=genre, genres=genres, page=page, per_page=per_page, total_pages=total_pages, start_page=start_page, end_page=end_page)


if __name__ == '__main__':
    app.run(debug=True)