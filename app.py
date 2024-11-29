import os
from flask import Flask, request, render_template, redirect, url_for
import pyodbc

app = Flask(__name__,  template_folder=os.path.join(os.getcwd(), 'templates'), static_folder='static', static_url_path='/static')

def create_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=.;'
            'DATABASE=Training;'
            'Trusted_Connection=yes;'
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            if fetch:
                result = cursor.fetchall()
                return result
            connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    return None

@app.route('/')
def index():
    sectors = execute_query("SELECT * FROM Sector", fetch=True)
    if sectors is not None:
        return render_template('index.html', sectors=sectors)
    return "Error connecting to the database"

@app.route('/add_Sector', methods=['GET', 'POST'])
def add_Sector():
    if request.method == 'POST':
        sectorid = request.form['sectorid']
        sectorname = request.form['sectorname']
        query = "INSERT INTO Sector(sectorid, sectorname) VALUES (?, ?)"
        execute_query(query, (sectorid, sectorname))
        return redirect(url_for('index'))
    return render_template('add_Sector.html')

@app.route('/edit_Sector', methods=['GET', 'POST'])
def edit_Sector():
    if request.method == 'POST':
        sectorid = request.form['sectorid']
        sectorname = request.form['sectorname']
        query = "UPDATE Sector SET sectorname = ? WHERE sectorid = ?"
        execute_query(query, (sectorname, sectorid))
        return redirect(url_for('index'))
    
    sectors = execute_query("SELECT sectorid, sectorname FROM Sector", fetch=True)
    return render_template('edit_Sector.html', sectors=sectors)

@app.route('/delete_Sector', methods=['GET', 'POST'])
def delete_Sector():
    if request.method == 'POST':
        sectorid = request.form['sectorid']
        query = "DELETE FROM Sector WHERE sectorid = ?"
        execute_query(query, (sectorid,))
        return redirect(url_for('index'))
    
    sectors = execute_query("SELECT sectorid, sectorname FROM Sector", fetch=True)
    return render_template('delete_Sector.html', sectors=sectors)

@app.route('/add_CentralizationMangement', methods=['GET', 'POST'])
def add_CentralizationMangement():
    if request.method == 'POST':
        CentralMangementid = request.form['CentralMangementid']
        sectorid = request.form['sectorid']
        CentralMangementname = request.form['CentralMangementname']
        query = '''
            INSERT INTO CentralizationMangement(CentralMangementid, sectorid, CentralMangementname)
            VALUES (?, ?, ?)
        '''
        execute_query(query, (CentralMangementid, sectorid, CentralMangementname))
        return redirect(url_for('index'))
    
    sectors = execute_query("SELECT sectorid, sectorname FROM Sector", fetch=True)
    return render_template('add_CentralizationMangement.html', sectors=sectors)

@app.route('/edit_CentralizationMangement', methods=['GET', 'POST'])
def edit_CentralizationMangement():
    if request.method == 'POST':
        CentralMangementid = request.form['CentralMangementid']
        sectorid = request.form['sectorid']
        CentralMangementname = request.form['CentralMangementname']
        query = '''
            UPDATE CentralizationMangement
            SET sectorid = ?, CentralMangementname = ?
            WHERE CentralMangementid = ?
        '''
        execute_query(query, (sectorid, CentralMangementname, CentralMangementid))
        return redirect(url_for('index'))
    
    central_managements = execute_query("SELECT CentralMangementid, CentralMangementname, sectorid FROM CentralizationMangement", fetch=True)
    sectors = execute_query("SELECT sectorid, sectorname FROM Sector", fetch=True)
    return render_template('edit_CentralizationMangement.html', central_managements=central_managements, sectors=sectors)

