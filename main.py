import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.assessment import Assessment, LibraryContent, NewsletterSubscription
from src.routes.user import user_bp
from src.routes.assessment import assessment_bp
from src.routes.ai_query import ai_query_bp
from src.routes.voice_cloning import voice_cloning_bp
from src.routes.speech_generation import speech_generation_bp
from src.routes.lead_magnet import lead_magnet_bp
from src.routes.newsletter import newsletter_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for frontend communication
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(assessment_bp, url_prefix='/api')
app.register_blueprint(ai_query_bp, url_prefix='/api')
app.register_blueprint(voice_cloning_bp, url_prefix='/api/voice-cloning')
app.register_blueprint(speech_generation_bp, url_prefix='/api/voice-cloning')
app.register_blueprint(lead_magnet_bp)
app.register_blueprint(newsletter_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
