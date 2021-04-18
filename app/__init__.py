from flask import Flask
from config import Config 
from flask_migrate import Migrate

migrate = Migrate()

# Create and Return a Flask app with its extensions and blueprints
def create_app(config_filename=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_filename)

    with app.app_context():
        # Method for Register/Init Extensions
        register_extensions(app)

        import app.extensions as ex
        migrate.init_app(app, ex.db,render_as_batch=True)
        # Register Blueprints
        register_blueprints(app)

    return app

# Method for Register/Init Extensions
def register_extensions(app):
    import app.extensions as ex
    ex.db.init_app(app)
    ex.bcrypt.init_app(app)
    ex.login_manager.init_app(app)
    ex.mail.init_app(app)
# Method for Register Blueprints
def register_blueprints(app):
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)