@app.route('/delete_CentralizationMangement', methods=['GET', 'POST'])
def delete_CentralizationMangement():
    if request.method == 'POST':
        CentralMangementid = request.form['CentralMangementid']
        query = "DELETE FROM CentralizationMangement WHERE CentralMangementid = ?"
        execute_query(query, (CentralMangementid,))
        return redirect(url_for('index'))
    
    central_managements = execute_query("SELECT CentralMangementid, CentralMangementname FROM CentralizationMangement", fetch=True)
    return render_template('delete_CentralizationMangement.html', central_managements=central_managements)

@app.route('/add_Public_Mangement', methods=['GET', 'POST'])
def add_Public_Mangement():
    if request.method == 'POST':
        PublicMangementid = request.form['PublicMangementid']
        CentralMangementid = request.form['CentralMangementid']
        PublicMangementname = request.form['PublicMangementname']
        query = '''
            INSERT INTO Public_Mangement(PublicMangementid, CentralMangementid, PublicMangementname)
            VALUES (?, ?, ?)
        '''
        execute_query(query, (PublicMangementid, CentralMangementid, PublicMangementname))
        return redirect(url_for('index'))
    
    CentralizationMangement = execute_query("SELECT CentralMangementid, CentralMangementname FROM CentralizationMangement", fetch=True)
    return render_template('add_Public_Mangement.html', CentralizationMangement=CentralizationMangement)

@app.route('/edit_Public_Mangement', methods=['GET', 'POST'])
def edit_Public_Mangement():
    if request.method == 'POST':
        PublicMangementid = request.form['PublicMangementid']
        CentralMangementid = request.form['CentralMangementid']
        PublicMangementname = request.form['PublicMangementname']
        query = '''
            UPDATE Public_Mangement
            SET CentralMangementid = ?, PublicMangementname = ?
            WHERE PublicMangementid = ?
        '''
        execute_query(query, (CentralMangementid, PublicMangementname, PublicMangementid))
        return redirect(url_for('index'))
    
    public_mangement = execute_query("SELECT PublicMangementid, CentralMangementid, PublicMangementname FROM Public_Mangement", fetch=True)
    CentralizationMangement = execute_query("SELECT CentralMangementid, CentralMangementname FROM CentralizationMangement", fetch=True)
    return render_template('edit_Public_Mangement.html', public_mangement=public_mangement, CentralizationMangement=CentralizationMangement)

@app.route('/delete_Public_Mangement', methods=['GET', 'POST'])
def delete_Public_Mangement():
    if request.method == 'POST':
        PublicMangementid = request.form['PublicMangementid']
        query = "DELETE FROM Public_Mangement WHERE PublicMangementid = ?"
        execute_query(query, (PublicMangementid,))
        return redirect(url_for('index'))
    
    public_managements = execute_query("SELECT PublicMangementid, PublicMangementname FROM Public_Mangement", fetch=True)
    return render_template('delete_Public_Mangement.html', public_managements=public_managements)

@app.route('/add_TrainingProgram', methods=['GET', 'POST'])
def add_TrainingProgram():
    if request.method == 'POST':
        TrainerProgram_Id = request.form['TrainerProgram_Id']
        TrainerProgram_Name = request.form['TrainerProgram_Name']
        query = '''
            INSERT INTO TrainingProgram(TrainerProgram_Id, TrainerProgram_Name)
            VALUES (?, ?)
        '''
        execute_query(query, (TrainerProgram_Id, TrainerProgram_Name))
        return redirect(url_for('index'))
    return render_template('add_TrainingProgram.html')

@app.route('/edit_TrainingProgram', methods=['GET', 'POST'])
def edit_TrainingProgram():
    if request.method == 'POST':
        TrainerProgram_Id = request.form['TrainerProgram_Id']
        TrainerProgram_Name = request.form['TrainerProgram_Name']
        query = '''
            UPDATE TrainingProgram
            SET TrainerProgram_Name = ?
            WHERE TrainerProgram_Id = ?
        '''
        execute_query(query, (TrainerProgram_Name, TrainerProgram_Id))
        return redirect(url_for('index'))
    
    training_program = execute_query("SELECT TrainerProgram_Id, TrainerProgram_Name FROM TrainingProgram", fetch=True)
    return render_template('edit_TrainingProgram.html', training_program=training_program)

