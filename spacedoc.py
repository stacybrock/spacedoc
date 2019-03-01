import flask
from flask import g
import wikicore

app = flask.Flask(__name__)

@app.before_request
def before_request():
    if 'wiki' not in g:
        g.wiki = wikicore.Wiki('/tmp/wiki-test')


@app.route('/')
def index():
    return flask.redirect('/wiki', code=302)


@app.route('/wiki')
def view_wiki_index():
    page = g.wiki.get_page('index.md')
    if page is not None:
        return page.render_html(linkroot='/wiki')
    else:
        pass #TODO


@app.route('/wiki/<path:pagepath>')
def view_page(pagepath):
    page = g.wiki.get_page(pagepath)
    if page is not None:
        return page.render_html(linkroot='/wiki')
    else:
        pass #TODO


@app.teardown_appcontext
def teardown_app(error):
    g.wiki.__del__()


if __name__ == '__main__':
    app.run(debug=True)
