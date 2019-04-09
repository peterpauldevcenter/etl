from sqlalchemy import Column, Boolean, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from etl.models import Base


class StudentRoster(Base):
    """Model for static and summary level student features."""
    __tablename__ = 'student_roster'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    initial_enrollment_date = Column(DateTime)
    number_of_completed_school_years = Column(Integer)

    term_observable = relationship('StudentTermObservation', black_populates='student_term_observation')


class StudentTermObservation(Base):
    """Model for Peter Paul term time series student features"""
    __tablename__ = 'student_term_observation'

    growth_eumerated_values = 'any projection exceeded'.split()

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student_roster.id'))
    time_series = Column(Integer, ForeignKey('trimester_observation.id'))
    grade = Column(Integer)
    peter_paul_location = Column(Integer, ForeignKey('peter_paul_location.id'))
    attended_peter_paul_for_time_series = Column(Boolean)
    growth_in_reading = Column(Enum(growth_eumerated_values))
    test_percentile_in_reading = Column(Integer)
    met_national_norm_in_reading = Column(Boolean)
    growth_in_math = Column(Enum(growth_eumerated_values))
    test_percentile_in_math = Column(Integer)
    met_national_norm_in_math = Column(Boolean)