@app.route('/delete_TrainingProgram', methods=['GET', 'POST'])
def delete_TrainingProgram():
    if request.method == 'POST':
        TrainerProgram_Id = request.form['TrainerProgram_Id']
        query = "DELETE FROM TrainingProgram WHERE TrainerProgram_Id = ?"
        execute_query(query, (TrainerProgram_Id,))
        return redirect(url_for('index'))
    
    training_programs = execute_query("SELECT TrainerProgram_Id, TrainerProgram_Name FROM TrainingProgram", fetch=True)
    return render_template('delete_TrainingProgram.html', training_programs=training_programs)

@app.route('/add_attende', methods=['GET', 'POST'])
def add_attende():
    if request.method == 'POST':
        AbsenceId = request.form['AbsenceId']
        Attendedate = request.form['Attendedate']
        Nation_Trainee_Id = request.form['Nation_Trainee_Id']
        Course_Id = request.form['Course_Id']
        Countdayabbsent = request.form['Countdayabbsent']
        
        query = '''
            INSERT INTO Attende (AbsenceId, Attendedate, Nation_Trainee_Id, Course_Id, Countdayabbsent)
            VALUES (?, ?, ?, ?, ?)
        '''
        execute_query(query, (AbsenceId, Attendedate, Nation_Trainee_Id, Course_Id, Countdayabbsent))
        return redirect(url_for('index'))
    
    return render_template('add_attende.html')


@app.route('/edit_attende', methods=['GET', 'POST'])
def edit_attende():
    if request.method == 'POST':
        AbsenceId = request.form['AbsenceId']
        Attendedate = request.form['Attendedate']
        Nation_Trainee_Id = request.form['Nation_Trainee_Id']
        Course_Id = request.form['Course_Id']
        Countdayabbsent = request.form['Countdayabbsent']
        
        query = '''
            UPDATE Attende
            SET Attendedate = ?, Nation_Trainee_Id = ?, Course_Id = ?, Countdayabbsent = ?
            WHERE AbsenceId = ?
        '''
        execute_query(query, (Attendedate, Nation_Trainee_Id, Course_Id, Countdayabbsent, AbsenceId))
        return redirect(url_for('index'))
    
    absence_records = execute_query("SELECT AbsenceId, Attendedate, Nation_Trainee_Id, Course_Id, Countdayabbsent FROM Attende", fetch=True)
    return render_template('edit_attende.html', absence_records=absence_records)


@app.route('/delete_attende', methods=['GET', 'POST'])
def delete_attende():
    if request.method == 'POST':
        AbsenceId = request.form['AbsenceId']
        query = "DELETE FROM Attende WHERE AbsenceId = ?"
        execute_query(query, (AbsenceId,))
        return redirect(url_for('index'))
    
    absence_records = execute_query("SELECT AbsenceId, Attendedate FROM Attende", fetch=True)
    return render_template('delete_attende.html', absence_records=absence_records)

@app.route('/add_instructor', methods=['GET', 'POST'])
def add_instructor():
    if request.method == 'POST':
        Nation_Instructor_Id = request.form['Nation_Instructor_Id']
        Instructor_Name = request.form['Instructor_Name']
        Instructor_Mobile = request.form['Instructor_Mobile']
        Instructor_Bierthdate = request.form['Instructor_Bierthdate']
        Instructor_Email = request.form['Instructor_Email']
        
        query = '''
            INSERT INTO Instructor (Nation_Instructor_Id, Instructor_Name, Instructor_Mobile, Instructor_Bierthdate, Instructor_Email)
            VALUES (?, ?, ?, ?, ?)
        '''
        execute_query(query, (Nation_Instructor_Id, Instructor_Name, Instructor_Mobile, Instructor_Bierthdate, Instructor_Email))
        return redirect(url_for('index'))
    
    return render_template('add_instructor.html')


