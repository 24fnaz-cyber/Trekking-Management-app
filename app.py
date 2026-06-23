from flask import Flask, render_template
from config import Config
from models import db

def create_app():         #function to configure
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app   #returning the flask app

app = create_app()
print(app.url_map)

@app.route('/')
def start():
    return render_template('index.html')



if __name__ == "__main__":
    #app = create_app()   # this is in our global scope 
    app.run(debug = True)