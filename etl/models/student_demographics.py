"""Models for storing student demographics.

Unlike most other models, these are shared models that are built out from multiple sources.
"""
from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from etl.models import Base
from etl.models.timeseries import SchoolYear
from etl import session


class School(Base):
    """Model for Richmond Public Schools

    Source: MAP Test
    """
    __tablename__ = 'school'
    __table_args__ = (UniqueConstraint('name', name='uc__name'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)

    district = Column(String)
    student_annual_demographics = relationship('StudentAnnualDemographics')

    def __init__(self, name: str):
        self.name = name


class Student(Base):
    """Model for students that uniquely identifies the student

    Source: Student Roster (just keys)

    .. warning::

        This table will contain PII
    """
    __tablename__ = 'student'
    __table_args__ = (UniqueConstraint('student_token', name='uc__student_token'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')

    # MAP Test
    student_token = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    middle_initial = Column(String)
    date_of_birth = Column(Date)
    student_demographics = relationship('StudentDemographics')
    student_annual_demographics = relationship('StudentAnnualDemographics')
    school_attendance = relationship('SchoolAttendance')
    report_cards = relationship('ReportCard')
    student_annual_peter_paul_summary = relationship('StudentAnnualPeterPaulSummary')
    map_tests = relationship('MAPTest')
    map_test_growth = relationship('MAPTestGrowth')

    def __init__(self, student_token: int):
        self.student_token = student_token


class StudentDemographics(Base):
    """Model for student demographics that stay relatively constant

    Source: MAP Test, Student Demographics, Student Roster
    """
    __tablename__ = 'student_demographics'
    __table_args__ = (UniqueConstraint('student_id', name='uc__student'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='student_demographics')

    # MAP Test
    ethnic_group = Column(String)
    # MAP Test or Student Demographics
    gender = Column(String)
    # Student Demographics
    year_of_birth = Column(Integer)
    race = Column(String)
    # Student Roster
    peter_paul_enrollment_date = Column(DateTime)
    peter_paul_location_id = Column(Integer, ForeignKey('peter_paul_location.id'))
    peter_paul_location = relationship('PeterPaulLocation', back_populates='student_demographics')

    def __init__(self, student_token: int):
        student = session.query(Student).filter_by(student_token=student_token).first()
        if student is None:
            student = Student(student_token=student_token)
        self.student = student


class StudentAnnualDemographics(Base):
    """Model for student demographics that could change each school year

    Source: Student Demographics, Report Card
    """
    __tablename__ = 'student_annual_demographics'
    __table_args__ = (UniqueConstraint('student_id', 'school_year_id', name='uc__student__school_year'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='student_annual_demographics')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    school_year = relationship('SchoolYear', back_populates='student_annual_demographics')

    # Student Demographics
    peter_paul_location_id = Column(Integer, ForeignKey('peter_paul_location.id'))
    peter_paul_location = relationship('PeterPaulLocation', back_populates='student_annual_demographics')
    family_size = Column(Integer)
    household_type = Column(String)
    family_setting = Column(String)
    income_category = Column(String)
    disability = Column(Boolean)
    promise_family_network = Column(String)

    # Report Card
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship('School', back_populates='student_annual_demographics')
    grade_level = Column(Integer)
    promoted = Column(Boolean)
    individualized_education_plan_indicator = Column(Boolean)

    def __init__(self, student_token: int, school_year: int):
        student = session.query(Student).filter_by(student_token=student_token).first()
        if student is None:
            student = Student(student_token=student_token)
        self.student = student
        school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
        if school_year_obj is None:
            school_year_obj = SchoolYear(school_year=school_year)
        self.school_year = school_year_obj