@app.route('/edit_instructor', methods=['GET', 'POST'])
def edit_instructor():
    if request.method == 'POST':
        Nation_Instructor_Id = request.form['Nation_Instructor_Id']
        Instructor_Name = request.form['Instructor_Name']
        Instructor_Mobile = request.form['Instructor_Mobile']
        Instructor_Bierthdate = request.form['Instructor_Bierthdate']
        Instructor_Email = request.form['Instructor_Email']
        
        query = '''
            UPDATE Instructor
            SET Instructor_Name = ?, Instructor_Mobile = ?, Instructor_Bierthdate = ?, Instructor_Email = ?
            WHERE Nation_Instructor_Id = ?
        '''
        execute_query(query, (Instructor_Name, Instructor_Mobile, Instructor_Bierthdate, Instructor_Email, Nation_Instructor_Id))
        return redirect(url_for('index'))
    
    instructors = execute_query("SELECT Nation_Instructor_Id, Instructor_Name, Instructor_Mobile, Instructor_Bierthdate, Instructor_Email FROM Instructor", fetch=True)
    return render_template('edit_instructor.html', instructors=instructors)


@app.route('/delete_instructor', methods=['GET', 'POST'])
def delete_instructor():
    if request.method == 'POST':
        Nation_Instructor_Id = request.form['Nation_Instructor_Id']
        query = "DELETE FROM Instructor WHERE Nation_Instructor_Id = ?"
        execute_query(query, (Nation_Instructor_Id,))
        return redirect(url_for('index'))
    
    instructors = execute_query("SELECT Nation_Instructor_Id, Instructor_Name FROM Instructor", fetch=True)
    return render_template('delete_instructor.html', instructors=instructors)

