from flask import Flask, send_from_directory, render_template
from pathlib import Path
from .config import Config

app = Flask(__name__, static_folder=Config.STATIC_PATH,
            template_folder=Config.TEMPLATE_PATH)
app.config.from_object(Config)


# Catch all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path and Path.exists(Path(str(Config.TEMPLATE_PATH) + path)):
        return send_from_directory(Config.TEMPLATE_PATH, path)
    return render_template('index.html')
