import os 
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600 #1HR
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

    # Google OAuth2 config
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    # Use environment variable for redirect URI, fallback to production URL
    GOOGLE_REDIRECT_URI = os.getenv("https://dunamasgame.vercel.app/google/authorized")
