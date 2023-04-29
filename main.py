from fastapi import FastAPI
import uvicorn
import mysql.connector
from pydantic import BaseModel

app = FastAPI()

userdata = []


class Student(BaseModel):
    name: str
    age: int
    gender: str
    phone: int
    city: str


@app.get("/home/{user_name}")
def get_data(user_name):
    return {
        "user_name": user_name
    }


@app.put("/put_data/{user_data}")
@app.get("/citi")
def get_citi():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="suchitadb1",
    )
    print("mydb >>", mydb)
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute("SELECT id as cid, city_name FROM citi")
    # mycursor.execute("SELECT * from citi where city_name= 'Agra'")

    # myresult = mycursor.fetchone()
    myresult = mycursor.fetchall()
    user_data = []
    print(myresult)

    for row in myresult:
        user_data.append({'city_id': row['cid'], 'city_name': row['city_name']})
    return {'data': user_data}


@app.get("/students")
def get_students():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="suchitadb1",
    )
    print("mydb >>", mydb)
    mycursor = mydb.cursor(dictionary=True)

    # mycursor.execute("SELECT * FROM student ORDER BY name ")
    mycursor.execute("SELECT * FROM student")

    myresult = mycursor.fetchall()

    user_data = []
    print(myresult)

    for row in myresult:
        user_data.append({'student_id': row['studentid'],
                          'student_name': row['name'],
                          'student_age': row['age'],
                          'student_gender': row['gender'],
                          'student_phone': row['phone'],
                          'student_city': row['city']})
    return {'data': myresult}


@app.post("/create-student")
async def create_student(student: Student):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="suchitadb1",
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO student (name, age, gender, phone, city) VALUES (%s, %s, %s, %s, %s)"
    val = (student.name, student.age, student.gender, student.phone, student.city)
    mycursor.execute(sql, val)

    mydb.commit()

    return {"message": "Student record created successfully"}


@app.delete("/delete-student/{student_id}")
async def delete_student(student_id: int):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="suchitadb1",
    )
    mycursor = mydb.cursor()

    sql = "DELETE FROM student WHERE studentid = %s"
    val = (student_id,)
    mycursor.execute(sql, val)

    mydb.commit()

    return {"message": "Student record deleted successfully"}


@app.get("/get-student/{student_id}")
async def get_student(student_id: int):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="suchitadb1",
    )
    mycursor = mydb.cursor(dictionary=True)

    sql = "select * from student WHERE studentid = %s"
    val = (student_id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    # mydb.commit()

    return result


@app.get("/student-details/{student_id}")
async def get_student(student_id: int):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="suchitadb1",
    )
    mycursor = mydb.cursor(dictionary=True)

    sql = "select * from student WHERE studentid = %s"
    val = (student_id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    # mydb.commit()

    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
