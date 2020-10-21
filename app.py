from flask import Flask
from flask_jsonrpc import JSONRPC
import json

from wikipedia import wikipedia

app = Flask(__name__)

rpc = JSONRPC(app, '/', enable_web_browsable_api=True)


@app.route('/wiki')
@rpc.method('/api/wiki')
def wiki(query: str) -> str:
    wikipedia.set_lang('en')
    search = wikipedia.search(query)[0]
    return json.dumps(
        filterResult(
            wikipedia.page(
                None, search['pageid']
            )))


@app.route('/wiki/title')
@rpc.method('/wiki/title')
def wikiByTitle(query: str) -> str:
    wikipedia.set_lang('en')
    search = wikipedia.search(query)[0]
    return json.dumps(
        filterResult(
            wikipedia.page(
                search['title']
            )))


@app.route('/geo')
@rpc.method('/api/geo')
def geo(lat: float, lon: float) -> str:
    wikipedia.set_lang('en')
    return json.dumps(
        filterResult(
            wikipedia.page(
                wikipedia.geosearch(lat, lon))))


def filterResult(result: wikipedia.WikipediaPage):
    resultContainer = {}
    for attribute in dir(result):
        if not attribute.startswith('-'):
            try:
                classAttr = result.__getattribute__(attribute)
                if isinstance(classAttr, str):
                    resultContainer[attribute] = classAttr
            except KeyError:
                continue
            except AttributeError:
                continue
    return resultContainer
