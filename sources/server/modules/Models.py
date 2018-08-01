import datetime
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(250), nullable=False)


class SystemInformation(Base):
    __tablename__ = 'system_information'
    id = Column(Integer, primary_key=True)
    platform = Column(String(250))
    system = Column(String(128))
    release = Column(String(128), nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class SystemStatus(Base):
    __tablename__ = 'system_status'
    id = Column(Integer, primary_key=True)
    cpu_percent = Column(Float)
    vmem_percent = Column(Float)
    swap_percent = Column(Float)
    cpu_temp = Column(Float)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class Process(Base):
    __tablename__ = 'processes'
    id = Column(Integer, primary_key=True)
    pid = Column(String(16))
    name = Column(String(1024))
    cpu_percent = Column(Float)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class NginxVersion(Base):
    __tablename__ = 'nginxstatus'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    version = Column(String(128))
    full_version = Column(String(2048))
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class NginxStatus(Base):
    __tablename__ = 'nginxstatus'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    active = Column(Integer)            # active connections
    server = Column(Integer)            # server requests
    accepts = Column(Integer)           # accepts requests
    handled = Column(Integer)           # handled requests
    reading = Column(Integer)           # reading connections
    writing = Column(Integer)           # writing connections
    waiting = Column(Integer)           # waiting connections
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)

