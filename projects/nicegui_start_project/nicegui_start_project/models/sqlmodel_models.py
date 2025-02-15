from abc import ABC, abstractmethod

from sqlmodel import SQLModel, Field, Session, create_engine, select

from nicegui_start_project.settings import SOURCE_DIR


class TestSqlModelHero(SQLModel, table=True):
    __tablename__ = "test_sql_model_hero"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    team: str | None = None


class Manager(ABC):
    @abstractmethod
    def run(self):
        pass


class ManagerIml(Manager):
    def __init__(self):
        pass

    def run(self):
        Hero = TestSqlModelHero

        # init database
        engine = create_engine(f"sqlite:///{SOURCE_DIR}/sqlite.db")
        SQLModel.metadata.create_all(engine)

        # create
        with Session(engine) as session:
            hero = Hero(name="Thor", age=1500, team="Avengers")
            session.add(hero)
            session.commit()
        print("------------")

        # read
        with Session(engine) as session:
            # 查询所有
            heroes = session.exec(select(Hero)).all()

            # 条件查询
            thor = session.exec(select(Hero).where(Hero.name == "Thor")).first()
            print(heroes)
            print(thor)
        print("------------")

        # update
        with Session(engine) as session:
            thor = session.exec(select(Hero).where(Hero.name == "Thor")).first()
            thor.age = 1501
            session.add(thor)
            session.commit()
            print(session.exec(select(Hero).where(Hero.name == "Thor")))
        print("------------")

        # delete
        # with Session(engine) as session:
        #     hero = session.exec(select(Hero).where(Hero.name == "Thor")).first()
        #     session.delete(hero)
        #     session.commit()
        #     print(session.exec(select(Hero)).all())
        # print("------------")


if __name__ == '__main__':
    ManagerIml().run()
