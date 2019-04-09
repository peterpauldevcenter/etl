import pathlib
from etl.views import utils


class SchoolAttendanceView:

    def __init__(self):
        self.table = 'school_attendence'

    def post(self, report_card_file: pathlib.Path):
        stage_table = utils.create_stage_table_from_file(report_card_file)
        sql = f'''
            select
                MARKEL_ID as student_id,
            from {stage_table} stage
            join marking_period mp
                on mp.name = stage.
            join school_year sy
                on sy.id = mp.school_year_id
                and sy.start_year = 2018
        '''
        utils.execute_sql(sql)

"""
    student_id = Column(Integer, ForeignKey('student.id'))
    marking_period_id = Column(Integer, ForeignKey('marking_period.id'))

    days_absent = Column(Integer)
    days_tardy = Column(Integer)
    days_present = Column(Integer)
    days_suspended = Column(Integer)
    suspension_reason = Column(String)

"""