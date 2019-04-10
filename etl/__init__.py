from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import settings
from . import models, views
# from .models import timeseries, student_demographics  # , report_card, questionnaire, peter_paul_roster, map_testing


engine = create_engine(settings.ENGINE)

session_factory = sessionmaker()
session_factory.configure(bind=engine)
session = session_factory()

