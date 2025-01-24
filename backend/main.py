from flask import Flask, jsonify
from flask_restx import Api
from app.api import api_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Inisialisasi Api
api = Api(app, version='1.0', title='Analisis Sentimen API',
          description='API untuk KNN dan preprocessing')
# Register Blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
