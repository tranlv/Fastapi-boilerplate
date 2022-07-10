from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


__author__ = ""
__maintainer__ = ""
__email__ = ""
__copyright__ = ""



engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
