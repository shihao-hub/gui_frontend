from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestSqlAlchemyUser(Base):
    __tablename__ = "test_sql_alchemy_users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


if __name__ == '__main__':
    pass
