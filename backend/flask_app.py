from flask import (Flask, send_from_directory, render_template,
                   render_template_string)
from pathlib import Path
from .config import Config
from .machine_learning.mnist.testMnist import test_mnist

app = Flask(__name__, static_folder=Config.STATIC_PATH,
            template_folder=Config.TEMPLATE_PATH)
app.config.from_object(Config)


# Test mnist predict
@app.route('/test')
def test_ml():
    result = test_mnist()
    print(result)
    template_str = '''
    <h1>Result</h1>
    <p>Value: {{value}}</p>
    <img src={{img}} alt={{value}} height="42" width="42">
    '''

    return render_template_string(template_str, value=str(result))


# Catch all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path and Path.exists(Path(str(Config.TEMPLATE_PATH) + path)):
        return send_from_directory(Config.TEMPLATE_PATH, path)
    return render_template('index.html')