@app.route('/add_Course', methods=['GET', 'POST'])
def add_Course():
    connection = create_connection()
    if request.method == 'POST':
        Course_Id = request.form['Course_Id']
        TrainerProgram_Id = request.form['TrainerProgram_Id']
        Instructor_Id = request.form['Instructor_Id']
        Lab_Id = request.form['Lab_Id']
        Course_Cost = request.form['Course_Cost']
        CourseSessionCount = request.form['CourseSessionCount']
        CourseDays = request.form['CourseDays']
        CourseTimeFrom = request.form['CourseTimeFrom']
        CourseTimeTo = request.form['CourseTimeTo']
        CourseDateFrom = request.form['CourseDateFrom']
        CourseDateTo = request.form['CourseDateTo']
        TrainerProgram_Desc = request.form['TrainerProgram_Desc']

        query = '''
            INSERT INTO COURSE (Course_Id, TrainerProgram_Id, Instructor_Id, Lab_Id, Course_Cost, CourseSessionCount, CourseDays, 
                                CourseTimeFrom, CourseTimeTo, CourseDateFrom, CourseDateTo, TrainerProgram_Desc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        execute_query(query, (Course_Id, TrainerProgram_Id, Instructor_Id, Lab_Id, Course_Cost, CourseSessionCount, CourseDays,
                              CourseTimeFrom, CourseTimeTo, CourseDateFrom, CourseDateTo, TrainerProgram_Desc))
        return redirect(url_for('index'))

    # Fetching related tables to populate dropdowns
    TrainingPrograms = execute_query("SELECT TrainerProgram_Id, TrainerProgram_Name FROM TrainingProgram", fetch=True)
    instructors = execute_query("SELECT Nation_Instructor_Id, Instructor_Name FROM Instructor", fetch=True)
    labs = execute_query("SELECT Lab_Id, Lab_name FROM Lab", fetch=True)
    
    return render_template('add_Course.html', TrainingPrograms=TrainingPrograms, instructors=instructors, labs=labs)


@app.route('/edit_Course', methods=['GET', 'POST'])
def edit_Course():
    connection = create_connection()
    if request.method == 'POST':
        Course_Id = request.form['Course_Id']
        TrainerProgram_Id = request.form['TrainerProgram_Id']
        Instructor_Id = request.form['Instructor_Id']
        Lab_Id = request.form['Lab_Id']
        Course_Cost = request.form['Course_Cost']
        CourseSessionCount = request.form['CourseSessionCount']
        CourseDays = request.form['CourseDays']
        CourseTimeFrom = request.form['CourseTimeFrom']
        CourseTimeTo = request.form['CourseTimeTo']
        CourseDateFrom = request.form['CourseDateFrom']
        CourseDateTo = request.form['CourseDateTo']
        TrainerProgram_Desc = request.form['TrainerProgram_Desc']

        query = '''
            UPDATE COURSE 
            SET TrainerProgram_Id = ?, Instructor_Id = ?, Lab_Id = ?, Course_Cost = ?, CourseSessionCount = ?, 
                CourseDays = ?, CourseTimeFrom = ?, CourseTimeTo = ?, CourseDateFrom = ?, CourseDateTo = ?, TrainerProgram_Desc = ?
            WHERE Course_Id = ?
        '''
        execute_query(query, (TrainerProgram_Id, Instructor_Id, Lab_Id, Course_Cost, CourseSessionCount, CourseDays,
                              CourseTimeFrom, CourseTimeTo, CourseDateFrom, CourseDateTo, TrainerProgram_Desc, Course_Id))
        return redirect(url_for('index'))

    # Fetching all courses and related tables for editing
    Course = execute_query("SELECT * FROM COURSE WHERE Course_Id = ?", fetch=True)
    TrainingPrograms = execute_query("SELECT TrainerProgram_Id, TrainerProgram_Name FROM TrainingProgram", fetch=True)
    instructors = execute_query("SELECT Nation_Instructor_Id, Instructor_Name FROM Instructor", fetch=True)
    labs = execute_query("SELECT Lab_Id, Lab_name FROM Lab", fetch=True)
    
    return render_template('edit_Course.html', Course=Course, TrainingPrograms=TrainingPrograms, 
                           instructors=instructors, labs=labs)


@app.route('/delete_Course', methods=['GET', 'POST'])
def delete_Course():
    connection = create_connection()
    if request.method == 'POST':
        Course_Id = request.form['Course_Id']
        query = "DELETE FROM COURSE WHERE Course_Id = ?"
        execute_query(query, (Course_Id,))
        return redirect(url_for('index'))

    # Fetching all courses for deletion
    courses = execute_query("SELECT Course_Id, TrainerProgram_Desc FROM COURSE", fetch=True)
    return render_template('delete_Course.html', courses=courses)

@app.route('/add_Course_Result', methods=['GET', 'POST'])
def add_Course_Result():
    connection = create_connection()
    if request.method == 'POST':
        # Retrieving form data
        CourseTrainee_Id = request.form['CourseTrainee_Id']
        Nation_Trainee_Id = request.form['Nation_Trainee_Id']
        Course_Id = request.form['Course_Id']
        CTResult = request.form['CTResult']
        id = request.form['id']
        Train_id = request.form['Train_id']
        TrainerProgram_Id = request.form['TrainerProgram_Id']

        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    INSERT INTO Course_Result(CourseTrainee_Id, Nation_Trainee_Id, Course_Id, CTResult, id, Train_id, TrainerProgram_Id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
                cursor.execute(query, (CourseTrainee_Id, Nation_Trainee_Id, Course_Id, CTResult, id, Train_id, TrainerProgram_Id))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))  # Redirect to home or results page after insertion

    else:
        # Fetching the necessary data for drop-down lists
        courses = []
        trainees = []
        training_programs = []
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Course_Id, Course_Name FROM Course")
            courses = cursor.fetchall()  # Fixed variable name to 'courses'
            cursor.execute("SELECT Nation_Trainee_Id, Trainee_Name FROM Trainee")
            trainees = cursor.fetchall()  # Fixed variable name to 'trainees'
            cursor.execute("SELECT TrainerProgram_Id, TrainerProgram_Name FROM TrainingProgram")
            training_programs = cursor.fetchall()  # Fixed variable name to 'training_programs'
            cursor.close()
            connection.close()

        return render_template('add_Course_Result.html', courses=courses, trainees=trainees, training_programs=training_programs)

@app.route('/edit_Course_Result>', methods=['GET', 'POST'])
def edit_Course_Result():
    connection = create_connection()
    if request.method == 'POST':
        # Retrieving updated data from the form
        CourseTrainee_Id = request.form['CourseTrainee_Id']
        Nation_Trainee_Id = request.form['Nation_Trainee_Id']
        Course_Id = request.form['Course_Id']
        CTResult = request.form['CTResult']
        id = request.form['id']
        Train_id = request.form['Train_id']
        TrainerProgram_Id = request.form['TrainerProgram_Id']

        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    UPDATE Course_Result
                    SET Nation_Trainee_Id = ?, Course_Id = ?, CTResult = ?, id = ?, Train_id = ?, TrainerProgram_Id = ?
                    WHERE CourseTrainee_Id = ?
                '''
                cursor.execute(query, (CourseTrainee_Id,Nation_Trainee_Id, Course_Id, CTResult, id, Train_id, TrainerProgram_Id ))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))  # Redirect after updating

    else:
        # Fetch the current course result data to pre-fill the form
        course_result = None
        courses = []
        trainees = []
        training_programs = []
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Course_Result ")
            course_result = cursor.fetchone()
            cursor.execute("SELECT Course_Id  FROM Course")
            courses = cursor.fetchall()
            cursor.execute("SELECT Nation_Trainee_Id, Trainee_Name FROM Trainee")
            trainees = cursor.fetchall()
            cursor.execute("SELECT TrainerProgram_Id, TrainerProgram_Name FROM TrainingProgram")
            training_programs = cursor.fetchall()
            cursor.close()
            connection.close()

        return render_template('edit_Course_Result.html', course_result=course_result, courses=courses, trainees=trainees, training_programs=training_programs)

