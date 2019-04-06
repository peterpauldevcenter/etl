from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from etl.models import Base


class StudentRoster(Base):
    """Model for static and summary level student features."""
    __tablename__ = 'student_roster'

    id = Column(Integer, primary_key=True)
    initial_enrollment_date = None
    number_of_completed_school_years = None


class PeterPaulTerm(Base):
    """Model to represent a time series of related Peter Paul activities.

    Sometimes time series may be a full year, other times sessions are just Summers.
    """
    __tablename__ = 'peter_paul_term'

    id = Column(Integer, primary_key=True)
    """Since time series are of variable length, rely on their sequential order."""
    sequential_order = None


class StudentTimeSeries(Base):
    """Model for time series student features"""
    __tablename__ = 'student_roster_time_series'

    id = Column(Integer, primary_key=True)
    time_series = Column(Integer, ForeignKey('PeterPaulTerm.id'))
    grade = Column(Integer)
    peter_paul_location = Column(Integer, ForeignKey('PeterPaulLocation.id'))
    attended_peter_paul_for_time_series = Column(Boolean)


