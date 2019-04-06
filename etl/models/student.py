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
    student_id = Column(Integer, ForeignKey('StudentRoster.id'))
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


class StudentExperienceQuestionnaire(Base):
    __tablename__ = 'student_experience_questionnaire'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('StudentRoster.id'))
    time_series = Column(Integer, ForeignKey('PeterPaulTerm.id'))
    kids_friendly_with_each_other = Column(Integer)
    does_unwanted_teasing = Column(Integer)
    kids_treat_each_other_respect = Column(Integer)
    you_have_good_friends = Column(Integer)
Spring-2016 d. Do you have a lot of good friends here?
Spring-2016 e. If you were upset, would other kids here try to help you?
Spring-2016 f. Do the other kids here listen to you?
Spring-2016 a. Do you like coming here?
Spring-2016 b. Do you have fun when you're here?
Spring-2016 c. Do you feel bored when you're here?
Spring-2016 d. Can you always find things that you like to do here?
Spring-2016 a. Do you learn new things?
Spring-2016 b. Do you feel challenged <i>in a good way</i>?
Spring-2016 c. Do you get to do things here that you have never done before?
Spring-2016 a. Is there an adult here who is interested in what you think about things?
Spring-2016 b. Is there an adult here you can talk to when you are upset?
Spring-2016 c. Is there an adult here who helps you when you have a problem?
Spring-2016 d. Is there an adult here who <u>you</u> will listen to and respect?
Spring-2016 a. I like to read at home during my free time.
Spring-2016 b. I enjoy reading when I'm at school.
Spring-2016 c. I enjoy reading when I'm at this after-school program.
Spring-2016 d. I'm good at reading.
Spring-2016 e. I like to give new books a try, even if they look hard.
Spring-2016 Has coming to this after-school program helped you to read more often?
Spring-2016 a. I like to learn new things in math.
Spring-2016 b. I like to do math when I'm at school.
Spring-2016 c. I like to do math when I'm at this after-school program.
Spring-2016 d. Math is something I'm good at.
Spring-2016 e. I'm interested in math.
Spring-2016 f. I like to give new math problems a try, even when they look hard.
Spring-2016 Has coming to this after-school program helped you do better in math?
Spring-2016 a. Coming here has helped me to get my homework done.
Spring-2016 b. Coming here has helped me to try harder in school.
Spring-2016 c. Coming here has helped me to do better in school.
Spring-2016 a. Be successful in high school?
Spring-2016 b. Graduate from high school?
Spring-2016 c. Go to college?"""



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

