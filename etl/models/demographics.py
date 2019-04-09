from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from etl.models import Base


class PeterPaulLocation(Base):
    """Model for Peter Paul Locations

    todo: combine into a consolidated Peter Paul location model
    """
    __tablename__ = 'peter_paul_location'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)


class StudentDemographics(Base):
    """Model for student demographics in the Richmond Public School system

    todo: combine into consolidated student model
    """
    __tablename__ = 'student_demographics'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))

    year_of_birth = Column(Integer)
    race = Column(String)
    gender = Column(String)


class StudentAnnualDemographics(Base):
    """Model for student demographics in the Richmond Public School system"""
    __tablename__ = 'student_annual_demographics'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    year_id = Column(Integer, ForeignKey('year.id'))

    peter_paul_location_id = Column(Integer, ForeignKey('peter_paul_location.id'))
    family_size = Column(Integer)
    household_type = Column(String)
    family_setting = Column(String)
    income_category = Column(String)
    disability = Column(Boolean)
    promise_family_network = Column(String)
