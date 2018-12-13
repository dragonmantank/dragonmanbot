from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dragonmanbot import engine, session

Base = declarative_base()

class TwitchUser(Base):
    __tablename__ = "twitch_user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    gold = Column(Integer)

class TwitchUserRepository:
    def findByUsername(self, username):
        user = session.query(TwitchUser).filter_by(username=username).first()
        if not user:
            user = TwitchUser(
                username=username,
                gold=1
            )
            session.add(user)
            session.commit()

        return user
    
    def save(self, user):
        session.add(user)
        session.commit()


repository = TwitchUserRepository()
Base.metadata.create_all(engine)