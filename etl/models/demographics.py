from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from etl.models import Base


class PeterPaulOrganization(Base):
    """Model for Peter Paul Organizations"""
    __tablename__ = 'peter_paul_organization'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Demographics(Base):
    """Model for student demographics in the Richmond Public School system"""
    __tablename__ = 'demographics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)

    peter_paul_organization_id = Column(Integer, ForeignKey('peter_paul_organization.id'))
    year_of_birth = Column(Integer)
    race = Column(String)
    gender = Column(String)
    family_size = Column(Integer)
    household_type = Column(String)
    family_setting = Column(String)
    income_category_id = Column(String)
    disability = Column(Boolean)
    student_pfn = Column(String)