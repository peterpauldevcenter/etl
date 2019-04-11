"""Provides models to easy time series calculations and setup."""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from etl.models import Base
from etl.utils import get_or_create


class SchoolYear(Base):
    """Time series for observations occurring once per school year

    School years start in September, so Sept 2018 - Sept 2019 has a name of 2019
    """
    __tablename__ = 'school_year'
    __table_args__ = (UniqueConstraint('school_year', name='uc__school_year'),)

    id = Column(Integer, primary_key=True)
    school_year = Column(Integer)

    name = Column(String)
    start_year = Column(Integer)
    semesters = relationship('Semester')
    trimesters = relationship('Trimester')
    marking_periods = relationship('MarkingPeriod')
    student_annual_demographics = relationship('StudentAnnualDemographics')
    student_annual_peter_paul_summary = relationship('StudentAnnualPeterPaulSummary')

    def __init__(self, school_year: int):
        self.school_year = school_year
        self.start_year = school_year - 1
        self.name = f'{self.start_year}-{self.school_year}'


class Semester(Base):
    """Time series for observations occurring twice per school year

    School years start in September, so Sept 2018 is Fall of 2019 and April of 2019 is Spring of 2019
    """
    __tablename__ = 'semester'
    __table_args__ = (UniqueConstraint('school_year_id', 'name', name='uc__school_year__name'),)

    semester_numbers = {'Fall': 0, 'Spring': 1}

    id = Column(Integer, primary_key=True, autoincrement='auto')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    school_year = relationship('SchoolYear', back_populates='semesters')
    name = Column(String)
    time_series_sequence = Column(Integer)

    def __init__(self, school_year: int, name: str):
        self.school_year = get_or_create(SchoolYear, school_year=school_year)
        self.name = name
        semester_number = self.semester_numbers[name]
        self.time_series_sequence = self.school_year.start_year * 2 + semester_number


class Trimester(Base):
    """Time series for observations occurring three times each year

    School years start in September, so Sept 2018 is Fall of 2019 and January of 2019 is Winter of 2019
    """
    __tablename__ = 'trimester'
    __table_args__ = (UniqueConstraint('school_year_id', 'name', name='uc__school_year__name'),)

    trimester_numbers = {'Fall': 0, 'Winter': 1, 'Spring': 2}

    id = Column(Integer, primary_key=True, autoincrement='auto')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    school_year = relationship('SchoolYear', back_populates='trimesters')
    name = Column(String)
    time_series_sequence = Column(Integer)
    map_tests = relationship('MAPTest')

    def __init__(self, school_year: int, name: str):
        self.school_year = get_or_create(SchoolYear, school_year=school_year)
        self.name = name
        trimester_number = self.trimester_numbers[name]
        self.time_series_sequence = self.school_year.start_year * 3 + trimester_number


class MarkingPeriod(Base):
    """Time series for observations occurring each quarter of a school year

    School years start in September adn end in June, so Sept 2018 is MP1 of 2019 and Febuary of 2019 is MP3 of 2019

    .. warning::

        Because this is school year-based, summer is skipped. This is not meant to tie to concepts like
        Summer Promise. Instead, Summer Promise is thought of as occurring all at once on the first day
        of the following school year.

    """
    __tablename__ = 'marking_period'
    __table_args__ = (UniqueConstraint('school_year_id', 'name', name='uc__school_year__name'),)

    marking_period_numbers = {'MP1': 0, 'MP2': 1, 'MP3': 2, 'MP4': 3}

    id = Column(Integer, primary_key=True, autoincrement='auto')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    school_year = relationship('SchoolYear', back_populates='marking_periods')
    name = Column(String)
    time_series_sequence = Column(Integer)
    school_attendance = relationship('SchoolAttendance')
    report_cards = relationship('ReportCard')

    def __init__(self, school_year: int, name: str):
        self.school_year = get_or_create(SchoolYear, school_year=school_year)
        self.name = name
        marking_period_number = self.marking_period_numbers[name]
        self.time_series_sequence = self.school_year.start_year * 4 + marking_period_number