@app.route('/delete_Course_Result>', methods=['GET', 'POST'])
def delete_Course_Result():
    connection = create_connection()
    if request.method == 'POST':
        query = "DELETE FROM Course_Result WHERE CourseTrainee_Id = ?"
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (CourseTrainee_Id,))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        return redirect(url_for('index'))

    # Fetch the course result to be deleted for confirmation
    course_result = None
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Course_Result ")
        course_result = cursor.fetchone()
        cursor.close()
        connection.close()

    return render_template('delete_Course_Result.html', course_result=course_result)

@app.route('/add_in_out', methods=['GET', 'POST'])
def add_in_out():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    INSERT INTO in_out (id, name)
                    VALUES (?, ?)
                '''
                cursor.execute(query, (id, name))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    return render_template('add_in_out.html')

@app.route('/edit_in_out', methods=['GET', 'POST'])
def edit_in_out():
    connection = create_connection()
    if request.method == 'POST':
        id= request.form['id']
        name = request.form['name']

        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    UPDATE in_out
                    SET name = ?
                    WHERE id = ?
                '''
                cursor.execute(query, (name, id))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    
    else:
        in_out_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT id, name
                    FROM in_out
                    WHERE id = ?
                '''
                cursor.execute(query, (id,))
                in_out_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('edit_in_out.html', entry=in_out_entry)

@app.route('/delete_in_out>', methods=['POST', 'GET'])
def delete_in_out():
    connection = create_connection()
    if request.method == 'POST':
       
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    DELETE FROM in_out
                    WHERE id = ?
                '''
                cursor.execute(query, (id,))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        return redirect(url_for('index'))
    
    # If GET request, display the confirmation page
    else:
        in_out_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT id, name
                    FROM in_out
                    WHERE id = ?
                '''
                cursor.execute(query, (id,))
                in_out_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('delete_in_out.html', entry=in_out_entry)

@app.route('/add_lab', methods=['GET', 'POST'])
def add_lab():
    if request.method == 'POST':
        Lab_id = request.form['Lab_id']
        Lab_name = request.form['Lab_name']
        Lab_desc = request.form['Lab_desc']
        LabPc_count = request.form['LabPc_count']
        LabHasWhiteboard = request.form['LabHasWhiteboard']
        LabHasDataShow = request.form['LabHasDataShow']


        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    INSERT INTO lab(Lab_id, Lab_name,Lab_desc,LabPc_count,LabHasWhiteboard,LabHasDataShow)
                    VALUES (?, ?, ?, ?, ?, ?)
                '''
                cursor.execute(query, (Lab_id,Lab_name,Lab_desc,LabPc_count,LabHasWhiteboard,LabHasDataShow))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    return render_template('add_lab.html')


