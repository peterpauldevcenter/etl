import pandas
import pathlib
from etl.views import session, engine


def execute_sql(sql: str):
    try:
        session.execute(sql)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def create_stage_table_from_file(file: pathlib.Path) -> str:
    """Boiler plate code to create a staging table from an Excel file

    Args:
        file: Excel file to be read in as the staging table

    Returns: the name of the staging table, which should be the file name with 'stage_' prepended to it

    """
    table_name = f'stage_{file.name}'
    df = pandas.read_excel(file.absolute())
    df.to_sql(con=engine, index_label='id', name=table_name, if_exists='replace')
    return table_name
