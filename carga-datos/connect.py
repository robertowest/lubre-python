import sqlite3

try:
    conn = sqlite3.connect("db.sqlite3")
    print("Base de datos abierta correctamente")

except sqlite3.OperationalError as error:
    print("Error al abrir:", error)
