from flask import Flask
from flask_jsonrpc import JSONRPC
import urllib.parse
import json

import wikipedia

app = Flask(__name__)

rpc = JSONRPC(app, '/', enable_web_browsable_api=True)


@app.route('/wiki')
@rpc.method('/api/wiki')
def wiki(query: str) -> str:
    wikipedia.set_lang('en')
    resultContainer = {}

    result = wikipedia.page(
        urllib.parse.quote(
            wikipedia.search(query)[0]
        ))

    for attribute in dir(result):
        if not attribute.startswith('_'):
            try:
                classAttr = result.__getattribute__(attribute)
                if isinstance(classAttr, str):
                    resultContainer[attribute] = classAttr
            except KeyError:
                continue
            except AttributeError:
                continue

    return json.dumps(resultContainer)
