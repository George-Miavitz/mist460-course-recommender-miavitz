from fastapi import FastAPI, HTTPException
import pyodb
import os
from dotenvy import load_dotenv
from pathlib import Path

from web_apis.course_recommender_apis import DBSERVER
#Load environment variables from .env file
# path - Path(__file__).parent / '.env'
#load_dotenv(path)



def get_db_connection():

    environment = os.getenv('ENVIRONMENT')
    if environment == 'PRODUCTION':
        DB_SERVER = os.getenv('DB_SERVER')
        DB_DATABASE = os.getenv('DB_DATABASE')
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_DRIVER = os.getenv('DB_DRIVER')
        connection_string = (
            f'DRIVER={DB_DRIVER};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_DATABASE};'
            f'UID={DB_USERNAME};'
            f'PWD={DB_PASSWORD};'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )

    else: 
        #Local Database connection parameters
        DB_SERVER = #Need to create local server
        DB_DATABASE = #Need to create local database
        DB_Driver = '{ODBC Driver 18 for SQL Server}'
        connection_string = (
            
            f'DRIVER={DB_DRIVER};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_DATABASE};'
            'Encrypt=yes;'
            'trusted_connection=yes;'
            'Connection Timeout=30;'
        )


    try:
        return pyodbc.connect(connection_string)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
 
        

