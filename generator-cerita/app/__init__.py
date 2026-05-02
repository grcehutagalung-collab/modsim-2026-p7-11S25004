from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.extensions import Base, engine
from app.routes.story_routes import story_bp

def create_app():
    app = Flask(__name__, static_folder="../static", static_url_path="/static")
    app.config.from_object(Config)

    CORS(app)

    # Buat tabel database
    Base.metadata.create_all(bind=engine)

    # Daftarkan blueprint
    app.register_blueprint(story_bp)

    @app.route("/")
    def index():
        return jsonify({"message": "Generator Cerita Pendek API berjalan!", "version": "1.0"})

    return app
