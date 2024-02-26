from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = 'YfeItpdUsWnmgfQ'

@app.route('/', methods=["GET"])
def index():
    return render_template('login.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form['username']
            password = request.form['password']

            with sql.connect('db_clinica') as con:
                cur = con.cursor()
                password_hash = cur.execute('SELECT PASSWORD FROM USER_DATA WHERE USERNAME = ?',(username,)).fetchone()
                if password_hash and pbkdf2_sha256.verify(password, password_hash[0]):
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('login.html', error='Credenciales invalidas')
        except:
            return render_template('login.html', error='Credenciales invalidas')
    return render_template('login.html')


@app.route('/dash', methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        opcion = int(request.form['opcion'])
        if opcion == 1:
            return render_template('dashboard.html')
        elif opcion == 2:
            return redirect(url_for('appointment_form'))
        elif opcion == 3:
            return redirect(url_for('patient_form'))
        else:
            return render_template('dashboard.html')
    return render_template('dashboard.html')

@app.route('/patient', methods=["GET", "POST"])
def patient_form():
    return render_template('patient.html')

@app.route('/patient/search', methods=["GET", "POST"])
def search_patient():
    if request.method == 'POST':
        try:
            name_last_name = request.form['name_last_name']
            name, last_name = name_last_name.split()

            with sql.connect('db_clinica') as con:
                cur = con.cursor()
                review = cur.execute('SELECT * FROM PATIENT WHERE NAME = ? AND LAST_NAME = ?', (name,last_name)).fetchone()
                if review:
                    return render_template('patient.html', review=review)
                else:
                    return render_template('patient.html', error='paciente no encontrado')
        except:
            return render_template('patient.html', error='paciente no encontrado')
    return render_template('patient.html')


@app.route('/patient/add', methods=["GET", "POST"])
def add_patient():
    if request.method == 'POST':
        try:
            name = request.form['name']
            last_name = request.form['last_name']
            id = request.form['id']
            birthdate = request.form['birthdate']
            address = request.form['address']

            with sql.connect('db_clinica') as con:
                cur = con.cursor()
                review = cur.execute('SELECT * FROM PATIENT WHERE ID = ?', (id,)).fetchone()
                if review:
                    return render_template('add_patient.html', error='registrado anteriormente')
                else:
                    insert = cur.execute('INSERT INTO PATIENT (name, last_name, id, birthdate, address) VALUES (?, ?, ?, ?, ?)', (name, last_name, id, birthdate, address))
                    con.commit()
                    return render_template('patient.html', msg='paciente registrado con exito')
        except:
            return render_template(error= 'No se agrego el paciente correctamente')
    return render_template('add_patient.html')


@app.route('/patient/edit', methods=["GET", "POST"])
def edit_patient():
    if request.method == 'POST':
        try:
            column_update = request.form['column_update']
            new_data = request.form['new_data']
            name = request.form['name']
            last_name = request.form['last_name']
            birthdate = request.form['birthdate']
            id = request.form['id']
            address = request.form['address']

            with sql.connect('db_clinica') as con:
                cur = con.cursor()
                update = cur.execute(f'UPDATE PATIENT SET {column_update} = ? WHERE NAME = ? AND LAST_NAME = ? AND BIRTHDATE = ? AND ID = ? AND ADDRESS = ?', (new_data, name, last_name, birthdate, id, address))
                con.commit()
                return render_template('patient.html', update=update)
        except:
            return render_template('patient.html', error= 'No se edito el paciente correctamente')
    return render_template('patient.html')

@app.route('/patient/delete', methods=['POST'])
def delete_patient():
    try:
        name = request.form['name']
        last_name = request.form['last_name']

        with sql.connect('db_clinica') as con:
            cur = con.cursor()
            delete = con.execute('DELETE FROM PATIENT WHERE NAME = ? AND LAST_NAME = ?', (name, last_name))
            con.commit()
        return render_template('patient.html')
    except:
        return render_template('patient.html', error= 'No se elimino el paciente correctamente')


@app.route('/appointment', methods=["GET"])
def appointment_form():
    return render_template('appointment.html')

@app.route('/appointment/search', methods=["GET", "POST"])
def search_appointment():
    if request.method == 'POST':
        try:
            name_last_name = request.form['name_last_name']
            name, last_name = name_last_name.split()

            with sql.connect('db_clinica') as con:
                cur = con.cursor()
                review_id = cur.execute('SELECT ID FROM PATIENT WHERE NAME = ? AND LAST_NAME = ?', (name, last_name)).fetchone()
                if review_id:
                    id_patient = review_id[0]
                    appo_review = cur.execute('SELECT * FROM APPOINTMENT WHERE ID_PATIENT = ?', (id_patient,)).fetchone()
                    if appo_review:
                        return render_template('appointment.html', name_last_name=name_last_name, appo_review=appo_review)
                    else:
                        return render_template('appointment.html', error= 'No se encontraron citas agendadas')
                else:
                    return render_template('appointment.html')
        except:
            return render_template('appointment.html', error= 'No se encontro el paciente')
    return render_template('appointment.html')
@app.route('/appointment/add', methods=["GET", "POST"])
def add_appointment():
    if request.method == 'POST':
        try:
            name_last_name = request.form['name_last_name']
            name, last_name = name_last_name.split()
            appo_date = request.form['appo_date']
            time = request.form['time']
            reason = request.form['reason']

            with sql.connect('db_clinica') as con:
                cur = con.cursor()
                patient_id = cur.execute('SELECT ID FROM PATIENT WHERE NAME = ? AND LAST_NAME = ?', (name, last_name)).fetchone()
                if patient_id:
                    exist_appo = cur.execute('SELECT * FROM APPOINTMENT WHERE APPO_DATE = ? AND TIME = ?',(appo_date, time)).fetchone()
                    if exist_appo:
                        return render_template('add_appointment.html', msg='Ya hay una cita registrada en ese horario.')
                    else:
                        insert = cur.execute('INSERT INTO APPOINTMENT (ID_PATIENT, APPO_DATE, TIME, REASON) VALUES (?, ?, ?, ?)', (patient_id[0], appo_date, time, reason))
                        con.commit()
                    return render_template('appointment.html', msg='Cita agregada con éxito')
                else:
                    return render_template('add_appointment.html', msg='Paciente no encontrado')
        except:
            return render_template('add_appointment.html', msg= 'La cita no se agrego correctamente')
    return render_template('add_appointment.html')

@app.route('/appointment/edit', methods= ["GET", "POST"])
def edit_appointment():
    if request.method == "POST":
        try:
            column_update = request.form['column_update']
            new_data = request.form['new_data']
            name_last_name = request.form['name_last_name']
            name, last_name = name_last_name.split()
            appo_date = request.form['appo_date']
            time = request.form['time']
            reason = request.form['reason']

            with sql.connect('db_clinica') as con:
                cur = con.cursor()
                update = cur.execute(f'UPDATE APPOINTMENT SET {column_update} = ? WHERE APPO_DATE = ? AND TIME = ? AND REASON = ?', (new_data, appo_date, time, reason))
                con.commit()
                return render_template('appointment.html', update=update)
        except:
            return render_template('appointment.html', error='No se edito la cita correctamente')
    return render_template('appointment.html')

@app.route('/appointment/delete', methods=["POST"])
def delete_appointment():
    try:
        name = request.form['name']
        last_name = request.form['last_name']

        with sql.connect('db_clinica.db') as con:
            cur = con.cursor()
            patient_id = cur.execute('SELECT ID FROM PATIENT WHERE NAME = ? AND LAST_NAME = ?', (name, last_name)).fetchone()
            if patient_id:
                id_patient = patient_id[0]
                exist_appo = cur.execute('SELECT ID FROM APPOINTMENT WHERE ID_PATIENT = ?', (id_patient,)).fetchone()
                if exist_appo:
                    delete = cur.execute('DELETE FROM APPOINTMENT WHERE ID_PATIENT = ?', (id_patient,))
                    con.commit()
                    return render_template('appointment.html', msg='Cita eliminada')
                else:
                    return render_template('appointment.html', msg='Cita NO eliminada')
            else:
                return render_template('appointment.html', msg='Cita NO encontrada')
    except:
        return render_template('appointment.html', error='No se elimino correctamente')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
