from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from etl.models import Base


class RichmondPublicSchool(Base):
    """Model for Richmond Public Schools

    Source: MAP Test
    """
    __tablename__ = 'school'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)

    district = Column(String)


class Student(Base):
    """Model for students that uniquely identifies the student

    .. warning::

        This table will contain PII
    """
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, autoincrement='auto')

    # MAP Test
    first_name = Column(String)
    last_name = Column(String)
    middle_initial = Column(String)
    date_of_birth = Column(Date)


class StudentDemographics(Base):
    """Model for student demographics that stay relatively constant

    Source: MAP Test, Student Demographics, Student Roster
    """
    __tablename__ = 'student_demographics'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))

    # MAP Test
    ethnic_group = Column(String)

    # MAP Test or Student Demographics
    gender = Column(String)

    # Student Demographics
    year_of_birth = Column(Integer)
    race = Column(String)

    # Student Roster
    peter_paul_enrollment_date = Column(DateTime)
    term_observable = relationship('StudentTermObservation', back_populates='student_term_observation')


class StudentAnnualDemographics(Base):
    """Model for student demographics that change each school year

    Source: Student Demographics, Report Card
    """
    __tablename__ = 'student_annual_demographics'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    school_year_id = Column(Integer, ForeignKey('school_year.id'))

    # Student Demographics
    peter_paul_location_id = Column(Integer, ForeignKey('peter_paul_location.id'))
    family_size = Column(Integer)
    household_type = Column(String)
    family_setting = Column(String)
    income_category = Column(String)
    disability = Column(Boolean)
    promise_family_network = Column(String)

    # Report Card
    school_id = Column(Integer, ForeignKey('school.id'))
    grade_level = Column(Integer)
    promoted = Column(Boolean)
    individualized_education_plan_indicator = Column(Boolean)
