import datetime
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(250), nullable=False)


class Version(Base):
    __tablename__ = 'version'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    version = Column(String(128))
    full_version = Column(String(2048))
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    active = Column(Integer)            # active connections
    server_requests = Column(Integer)   # server requests
    accepts_requests = Column(Integer   # accepts requests
    handled_requests = Column(Integer   # handled requests
    reading = Column(Integer)           # reading connections
    writing = Column(Integer)           # writing connections
    waiting = Column(Integer)           # waiting connections
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)
