from flask import Flask
from flask_migrate import Migrate
from src.config import Config
from src.db.core import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Init db
    db.init_app(app)
    migrate = Migrate(app, db)


    with app.app_context():
        # Import models
        from src.db.models.quiz_db import User, Questions, Options, Answers, Response
    

        # Import blueprints
        from src.api.models.quiz_route import quiz_bp
        from src.api.models.demoRun import demo_bp
        from src.api.models.practiceQuiz import practice_bp
        from src.api.models.questionBank import comprehensive_bp
        from src.api.auth.auth import auth_bp, google_bp

        # register blueprints
        app.register_blueprint(quiz_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(demo_bp)
        app.register_blueprint(practice_bp)
        app.register_blueprint(comprehensive_bp)
        app.register_blueprint(google_bp)


    return app

app=create_app()

if __name__ == '__main__':
    app.run(debug=True)