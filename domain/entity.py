from sqlalchemy import Column, Integer, String, DateTime, Time, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Station(Base):
    __tablename__ = 'station'
    name = Column(String(255), primary_key=True)
    line = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())


class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(16), nullable=False)
    location = Column(String(255), nullable=False)
    start_at = Column(Time)
    end_at = Column(Time)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    menu = Column(JSON)
    url = Column(String(2048))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    user_id = Column(String(255), ForeignKey('users.id'))  # 외래키 설정
    station = Column(String(255), ForeignKey('station.name'))  # 외래키 설정


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey('users.id'))  # 외래키 설정
    place_id = Column(Integer, ForeignKey('place.id'))  # 외래키 설정
    star = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
