import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # The database will be stored in the directory mounted by gcsfuse
    # We'll assume the mount point is /mnt/gcs_bucket
    MNT_DIR = os.environ.get('MNT_DIR', '/mnt/gcs_bucket')
    DB_NAME = os.environ.get('DB_NAME', 'blog.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{MNT_DIR}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    NANO_BANANA_API_KEY = os.environ.get('NANO_BANANA_API_KEY')
