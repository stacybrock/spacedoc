import flask
import wikicore
from flask import g
from blueprints.wikirenderer import wikirenderer

# create Flask app
app = flask.Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')
app.register_blueprint(wikirenderer, url_prefix=app.config['WIKI_ROOT'])
#app.config['EXPLAIN_TEMPLATE_LOADING'] = True


@app.before_request
def before_request():
    if 'wiki' not in g:
        g.wiki = wikicore.Wiki(app.config['WIKI_REPO_DIR'],
                               base_path=app.config['WIKI_ROOT'])
        if app.config['ASCIIDOC_PY3']:
            g.wiki.init_asciidoc(app.config['ASCIIDOC_PY3'])
        wikicore.WikiPage.wiki = g.wiki

    g.wiki_name = app.config['WIKI_NAME']


@app.route('/')
def index():
    return flask.redirect(f"{app.config['WIKI_ROOT']}/index", code=302)


@app.route('/search', methods=['POST'])
def search():
    searchterm = ''
    results = []

    if 'searchterm' in flask.request.form:
        searchterm = flask.request.form['searchterm']
        results = g.wiki.search(searchterm, case_insensitive=True)

    return flask.render_template('default/search.html',
                                 searchterm=searchterm, results=results)


@app.teardown_appcontext
def teardown_app(error):
    g.wiki.close()


if __name__ == '__main__':
    app.run(debug=True)
