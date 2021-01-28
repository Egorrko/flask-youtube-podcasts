from flask import Flask, render_template, request, redirect
import youtube

app = Flask(__name__)


@app.route('/')
def index():
    podcasts = youtube.get()
    return render_template('podcasts.html', podcasts=podcasts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    link = None
    result = None
    if request.method == 'POST' and 'link' in request.form:
        link = request.form['link']
        result = youtube.download(link)
        if result:
            return redirect("/")
        else:
            result = 'Ошибка загрузки. Проверьте ссылку'
    return render_template('add.html', error=result)


if __name__ == '__main__':
    app.run(debug=True)
