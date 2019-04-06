from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from etl.models import Base


class StudentRoster(Base):
    """Model for static and summary level student features."""
    __tablename__ = 'student_roster'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    initial_enrollment_date = None
    number_of_completed_school_years = None


class Year(Base):
    """Model for year time series"""
    id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True)


class PeterPaulTerm(Base):
    """Model to for Peter Paul term.

    Sometimes time series may be a full year, other times sessions are just Summers.
    """
    __tablename__ = 'peter_paul_term'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    """Since time series are of variable length, rely on their sequential order."""
    sequential_order = Column(Integer,)
    year_id = Column(Integer, ForeignKey('Year.id'))


class StudentTermTimeSeries(Base):
    """Model for Peter Paul term time series student features"""
    __tablename__ = 'student_roster_time_series'

    growth_eumerated_values = 'any projection exceeded'.split()

    id = Column(Integer, primary_key=True, autoincrement='auto')
    time_series = Column(Integer, ForeignKey('PeterPaulTerm.id'))
    grade = Column(Integer)
    peter_paul_location = Column(Integer, ForeignKey('PeterPaulLocation.id'))
    attended_peter_paul_for_time_series = Column(Boolean)
    growth_in_reading = Column(Enum(growth_eumerated_values))
    test_percentile_in_reading = Column(Integer)
    met_national_norm_in_reading = Column(Boolean)
    growth_in_math = Column(Enum(growth_eumerated_values))
    test_percentile_in_math = Column(Integer)
    met_national_norm_in_math = Column(Boolean)


class StudentYearTimeSeries(Base):
    """Model for year based student features."""
    __tablename__ = 'student_year_time_series'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('StudentRoster.id'))
    year = Column(Integer, ForeignKey('Year.id'), unique=True)
    grade_promotion = Column(Boolean)
    school_missed_for_suspension = Column(Boolean)
    reading_sol_passed = Column(Boolean)
    math_sol_passed = Column(Boolean)


class StudentObservation(Base):
    __tablename__ = 'student_roster_observation'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('StudentRoster.id'))
    peter_paul_term_id = Column(Integer, ForeignKey('PeterPaulTerm.id'))
    # ToDO: Define enum?
    description_reading = Column(String)
    description_math = Column(String)

