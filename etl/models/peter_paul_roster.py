from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, Enum
from etl.models import Base


class PeterPaulLocation(Base):
    """Model for Peter Paul Locations

    Source: Student Demographics
    """
    __tablename__ = 'peter_paul_location'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)


class StudentTermObservation(Base):
    """Model for Peter Paul term time series student features

    Source: Student Roster
    """
    __tablename__ = 'student_term_observation'

    growth_eumerated_values = 'any projection exceeded'.split()

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    school_year_id = Column(Integer, ForeignKey('school_year.id'))

    grade = Column(Integer)
    peter_paul_location = Column(Integer, ForeignKey('peter_paul_location.id'))
    attended_peter_paul_during_school_year = Column(Boolean)
    attended_peter_paul_summer_promise = Column(Boolean)
    growth_in_reading = Column(Enum(growth_eumerated_values))
    test_percentile_in_reading = Column(Integer)
    met_national_norm_in_reading = Column(Boolean)
    growth_in_math = Column(Enum(growth_eumerated_values))
    test_percentile_in_math = Column(Integer)
    met_national_norm_in_math = Column(Boolean)
    number_of_completed_program_years = Column(Integer)
