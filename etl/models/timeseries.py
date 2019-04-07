from sqlalchemy import Column, Integer, ForeignKey, Enum
from etl.models import Base


class Year(Base):
    """Model for year time series"""
    __tablename__ = 'year'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True)


class BiannualObservation(Base):
    """Time series for observations occuring twice a year."""
    __tablename__ = 'biannual_observation'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    year_id = Column(Integer, ForeignKey('year.id'))
    season = Column(Enum('Spring Summer Winter Fall'.split()))


class QuarterlyObservation(Base):
    """Time series for observations occuring each quarter."""
    __tablename__ = 'quarterly_observation'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    year_id = Column(Integer, ForeignKey('year.id'))
    quarter = Column(Integer)
    # todo unique together year_id and quarter


class TrimesterObservation(Base):
    """Time series for observations occuring three times each year."""
    __tablename__ = 'trimester_observation'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    year_id = Column(Integer, ForeignKey('year.id'))
    trimester = Column(Integer)
    # todo unique together year_id and  trimester
