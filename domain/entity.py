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

    # User와 Review 간의 관계 정의
    reviews = relationship("Review", back_populates="user")


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

    # Place와 Review 간의 관계 정의
    reviews = relationship("Review", back_populates="place")


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey('users.id'))  # 외래키 설정
    place_id = Column(Integer, ForeignKey('place.id'))  # 외래키 설정
    star = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Review와 User 간의 관계 정의
    user = relationship("User", back_populates="reviews")

    # Review와 Place 간의 관계 정의
    place = relationship("Place", back_populates="reviews")
