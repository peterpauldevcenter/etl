from sqlalchemy import Column, Integer, ForeignKey, Enum
from etl.models import Base


class SchoolYear(Base):
    """Model for year time series

    School years start in September, so Sept 2018 - Sept 2019 has a name of 2019
    """
    __tablename__ = 'school_year'

    id = Column(Integer, primary_key=True)
    name = Column(Integer)
    start_year = Column(Integer)
    end_year = Column(Integer)


class Semester(Base):
    """Time series for observations occuring twice a year."""
    __tablename__ = 'semester'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    year_id = Column(Integer, ForeignKey('year.id'))
    name = Column(Enum('Fall Spring'.split()))
    time_series_sequence = Column(Integer)


class Trimester(Base):
    """Time series for observations occuring three times each year.

    Beginning September of the school year and aligns with
    marking periods.
    """
    __tablename__ = 'trimester'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    year_id = Column(Integer, ForeignKey('year.id'))
    name = Column(Integer, Enum('Fall Winter Spring'.split()))
    time_series_sequence = Column(Integer)
    # todo unique together year_id and  trimester


class MarkingPeriod(Base):
    """Time series for observations occuring each quarter.
    """
    __tablename__ = 'marking_period'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    year_id = Column(Integer, ForeignKey('year.id'))
    name = Column(Integer)
    time_series_sequence = Column(Integer)
    # todo unique together year_id and quarter