@app.route('/edit_lab', methods=['GET', 'POST'])
def edit_lab():
    connection = create_connection()
    if request.method == 'POST':
        Lab_id = request.form['Lab_id']
        Lab_name = request.form['Lab_name']
        Lab_desc = request.form['Lab_desc']
        LabPc_count = request.form['LabPc_count']
        LabHasWhiteboard = request.form['LabHasWhiteboard']
        LabHasDataShow = request.form['LabHasDataShow']

        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    UPDATE lab
                    SET Lab_name = ?, Lab_desc = ?, LabPc_count = ?, LabHasWhiteboard = ?, LabHasDataShow = ?
                    WHERE Lab_id = ?
                '''
                cursor.execute(query, (Lab_id,Lab_name, Lab_desc, LabPc_count, LabHasWhiteboard, LabHasDataShow ))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    
    else:
        lab_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT Lab_id, Lab_name, Lab_desc, LabPc_count, LabHasWhiteboard, LabHasDataShow
                    FROM lab
                    WHERE Lab_id = ?
                '''
                cursor.execute(query, (Lab_id,))
                lab_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('edit_lab.html', entry=lab_entry)

@app.route('/delete_lab', methods=['POST', 'GET'])
def delete_lab():
    connection = create_connection()
    if request.method == 'POST':
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    DELETE FROM lab
                    WHERE Lab_id = ?
                '''
                cursor.execute(query, (Lab_id,))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        return redirect(url_for('index'))
    
    else:
        lab_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT Lab_id, Lab_name, Lab_desc, LabPc_count, LabHasWhiteboard, LabHasDataShow
                    FROM lab
                    WHERE Lab_id = ?
                '''
                cursor.execute(query, (Lab_id,))
                lab_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('delete_lab.html', entry=lab_entry)

@app.route('/add_Permissions', methods=['GET', 'POST'])
def add_Permissions():
    if request.method == 'POST':
        PermissionId = request.form['PermissionId']
        PermissionType = request.form['PermissionType']

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    INSERT INTO Permissions(PermissionId, PermissionType)
                    VALUES (?, ?)
                '''
                cursor.execute(query, (PermissionId, PermissionType))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    return render_template('add_Permissions.html')

@app.route('/edit_Permissions', methods=['GET', 'POST'])
def edit_Permissions():
    connection = create_connection()
    if request.method == 'POST':
        PermissionId = request.form['PermissionId']
        PermissionType = request.form['PermissionType']

        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    UPDATE Permissions
                    SET PermissionType = ?
                    WHERE PermissionId = ?
                '''
                cursor.execute(query, (PermissionType, PermissionId))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    
    else:
        permission_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT PermissionId, PermissionType
                    FROM Permissions
                    WHERE PermissionId = ?
                '''
                cursor.execute(query, (PermissionId,))
                permission_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('edit_Permissions.html', entry=permission_entry)

@app.route('/delete_Permissions', methods=['POST', 'GET'])
def delete_Permissions():
    connection = create_connection()
    if request.method == 'POST':
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    DELETE FROM Permissions
                    WHERE PermissionId = ?
                '''
                cursor.execute(query, (PermissionId,))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        return redirect(url_for('index'))
    
    else:
        permission_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT PermissionId, PermissionType
                    FROM Permissions
                    WHERE PermissionId = ?
                '''
                cursor.execute(query, (PermissionId,))
                permission_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('delete_Permissions.html', entry=permission_entry)

@app.route('/add_UserPermissions', methods=['GET', 'POST'])
def add_UserPermissions():
    if request.method == 'POST':
        UserId = request.form['UserId']
        PermissionId = request.form['PermissionId']

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    INSERT INTO UserPermissions(UserId,PermissionId)
                    VALUES (?, ?)
                '''
                cursor.execute(query, (UserId,PermissionId))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    return render_template('add_UserPermissions.html')

