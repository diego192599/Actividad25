import sqlite3

DB_NAME = "estudiantes.db"

class Estudiante:
    def __init__(self, nombre, carrera, promedio):
        self.nombre = nombre
        self.carrera = carrera
        self.promedio = promedio

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                carrera TEXT NOT NULL,
                promedio REAL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                creditos INTEGER
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS docentes (
                id_docente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                curso TEXT NOT NULL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO estudiantes (nombre, carrera, promedio) VALUES (?, ?, ?)",
                (self.nombre, self.carrera, self.promedio)
            )
        print(f"Estudiante '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar():
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM estudiantes")
            filas = cur.fetchall()
            if not filas:
                print("No hay estudiantes registrados.")
                return
            print("\n--- LISTADO DE ESTUDIANTES ---")
            for f in filas:
                print(f"ID: {f['id_estudiante']} | Nombre: {f['nombre']} | Carrera: {f['carrera']} | Promedio: {f['promedio']}")

    @staticmethod
    def promedio_general():
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT AVG(promedio) AS prom FROM estudiantes")
            prom = cur.fetchone()["prom"]
            if prom:
                print(f"\nPromedio general: {prom:.2f}")
            else:
                print("No hay datos para calcular el promedio.")


class Curso:
    def __init__(self, nombre, creditos):
        self.nombre = nombre
        self.creditos = creditos

    def guardar(self):
        with Estudiante._conn() as conn:
            conn.execute(
                "INSERT INTO cursos (nombre, creditos) VALUES (?, ?)",
                (self.nombre, self.creditos)
            )
        print(f"Curso '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar():
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM cursos")
            filas = cur.fetchall()
            if not filas:
                print("No hay cursos registrados.")
                return
            print("\n--- LISTA DE CURSOS ---")
            for f in filas:
                print(f"ID: {f['id_curso']} | Nombre: {f['nombre']} | Créditos: {f['creditos']}")

class Docente:
    def __init__(self, nombre, curso):
        self.nombre = nombre
        self.curso = curso

    def guardar(self):
        with Estudiante._conn() as conn:
            conn.execute(
                "INSERT INTO docentes (nombre, curso) VALUES (?, ?)",
                (self.nombre, self.curso)
            )
        print(f"Docente '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar():
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM docentes")
            filas = cur.fetchall()
            if not filas:
                print("No hay docentes registrados.")
                return
            print("\n--- LISTA DE DOCENTES ---")
            for f in filas:
                print(f"ID: {f['id_docente']} | Nombre: {f['nombre']} | Curso: {f['curso']}")

class MenuSistema:
    def __init__(self):
        pass

    def menu_principal(self):
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Estudiantes")
            print("2. Cursos")
            print("3. Docentes")
            print("0. Salir")
            op = input("Opción: ")
            if op == "1":
                self.menu_estudiantes()
            elif op == "2":
                self.menu_cursos()
            elif op == "3":
                self.menu_docentes()
            elif op == "0":
                print("¡Hasta pronto!")
                break
            else:
                print("Opción inválida.")

    def menu_estudiantes(self):
        while True:
            print("\n--- MENÚ ESTUDIANTES ---")
            print("1. Agregar estudiante")
            print("2. Listar estudiantes")
            print("3. Ver promedio general")
            print("0. Volver")
            op = input("Opción: ")

            if op == "1":
                nombre = input("Nombre: ")
                carrera = input("Carrera: ")
                promedio = float(input("Promedio: "))
                Estudiante(nombre, carrera, promedio).guardar()
            elif op == "2":
                Estudiante.listar()
            elif op == "3":
                Estudiante.promedio_general()
            elif op == "0":
                break
            else:
                print("Opción inválida.")

    def menu_cursos(self):
        while True:
            print("\n--- MENÚ CURSOS ---")
            print("1. Agregar curso")
            print("2. Listar cursos")
            print("0. Volver")
            op = input("Opción: ")

            if op == "1":
                nombre = input("Nombre del curso: ")
                creditos = int(input("Créditos: "))
                Curso(nombre, creditos).guardar()
            elif op == "2":
                Curso.listar()
            elif op == "0":
                break
            else:
                print("Opción inválida.")

    def menu_docentes(self):
        while True:
            print("\n--- MENÚ DOCENTES ---")
            print("1. Agregar docente")
            print("2. Listar docentes")
            print("0. Volver")
            op = input("Opción: ")

            if op == "1":
                nombre = input("Nombre del docente: ")
                curso = input("Curso que imparte: ")
                Docente(nombre, curso).guardar()
            elif op == "2":
                Docente.listar()
            elif op == "0":
                break
            else:
                print("Opción inválida.")

if __name__ == "__main__":
    menu = MenuSistema()
    menu.menu_principal()