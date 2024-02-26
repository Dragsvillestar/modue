from sqlalchemy import create_engine, text
import logging
import pandas as pd

""" Import sqlalchemy, logging and pandas,
    to create database connection, logging information and DataFrames respectively
"""
# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('data_ingestion')
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sql_query = """
SELECT *
FROM geographic_features
LEFT JOIN weather_features USING (Field_ID)
LEFT JOIN soil_and_crop_features USING (Field_ID)
LEFT JOIN farm_management_features USING (Field_ID)
"""

def query_data(engine, sql_query):
    """ Create a database connection object
        and use Pandas to execute the query and store the result in a DataFrame
        
        Args:
        engine: database engine
        sql_query: SQL query written in text format (to be used by pandas in creating DataFrame) 
        
        Return: DataFrame.
        
        Note: If there are errors, messages indicating error type will be displayed
        
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e