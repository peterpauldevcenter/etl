"""Records Peter Paul specific data as well as summary data from other sources.

"""
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from etl.models import Base
from etl.models.student_demographics import Student
from etl.models.timeseries import SchoolYear
from etl import session


class PeterPaulLocation(Base):
    """Model for Peter Paul Locations

    Source: Student Demographics
    """
    __tablename__ = 'peter_paul_location'
    __table_args__ = (UniqueConstraint('name', name='uc__name'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)

    student_demographics = relationship('StudentDemographics')
    student_annual_demographics = relationship('StudentAnnualDemographics')
    student_annual_peter_paul_summary = relationship('StudentAnnualPeterPaulSummary')

    def __init__(self, name: str):
        self.name = name


class StudentAnnualPeterPaulSummary(Base):
    """Model for Peter Paul summary time series student features

    Source: Student Roster
    """
    __tablename__ = 'student_annual_peter_paul_summary'
    __table_args__ = (UniqueConstraint('student_id', 'school_year_id', name='uc__student__school_year'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='student_annual_peter_paul_summary')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    school_year = relationship('SchoolYear', back_populates='student_annual_peter_paul_summary')

    peter_paul_location_id = Column(Integer, ForeignKey('peter_paul_location.id'))
    peter_paul_location = relationship('PeterPaulLocation', back_populates='student_annual_peter_paul_summary')

    attended_peter_paul_during_school_year = Column(Boolean)
    attended_peter_paul_summer_promise = Column(Boolean)
    did_not_complete_peter_paul_during_school_year = Column(Boolean)

    growth_in_reading = Column(String)
    test_percentile_in_reading = Column(Integer)
    met_national_norm_in_reading = Column(Boolean)

    growth_in_math = Column(String)
    test_percentile_in_math = Column(Integer)
    met_national_norm_in_math = Column(Boolean)

    def __init__(self, student_token: int, school_year: int):
        student = session.query(Student).filter_by(student_token=student_token).first()
        if student is None:
            student = Student(student_token=student_token)
        self.student = student
        school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
        if school_year_obj is None:
            school_year_obj = SchoolYear(school_year=school_year)
        self.school_year = school_year_obj