@app.route('/edit_UserPermissions', methods=['GET', 'POST'])
def edit_UserPermissions():
    connection = create_connection()
    if request.method == 'POST':
        UserId = request.form['UserId']
        PermissionId = request.form['PermissionId']

        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    UPDATE UserPermissions
                    SET PermissionId = ?
                    WHERE UserId = ? AND PermissionId = ?
                '''
                cursor.execute(query, (new_PermissionId, UserId, PermissionId))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    
    else:
        user_permission = None
        permissions = []
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT UserId, PermissionId
                    FROM UserPermissions
                    WHERE UserId = ? AND PermissionId = ?
                '''
                cursor.execute(query, (UserId, PermissionId))
                user_permission = cursor.fetchone()
                cursor.execute("SELECT PermissionId, PermissionType FROM Permissions")
                permissions = cursor.fetchall()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('edit_UserPermissions.html', entry=user_permission, permissions=permissions)

@app.route('/delete_UserPermissions', methods=['POST', 'GET'])
def delete_UserPermissions():
    connection = create_connection()
    if request.method == 'POST':
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    DELETE FROM UserPermissions
                    WHERE UserId = ? AND PermissionId = ?
                '''
                cursor.execute(query, (UserId, PermissionId))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        return redirect(url_for('index'))
    
    else:
        user_permission = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT UserId, PermissionId
                    FROM UserPermissions
                    WHERE UserId = ? AND PermissionId = ?
                '''
                cursor.execute(query, (UserId, PermissionId))
                user_permission = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('delete_UserPermissions.html', entry=user_permission)

@app.route('/add_Users', methods=['GET', 'POST'])
def add_Users():
    if request.method == 'POST':
        UserId = request.form['UserId']
        UserName = request.form['UserName']
        UserRole = request.form['UserRole']
        Password = request.form['Password']

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    INSERT INTO Users(UserId,UserName,UserRole,Password)
                    VALUES (?, ?, ?, ?)
                '''
                cursor.execute(query, (UserId,UserName,UserRole,Password))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    return render_template('add_Users.html')

@app.route('/edit_Users', methods=['GET', 'POST'])
def edit_Users():
    connection = create_connection()
    if request.method == 'POST':
        UserId = request.form['UserId']
        UserName = request.form['UserName']
        UserRole = request.form['UserRole']
        Password = request.form['Password']

        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    UPDATE Users
                    SET UserName = ?, UserRole = ?, Password = ?
                    WHERE UserId = ?
                '''
                cursor.execute(query, (UserName, UserRole, Password, UserId))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for('index'))
    
    else:
        user_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT UserId, UserName, UserRole, Password
                    FROM Users
                    WHERE UserId = ?
                '''
                cursor.execute(query, (UserId,))
                user_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('edit_Users.html', entry=user_entry)

@app.route('/delete_Users', methods=['POST', 'GET'])
def delete_Users():
    connection = create_connection()
    if request.method == 'POST':
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    DELETE FROM Users
                    WHERE UserId = ?
                '''
                cursor.execute(query, (UserId,))
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        return redirect(url_for('index'))
    
    else:
        user_entry = None
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT UserId, UserName, UserRole, Password
                    FROM Users
                    WHERE UserId = ?
                '''
                cursor.execute(query, (UserId,))
                user_entry = cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        return render_template('delete_Users.html', entry=user_entry)



if __name__ == '__main__':
    app.run(debug=True)
