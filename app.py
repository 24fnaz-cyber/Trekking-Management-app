from flask import Flask, render_template
from werkzeug.security import generate_password_hash
from config import Config
from models import db, User
from flask_login import LoginManager

from auth import auth
from views import views

def create_app():         #function to configure
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
     #initializing bluprint
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))   #flask or cookie based unique authentication

    with app.app_context():
        db.create_all()

        admin_exists = User.query.filter_by(role = 'admin').first()
        if not admin_exists:
            print("No admin exists. Creating default admin account...")  #this showup in terminal
            password = 'adminpassword'
            hashed_password = generate_password_hash(password)
            default_admin = User(
                username = 'admin',
                password = hashed_password,
                role = 'admin'
            )
            db.session.add(default_admin)
            db.session.commit()
            print("Admin created successfully.")

    return app   #returning the flask app

app = create_app()
#print(app.url_map)

@app.route('/')
def start():
    return render_template('index.html')

with app.app_context():
    users = User.query.all()

    
    db.session.commit()
    print("Roles updated successfully!")



if __name__ == "__main__":
    #app = create_app()   # this is in our global scope 
    app.run(debug = True)