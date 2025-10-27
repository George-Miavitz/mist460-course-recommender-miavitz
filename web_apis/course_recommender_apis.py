from fastapi import FastAPI, HTTPException
import pyodb
import os
from dotenvy import load_dotenv
from pathlib import Path
#Load environment variables from .env file
# path - Path(__file__).parent / '.env'
#load_dotenv(path)

app = FastAPI()

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

    # Database connection setup
    DBSERVER = 'mist-miavitz.database.windows.net'
    DB_DATABASE = 'mist-miavitz.MIST460_RelationalDatabase_Miavitz.dbo'
    #DB_USERNAME = 'needs to go in a file'
    #DB_PASSWORD = 'needs to go into another file'
    DB_DRIVER = '{ODBC Driver 18 for SQL Server}'

    def get_db_connection():
        try:
            conn_str = f'DRIVER={DB_DRIVER};SERVER={DBSERVER};DATABASE={DB_DATABASE};trusted_connection=yes;'
            return pyodbc.connect(conn_str)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise HTTPException(status_code=500, detail="Database connection error")

@app.get("/find_current_semester_course_offerings")
def find_current_semester_course_offerings(
    subject_code: str,
    course_number: str
    ):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("{CALL procFindCurrentSemesterCourseOfferingsForSpecifiedCourse(?, ?)}", subject_code, course_number)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert rows to list of dictionaries for better serialization
    results = [
        
        {
            "SubjectCode": row.SubjectCode,
            "CourseNumber": row.CourseNumber,
            "CRN": row.CRN,
            "Semester": row.CourseOfferingSemester,
            "Year": row.CourseOfferingYear,
            "CourseOfferingID": row.CourseOfferingID,
            "NumberSeatsRemaining": row.NumberSeatsRemaining
        }
                for row in rows
        ]


    return {"data": results}
