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
    season = Column(Enum('Fall Spring'.split()))
    time_series_sequence = Column(Integer)


class QuarterlyObservation(Base):
    """Time series for observations occuring each quarter.
    """
    __tablename__ = 'quarterly_observation'

    season_values = 'Fall Winter Spring Summer'.split()

    id = Column(Integer, primary_key=True, autoincrement='auto')
    year_id = Column(Integer, ForeignKey('year.id'))
    time_series_sequence = Column(Integer)
    quarter = Column(Integer)
    # todo unique together year_id and quarter


class TrimesterObservation(Base):
    """Time series for observations occuring three times each year.

    Beginning September of the school year and aligns with
    marking periods.
    """
    __tablename__ = 'trimester_observation'

    season_values = 'Fall Winter Spring'.split()

    id = Column(Integer, primary_key=True, autoincrement='auto')
    time_series_sequence = Column(Integer)
    year_id = Column(Integer, ForeignKey('year.id'))
    trimester = Column(Integer)
    season = Column(Enum(season_values))
    # todo unique together year_id and  trimester
