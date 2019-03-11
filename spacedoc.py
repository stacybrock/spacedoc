import flask
import wikicore
from flask import g

# create Flask app
app = flask.Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')


@app.before_request
def before_request():
    if 'wiki' not in g:
        g.wiki = wikicore.Wiki(app.config['WIKI_REPO_DIR'], base_path='/page')
        wikicore.WikiPage.wiki = g.wiki


@app.route('/')
def index():
    return flask.redirect('/page/index', code=302)


@app.route('/page/index')
def view_wiki_index():
    return view_page('index.md')


@app.route('/page/<path:pagepath>')
def view_page(pagepath):
    page = g.wiki.get_page(pagepath)
    if page is not None:
        return page.to_html()
    else:
        pass #TODO


@app.teardown_appcontext
def teardown_app(error):
    g.wiki.close()


if __name__ == '__main__':
    app.run(debug=True)
