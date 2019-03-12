from flask import Blueprint, render_template, abort, g, Markup
from jinja2 import TemplateNotFound

wikirenderer = Blueprint('renderer', __name__)

@wikirenderer.route('/')
@wikirenderer.route('/index')
def view_index():
    return view_page('index.md')


@wikirenderer.route('/<path:pagepath>')
def view_page(pagepath):
    page = g.wiki.get_page(pagepath)
    page_content = Markup(page.to_html())
    try:
        return render_template('default/page.html', content=page_content,
                               title=pagepath)
    except TemplateNotFound:
        abort(404)
