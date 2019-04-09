from etl.views import utils, engine, session
from etl.models import timeseries

class MarkingPeriodView:

    def __init__(self):
        pass

    def get_marking_period_id(self, marking_period: list, school_year: list):
        sql = f'''
            select
                marking_period_id
            from marking_period mp
            join school_year sy
                on sy.id = mp.school_year_id
            where sy.start_year in ({','.join(school_year)})
            and mp.name = (','.join({marking_period}))
        '''
        return utils.execute_sql(sql)

    def post(self, start_year, end_year):
        marking_period = timeseries.MarkingPeriod()
        engine.execute(marking_period.)