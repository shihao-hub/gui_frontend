from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from nicegui_start_project.settings import database_manager

# sqlalchemy 为什么我觉得这么难用？django 多方便。还是说 sqlalchemy 有自己的亮点？

Base = database_manager.sqlalchemy.Base


class User(Base):
    __tablename__ = 'todolists__users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


database_manager.sqlalchemy.create_all()

if __name__ == '__main__':
    session = database_manager.sqlalchemy.Session()

    # 插入数据
    try:
        session.add(User(name="Alice", age=30))
        session.commit()
    except:  # NOQA
        session.rollback()
        raise

    # 查询数据
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

    session.close()
