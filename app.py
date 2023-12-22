from flask import Flask, render_template
from database.news_information import fetch_news_information

app = Flask(__name__)

@app.route('/')
def index():
    # database.py에서 정의된 함수를 사용하여 뉴스 정보를 가져옴
    news_items = fetch_news_information()
    return render_template('it_science.html', news_items=news_items)

if __name__ == '__main__':
    app.run(debug=True)