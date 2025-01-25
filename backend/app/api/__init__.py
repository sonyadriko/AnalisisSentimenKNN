from flask import Blueprint
from flask_restx import Api

# Create Blueprint
api_bp = Blueprint('api', __name__)
api = Api(
    api_bp,
    version='1.0',
    title='Analisis Sentimen API',
    description='API untuk analisis sentimen menggunakan metode KNN',
    doc='/swagger'  # Swagger aktif di /api/swagger
)


# Import namespaces
from .knn import knn_ns
from .preprocessing import preprocessing_ns
from .tfidf import tfidf_ns
from .metrics import metrics_ns
from .data_training import data_training_ns

# Add namespaces
api.add_namespace(knn_ns, path='/knn')
api.add_namespace(preprocessing_ns, path='/preprocessing')
api.add_namespace(tfidf_ns, path='/tfidf')
api.add_namespace(metrics_ns, path='/metrics')
api.add_namespace(data_training_ns, path='/data-training')