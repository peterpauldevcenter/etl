import pandas
import pathlib
from etl import session, engine


def get_or_create(model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance is None:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
    else:
        return instance


def execute_sql(sql: str) -> list:
    results = []
    try:
        results = session.execute(sql)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
        return results


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
