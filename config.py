import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "blocera-gizli-anahtar")

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "sqlite:///blocera.db"
    )

    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

    AI_PROVIDER = os.environ.get(
        "AI_PROVIDER",
        "groq"
    )

    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        "Sen BLOCERA'nın yapay zeka asistanısın."
    )

    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS",
        "*"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

print("GROQ KONTROL:", Config.GROQ_API_KEY[:10])