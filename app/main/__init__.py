from flask import Blueprint
from werkzeug.utils import secure_filename


bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads/companies'
ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'xlsx'}

from app.main import routes