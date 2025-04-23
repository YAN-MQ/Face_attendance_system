from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# MySQL连接配置
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'face_attendance'

# 创建SQLAlchemy连接字符串
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建SQLAlchemy引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础类，所有的ORM模型都将继承自这个类
Base = declarative_base()

# 获取数据库会话函数
def get_db():
    db = SessionLocal()
    return db 