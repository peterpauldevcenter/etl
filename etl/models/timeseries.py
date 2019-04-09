from sqlalchemy import Column, Integer, ForeignKey, Enum
from etl.models import Base


class SchoolYear(Base):
    """Model for year time series

    School years start in September, so Sept 2018 - Sept 2019 has a name of 2019
    """
    __tablename__ = 'school_year'

    id = Column(Integer, primary_key=True)
    name = Column(Integer)
    start_year = Column(Integer)
    end_year = Column(Integer)

    def __init__(self, school_year: int):
        self.end_year = school_year
        self.start_year = school_year - 1
        self.name = f'{self.start_year}-{self.end_year}'


class Semester(Base):
    """Time series for observations occuring twice a year.

    School years start in September, so Sept 2018 is Fall of 2019 and April of 2019 is Spring of 2019
    """
    __tablename__ = 'semester'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    name = Column(Enum('Fall Spring'.split()))
    time_series_sequence = Column(Integer)

    semester_numbers = {'Fall': 0, 'Spring': 1}

    def __init__(self, school_year: int, name: str):
        school_year = SchoolYear(school_year)
        self.school_year_id = school_year.id
        self.name = name
        semester_number = self.semester_numbers[name]
        self.time_series_sequence = school_year.start_year * 2 + semester_number


class Trimester(Base):
    """Time series for observations occuring three times each year.

    School years start in September, so Sept 2018 is Fall of 2019 and January of 2019 is Winter of 2019
    """
    __tablename__ = 'trimester'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    name = Column(Integer, Enum('Fall Winter Spring'.split()))
    time_series_sequence = Column(Integer)
    # todo unique together year_id and  trimester

    trimester_numbers = {'Fall': 0, 'Winter': 1, 'Spring': 2}

    def __init__(self, school_year: int, name: str):
        school_year = SchoolYear(school_year)
        self.school_year_id = school_year.id
        self.name = name
        trimester_number = self.trimester_numbers[name]
        self.time_series_sequence = school_year.start_year * 3 + trimester_number


class MarkingPeriod(Base):
    """Time series for observations occuring each quarter.

    School years start in September, so Sept 2018 is MP1 of 2019 and Febuary of 2019 is MP3 of 2019
    """
    __tablename__ = 'marking_period'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    school_year_id = Column(Integer, ForeignKey('school_year.id'))
    name = Column(Integer)
    time_series_sequence = Column(Integer)
    # todo unique together year_id and quarter

    marking_period_numbers = {'MP1': 0, 'MP2': 1, 'MP3': 2, 'MP4': 3}

    def __init__(self, school_year: int, name: str):
        school_year = SchoolYear(school_year)
        self.school_year_id = school_year.id
        self.name = name
        marking_period_number = self.marking_period_numbers[name]
        self.time_series_sequence = school_year.start_year * 4 + marking_period_number

