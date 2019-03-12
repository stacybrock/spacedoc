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
        wikicore.WikiPage.wiki = g.wiki
    g.wiki_name = app.config['WIKI_NAME']


@app.route('/')
def index():
    return flask.redirect(f"{app.config['WIKI_ROOT']}/index", code=302)


@app.teardown_appcontext
def teardown_app(error):
    g.wiki.close()


if __name__ == '__main__':
    app.run(debug=True)
