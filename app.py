import os
import sys
import logging
import datetime

import setting
from setting import ROOT_DIR

from flask import Flask, render_template, jsonify, request
from celery import Celery

from util import logger, get_tree, get_element_short_text
from util import g_cursor as db

app = Flask(__name__)
app.config.from_object(setting)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name='celery_task_add')
def celery_task_add(x, y):
    return x + y

@app.route('/test')
def add(x=1, y=2):
    x = int(request.args.get('x', x))
    y = int(request.args.get('y', y))
    res = celery_task_add.apply_async((x, y))
    result = {
        'id': res.task_id,
        'x': x,
        'y': y
    }
    return jsonify(result)

@app.route('/test/<task_id>')
def show_result(task_id):
    r = celery_task_add.AsyncResult(task_id)
    retval = 'Not ready'
    if r.ready():
        retval = r.get(timeout=1.0)
    return repr(retval)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog/index.html')

@app.route('/blog/<int:year>/<int:month>/<int:day>/<title>')
def blog_article(year, month, day, title):
    created = datetime.datetime(year, month, day)
    para = {
        'created': created,
        'created_next_day': created+datetime.timedelta(days=1),
        'title': title
    }
    logger.info('SELECT * FROM blog WHERE created >= %(created)s and created < %(created_next_day)s and title = %(title)s' % para)
    db.execute('SELECT * FROM blog WHERE created >= %(created)s and created < %(created_next_day)s and title = %(title)s', para)
    r = db.fetchall()
    for i in r:
        i['source_file'] = os.path.join('blog', i['source_file']+'.html')
    if r:
        para = {
            'data': r
        }
        return render_template('blog/article.html', **para)
    else:
        return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/test2')
def test2():
    url = 'http://getbootstrap.com/'
    tree = get_tree(url)
    e = tree.xpath('//div[@class="bs-docs-featurette"]/div[@class="container"]')[0]
    short_text = get_element_short_text(e)
    return short_text

if __name__ == '__main__':
    from flask import send_from_directory

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    @app.route('/bootstrap/<path:path>')
    def send_bootstrap(path):
        return send_from_directory('static/bootstrap', path)

    @app.route('/font-awesome/<path:path>')
    def send_font_awesome(path):
        return send_from_directory('static/font-awesome', path)

    @app.route('/leaflet/<path:path>')
    def send_leaflet(path):
        return send_from_directory('static/leaflet', path)

    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('static/css', path)

    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('static/js', path)

    @app.route('/js/vendor/<path:path>')
    def send_js_vendor(path):
        return send_from_directory('static/js/vendor', path)

    @app.route('/img/<path:path>')
    def send_img(path):
        return send_from_directory('static/img', path)

    @app.route('/doc/<path:path>')
    def send_doc(path):
        return send_from_directory('static/doc', path)
    app.run(host='127.0.0.1', port=8080, debug=True)
else:
    logging.basicConfig(stream=sys.stderr)
