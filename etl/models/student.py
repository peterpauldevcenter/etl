from sqlalchemy import Column, String, Boolean, Integer
from etl.models import Base


class StudentRoster(Base):
    """Model for static and summary level student features."""
    __tablename__ = 'student_roster'

    id = None
    initial_enrollment_date = None
    number_of_completed_school_years = None


class PeterPaulTerm(Base):
    """Model to represent a time series of related Peter Paul activities.

    Sometimes time series may be a full year, other times sessions are just Summers.
    """
    __tablename__ = 'peter_paul_term'

    id = None


class StudentTimeSeries(Base):
    """Model for time series student features"""
    __tablename__ = 'student_roster_time_series'

    id = None