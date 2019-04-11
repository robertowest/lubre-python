import sqlite3

try:
    # conn = sqlite3.connect("db.sqlite3")
    # print("Base de datos abierta correctamente")
    # db = sqlite3.connect(":memory")
    db = sqlite3.connect("libros.sqlite3")

except sqlite3.OperationalError as error:
    print("Error al abrir:", error)


def tabla():
    try:
        cursor = bd.cursor()
        tablas = [
            """
                CREATE TABLE IF NOT EXISTS autor(
                    nombre TEXT NOT NULL,
                );
                CREATE TABLE IF NOT EXISTS genero(
                    nombre TEXT NOT NULL,
                );
                CREATE TABLE IF NOT EXISTS libros(
                    autor TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    precio REAL NOT NULL,
                    titulo REAL NOT NULL
                );
            """
        ]
        for tabla in tablas:
            cursor.execute(tabla);
        print("Tablas creadas correctamente")

    except sqlite3.OperationalError as error:
        print("Error:", error)

def datos_iniciales():
    try:
        cursor = bd.cursor()
        libros = [
                """
            INSERT INTO libros (autor, genero, precio, titulo)
            VALUES
            ('Stephen King', 'Terror', 115,'Cementerio de animales'),
            ('Alfred Bester', 'Ciencia ficción', 200,'Las estrellas, mi destino'),
            ('Margaret Atwood', 'Ciencia ficción', 150,'El cuento de la criada');
            """
            ]
        for sentencia in libros:
            cursor.execute(sentencia)

        bd.commit()  # guardamos los cambios al terminar el ciclo
        print("Libros insertados correctamente")

    except sqlite3.OperationalError as error:
        print("Error:", error)

def nuevo_libro():      
    print("Nuevo Libro")
    print("-----------")
    print("")

    cursor = db.cursor()

    autor = input("Autor: ")
    genero = input("Género: ")
    precio = input("Precio: ")
    titulo = input("Título: ")

    sentencia = "INSERT INTO libros(autor, genero, precio, titulo) VALUES (?,?,?,?)"
        cursor.execute(sentencia, [autor, genero, precio, titulo])

        db.commit()
        print("Los datos fueron agregados correctamente")
        cursor.close()
