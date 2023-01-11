from flask import Flask

from services.dictionary import Dictionary
from services.get import Get
from services.search import Search
from services.bookmark import Bookmark

app = Flask(__name__)


@app.route('/')
def index():
    return "App is up and running"

@app.route('/dictionary')
async def get_meaning():
    return await Dictionary().get_meaning()


@app.route('/get')
def store_paragraph():
    return Get().store_paragraph()

@app.route('/search', methods = ['POST'])
def search_paragraph():
    return Search().search_paragraph()

@app.route('/bookmark', methods = ['POST', 'GET'])
def bookmark_paragraph():
    return Bookmark().bookmark_paragraph()
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)