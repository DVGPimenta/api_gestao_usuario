from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

url = 'mysql+pymysql://root:4188@localhost:3306/gestao_usuarios'
engine = create_engine(url)
Base = declarative_base()



