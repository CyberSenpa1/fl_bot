from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from os import getenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Проверка переменной окружения
DATABASE_URL = getenv("URL_ALCHEMY")
if not DATABASE_URL:
    raise ValueError("Environment variable 'URL_ALCHEMY' is not set or empty.")

# Создание движка
engine = create_async_engine(DATABASE_URL)

# Создание sessionmaker для работы с асинхронными сессиями
AsyncSessionMaker = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Декларативная база данных
Base = declarative_base()

# Модель Users
class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(100), nullable=True, default="No name")
    whois = Column(String(20), nullable=True)
    bio = Column(String(1000), nullable=True)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Асинхронное создание таблиц
async def init_db():
    try:
        async with engine.begin() as conn:
            logger.debug("Creating tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.debug("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
# Класс для управления пользователями
class User:
    @staticmethod
    async def create_user(id: int, name: str):
        async with AsyncSessionMaker() as db:
            try:
                # Проверка на существование пользователя
                result = await db.execute(select(Users).filter_by(telegram_id=id))
                existing_user = result.scalar_one_or_none()
                if existing_user:
                    logger.debug("User already exists")
                    return
                
                # Создание нового пользователя
                user = Users(telegram_id=id, username=name)
                db.add(user)
                await db.commit()
                logger.debug(f"User {name} created successfully!")
            except SQLAlchemyError as e:
                await db.rollback()
                logger.error(f"Database error: {e}")
