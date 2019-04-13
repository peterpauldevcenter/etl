"""Describes a Survey of Academic Youth Outcomes (SAYO) Questionnaire.

A questionnaire is given during the Fall and Spring of each school year.
The questions and sections are on a semi-Likert scale, only 1-4.

The component sections roll up to the questionnaire.

.. warning::

    These models are currently not being populated.

    During ETL two questions need to be reversed so the semi-Likert section averages
    compute properly. ie. 4 becomes 1, 3 becomes 2, etc

    - EnjoymentEngagementScale.feel_bored
    - SupportiveSocialEnvironmentScale.does_unwanted_teasing

.. note::

    Unlike Django, SQLAlchemy does not automatically create reverse relations when ForeignKey
    fields are created. There are two methods to set up the relation, backref_ and back_populates_.
    The difference being backref automatically creates the reverse relationship, but back_populates
    requires explicit setting the reverse on the target. I've opted to use back_populates here as it is more explicit.

    .. _backref: https://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref
    .. _back_populates: https://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates

"""
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from etl.models import Base


class SocialScale(Base):
    __tablename__ = 'student_experience_questionnaire_social_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='socialscale')

    kids_friendly_with_each_other = Column(Integer)
    does_unwanted_teasing = Column(Integer)
    kids_treat_each_other_respect = Column(Integer)
    have_good_friends = Column(Integer)
    other_kids_help = Column(Integer)
    other_kids_listen_to_you = Column(Integer)


class EnjoymentScale(Base):
    __tablename__ = 'student_experience_questionnaire_enjoyment_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='enjoymentscale')

    you_like_coming_here = Column(Integer)
    have_fun_here = Column(Integer)
    feel_bored = Column(Integer)
    find_things_to_do = Column(Integer)


class ChallengeScale(Base):
    __tablename__ = 'student_experience_questionnaire_challenge_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='challengescale')

    learn_new_things = Column(Integer)
    feel_challenged = Column(Integer)
    do_new_things = Column(Integer)


class SupportiveAdultScale(Base):
    __tablename__ = 'student_experience_questionnaire_supportive_adult_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='supportiveadultscale')

    adult_interested_in_think = Column(Integer)
    adult_can_talk_when_upset = Column(Integer)
    adult_helps_with_problems = Column(Integer)
    adult_you_respect = Column(Integer)


class ReaderScale(Base):
    __tablename__ = 'student_experience_questionnaire_reader_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='readerscale')

    like_to_read_at_home = Column(Integer)
    like_to_read_at_school = Column(Integer)
    like_to_read_after_school_program = Column(Integer)
    good_at_reading = Column(Integer)
    like_to_give_new_books_try = Column(Integer)


class MathScale(Base):
    """All scales are 1-4"""
    __tablename__ = 'student_experience_questionnaire_math_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='mathscale')

    like_to_learn_new_math = Column(Integer)
    like_to_do_math_at_school = Column(Integer)
    like_to_do_math_at_after_school_program = Column(Integer)
    math_is_something_good_at = Column(Integer)
    interested_in_math = Column(Integer)
    like_to_try_new_math_problems = Column(Integer)


class Retrospective(Base):
    """Restrospective questions are independent, only for subjective analysis
    They are not used to create a scaled rating. Only asked on Spring survey.
    Fall survey will have nulls.
    """
    __tablename__ = 'student_experience_questionnaire_retrospective'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='retrospective')

    coming_to_this_program_helped_read_more_often = Column(Integer)
    coming_helped_math = Column(Integer)
    coming_helped_homework = Column(Integer)
    coming_helped_try_harder_in_school = Column(Integer)
    coming_helped_do_better_in_school = Column(Integer)
    # The below features only apply to middle school students and should only be averaged
    be_successful_in_high_school = Column(Integer)
    graduated_from_high_school = Column(Integer)
    go_to_college = Column(Integer)


class Freeform(Base):
    """Fields to collect the free form questions.
    """
    __tablename__ = 'student_experience_questionnaire_freeform'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_experience_questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    questionnaire = relationship('StudentExperienceQuestionnaire', uselist=False, back_populates='freeform')

    favorite_thing_to_do_here = Column(String(length=280))
    activities_wish_offered = Column(String(length=280))


class StudentExperienceQuestionnaire(Base):
    """Model for the student questionnaire, taken once in the Fall and again in the Spring.
    """
    __tablename__ = 'student_experience_questionnaire'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    semester_id = Column(Integer, ForeignKey('semester.id'))

    socialscale = relationship('SocialScale', uselist=False, back_populates='questionnaire')
    enjoymentscale = relationship('EnjoymentScale', uselist=False, back_populates='questionnaire')
    challengescale = relationship('ChallengeScale', uselist=False, back_populates='questionnaire')
    supportiveadultscale = relationship('SupportiveAdultScale', uselist=False, back_populates='questionnaire')
    readerscale = relationship('ReaderScale', uselist=False, back_populates='questionnaire')
    mathscale = relationship('MathScale', uselist=False, back_populates='questionnaire')
    retrospective = relationship('Retrospective', uselist=False, back_populates='questionnaire')
    freeform = relationship('Freeform', uselist=False, back_populates='questionnaire')
