import sys
import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).parent
PROJECT_ROOT = PACKAGE_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT.absolute()))

from etl import models, views
import etl
import settings
