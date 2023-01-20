from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import datetime
from hh_api import get_info

app = Flask(__name__)


# TODO баги с корректностью поиска, проверить api. С базы он выводит все, даже что не искалось в данный момент
#  (там типо в момент выгрузки из БД он по запросу получается тянет все, надо поправить эту тему, либо сменить логику обработки).
#  Навести красоту на выводе, чтобы таблицей было все либо как то f строкой хз.

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
