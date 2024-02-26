import sqlite3
from passlib.hash import pbkdf2_sha256

conn = sqlite3.connect('db_clinica')

# conn.execute('''CREATE TABLE IF NOT EXISTS PATIENT
#                 (ID INTEGER PRIMARY KEY NOT NULL,
#                 NAME TEXT NOT NULL,
#                 LAST_NAME TEXT NOT NULL,
#                 BIRTHDATE DATE NOT NULL,
#                 ADDRESS TEXT NOT NULL);''')
#
# conn.execute('''CREATE TABLE IF NOT EXISTS APPOINTMENT
#                 (ID_APPO INTEGER PRIMARY KEY AUTOINCREMENT,
#                 ID_PATIENT INTEGER,
#                 APPO_DATE DATE NOT NULL,
#                 TIME TEXT NOT NULL,
#                 REASON TEXT NOT NULL,
#                 FOREIGN KEY (ID_PATIENT) REFERENCES PATIENT(ID));''')
# conn.commit()
# print('hecho')

# conn.execute('''CREATE TABLE IF NOT EXISTS USER_DATA
#                 (USERNAME TEXT PRIMARY KEY NOT NULL,
#                 PASSWORD TEXT NOT NULL);''')
#



# def register_user(username, password):
#     try:
#         password_hash = pbkdf2_sha256.hash(password)  # Generar el hash de la contraseña
#
#         conn.execute('INSERT INTO USER_DATA (USERNAME, PASSWORD) VALUES (?, ?)', (username, password_hash))
#         conn.commit()
#         conn.close()
#
#         print("Usuario registrado con éxito")
#     except Exception as e:
#         print("Error al registrar el usuario:", e)
#
# # Registrar un nuevo usuario
# register_user('admin_Admin', 'admin456')




