import pathlib
from etl.views import utils
from etl.views.timeseries import MarkingPeriodView


class SchoolAttendanceView:

    def __init__(self):
        self.table = 'school_attendence'

    def post(self, report_card_file: pathlib.Path):
        stage_table = utils.create_stage_table_from_file(report_card_file)
        marking_periods = ['M1', 'M2', 'M3', 'M4']
        school_years = [2018]
        marking_period = MarkingPeriodView()
        marking_period_id = marking_period.get_marking_period_id(marking_period=marking_periods,
                                                                 school_year=school_years)
        sql = f'''
            select
                MARKEL_ID as student_id,
                {marking_period_id} as marking_period_id,
                [MP1 ABSENT] as days_absent,
                [MP1 TARDY] as days_tardy,
                [MP1 PRESENT] as days_present,
                [MP1 # DAYS DUE TO SUSPENSION] as days_suspended,
                REASON as suspension_reason
            from {stage_table} stage
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