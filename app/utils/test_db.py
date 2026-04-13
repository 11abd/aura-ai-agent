from sqlalchemy import create_engine
from app.config.settings import settings

engine = create_engine(settings.DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ DB Connected successfully!")
except Exception as e:
    print("❌ DB Connection failed:", e)
    