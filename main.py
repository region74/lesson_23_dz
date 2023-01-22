from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import datetime
from hh_api import get_info

app = Flask(__name__)


# TODO баги с корректностью поиска, проверить api (не смотрел, но вроде +- норм).
#  Навести красоту на выводе, чтобы таблицей было все либо как то f строкой хз.(в светлом будущем, пока дальше пойдем)

@app.route("/")
def index():
    return render_template('index.html')


@app.get('/form/')
def form_get():
    return render_template('form.html')


@app.get('/result/')
def form_result():
    return render_template('result.html')


@app.post('/result/')
def form_post():
    text = request.form['text']
    result = get_info(text)
    return render_template('result.html', data=result)


if __name__ == "__main__":
    app.run(debug=True)
