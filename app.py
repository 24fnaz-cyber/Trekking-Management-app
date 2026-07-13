from flask import Flask, render_template
from werkzeug.security import generate_password_hash
from config import Config
from models import db, User
from flask_login import LoginManager

from auth import auth
from views import views

def create_app():       
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
        return User.query.get(int(id))   

    with app.app_context():
        db.create_all()

        admin_exists = User.query.filter_by(role = 'admin').first()
        if not admin_exists:
            print("No admin exists. Creating default admin account...")  
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

    return app   

app = create_app()
#print(app.url_map)

with app.app_context():
    users = User.query.all()

    
    db.session.commit()
    print("Roles updated successfully!")




if __name__ == "__main__":
    app.run(debug = True)