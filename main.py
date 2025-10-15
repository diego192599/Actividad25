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
                puntaje INTEGER
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS docentes (
                id_docente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                curso TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes_cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_estudiante INTEGER NOT NULL,
                id_curso INTEGER NOT NULL,
                FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
                FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
            );
        """)
        conn.commit()
        return conn

    # CRUD
    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO estudiantes (nombre, carrera, promedio) VALUES (?, ?, ?)",
                (self.nombre, self.carrera, self.promedio)
            )
        print(f" Estudiante '{self.nombre}' guardado con éxito.")

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
    def actualizar(id_estudiante, nombre, carrera, promedio):
        with Estudiante._conn() as conn:
            conn.execute("""
                UPDATE estudiantes SET nombre = ?, carrera = ?, promedio = ?
                WHERE id_estudiante = ?
            """, (nombre, carrera, promedio, id_estudiante))
        print(" Estudiante actualizado correctamente.")

    @staticmethod
    def eliminar(id_estudiante):
        with Estudiante._conn() as conn:
            conn.execute("DELETE FROM estudiantes WHERE id_estudiante = ?", (id_estudiante,))
        print(" Estudiante eliminado correctamente.")

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
    def __init__(self, nombre, puntaje):
        self.nombre = nombre
        self.puntaje = puntaje

    def guardar(self):
        with Estudiante._conn() as conn:
            conn.execute(
                "INSERT INTO cursos (nombre, puntaje) VALUES (?, ?)",
                (self.nombre, self.puntaje)
            )
        print(f" Curso '{self.nombre}' guardado con éxito.")

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
                print(f"ID: {f['id_curso']} | Nombre: {f['nombre']} | Puntaje: {f['puntaje']}")

    @staticmethod
    def actualizar(id_curso, nombre, puntaje):
        with Estudiante._conn() as conn:
            conn.execute("""
                UPDATE cursos SET nombre = ?, puntaje = ?
                WHERE id_curso = ?
            """, (nombre, puntaje, id_curso))
        print("Curso actualizado correctamente.")

    @staticmethod
    def eliminar(id_curso):
        with Estudiante._conn() as conn:
            conn.execute("DELETE FROM cursos WHERE id_curso = ?", (id_curso,))
        print(" Curso eliminado correctamente.")


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
        print(f" Docente '{self.nombre}' guardado con éxito.")

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

    @staticmethod
    def actualizar(id_docente, nombre, curso):
        with Estudiante._conn() as conn:
            conn.execute("""
                UPDATE docentes SET nombre = ?, curso = ?
                WHERE id_docente = ?
            """, (nombre, curso, id_docente))
        print(" Docente actualizado correctamente.")

    @staticmethod
    def eliminar(id_docente):
        with Estudiante._conn() as conn:
            conn.execute("DELETE FROM docentes WHERE id_docente = ?", (id_docente,))
        print(" Docente eliminado correctamente.")


class Inscripcion:
    @staticmethod
    def unir_estudiante_a_curso(id_estudiante, id_curso):
        with Estudiante._conn() as conn:
            cur_est = conn.execute("SELECT * FROM estudiantes WHERE id_estudiante = ?", (id_estudiante,))
            cur_cur = conn.execute("SELECT * FROM cursos WHERE id_curso = ?", (id_curso,))
            est = cur_est.fetchone()
            cur = cur_cur.fetchone()

            if not est:
                print(" Estudiante no encontrado.")
                return
            if not cur:
                print(" Curso no encontrado.")
                return

            cur_insc = conn.execute("""
                SELECT * FROM estudiantes_cursos
                WHERE id_estudiante = ? AND id_curso = ?
            """, (id_estudiante, id_curso))
            if cur_insc.fetchone():
                print(f" El estudiante '{est['nombre']}' ya está inscrito en '{cur['nombre']}'.")
                return

            conn.execute("""
                INSERT INTO estudiantes_cursos (id_estudiante, id_curso)
                VALUES (?, ?)
            """, (id_estudiante, id_curso))
            print(f" Estudiante '{est['nombre']}' se unió al curso '{cur['nombre']}'.")

    @staticmethod
    def listar_inscripciones():
        with Estudiante._conn() as conn:
            cur = conn.execute("""
                SELECT e.nombre AS estudiante, c.nombre AS curso
                FROM estudiantes_cursos ec
                JOIN estudiantes e ON e.id_estudiante = ec.id_estudiante
                JOIN cursos c ON c.id_curso = ec.id_curso
                ORDER BY e.nombre;
            """)
            filas = cur.fetchall()
            if not filas:
                print("No hay inscripciones registradas.")
                return
            print("\n--- INSCRIPCIONES ---")
            for f in filas:
                print(f"Estudiante: {f['estudiante']} | Curso: {f['curso']}")

    @staticmethod
    def eliminar_inscripcion(id_estudiante, id_curso):
        with Estudiante._conn() as conn:
            conn.execute("""
                DELETE FROM estudiantes_cursos
                WHERE id_estudiante = ? AND id_curso = ?
            """, (id_estudiante, id_curso))
        print("Inscripción eliminada correctamente.")


class MenuSistema:
    def __init__(self):
        pass

    def menu_principal(self):
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Estudiantes")
            print("2. Cursos")
            print("3. Docentes")
            print("4. Inscripciones")
            print("0. Salir")
            op = input("Opción: ")

            if op == "1":
                self.menu_estudiantes()
            elif op == "2":
                self.menu_cursos()
            elif op == "3":
                self.menu_docentes()
            elif op == "4":
                self.menu_inscripciones()
            elif op == "0":
                print("¡Hasta pronto!")
                break
            else:
                print("Opción inválida.")

    def menu_estudiantes(self):
        while True:
            print("\n--- MENÚ ESTUDIANTES ---")
            print("1. Agregar")
            print("2. Listar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Ver promedio general")
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
                Estudiante.listar()
                id_e = int(input("ID del estudiante: "))
                nombre = input("Nuevo nombre: ")
                carrera = input("Nueva carrera: ")
                promedio = float(input("Nuevo promedio: "))
                Estudiante.actualizar(id_e, nombre, carrera, promedio)
            elif op == "4":
                Estudiante.listar()
                id_e = int(input("ID del estudiante a eliminar: "))
                Estudiante.eliminar(id_e)
            elif op == "5":
                Estudiante.promedio_general()
            elif op == "0":
                break
            else:
                print("Opción inválida.")

    def menu_cursos(self):
        while True:
            print("\n--- MENÚ CURSOS ---")
            print("1. Agregar")
            print("2. Listar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Opción: ")

            if op == "1":
                nombre = input("Nombre del curso: ")
                puntaje = int(input("Puntaje para ganar el curso: "))
                Curso(nombre, puntaje).guardar()
            elif op == "2":
                Curso.listar()
            elif op == "3":
                Curso.listar()
                id_c = int(input("ID del curso: "))
                nombre = input("Nuevo nombre: ")
                puntaje = int(input("Nuevo puntaje: "))
                Curso.actualizar(id_c, nombre, puntaje)
            elif op == "4":
                Curso.listar()
                id_c = int(input("ID del curso a eliminar: "))
                Curso.eliminar(id_c)
            elif op == "0":
                break
            else:
                print("Opción inválida.")

    def menu_docentes(self):
        while True:
            print("\n--- MENÚ DOCENTES ---")
            print("1. Agregar")
            print("2. Listar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Opción: ")

            if op == "1":
                nombre = input("Nombre del docente: ")
                curso = input("Curso que imparte: ")
                Docente(nombre, curso).guardar()
            elif op == "2":
                Docente.listar()
            elif op == "3":
                Docente.listar()
                id_d = int(input("ID del docente: "))
                nombre = input("Nuevo nombre: ")
                curso = input("Nuevo curso: ")
                Docente.actualizar(id_d, nombre, curso)
            elif op == "4":
                Docente.listar()
                id_d = int(input("ID del docente a eliminar: "))
                Docente.eliminar(id_d)
            elif op == "0":
                break
            else:
                print("Opción inválida.")

    def menu_inscripciones(self):
        while True:
            print("\n--- MENÚ INSCRIPCIONES ---")
            print("1. Unir estudiante a curso")
            print("2. Listar inscripciones")
            print("3. Eliminar inscripción")
            print("0. Volver")
            op = input("Opción: ")

            if op == "1":
                Estudiante.listar()
                id_est = int(input("ID del estudiante: "))
                Curso.listar()
                id_curso = int(input("ID del curso: "))
                Inscripcion.unir_estudiante_a_curso(id_est, id_curso)
            elif op == "2":
                Inscripcion.listar_inscripciones()
            elif op == "3":
                Estudiante.listar()
                id_est = int(input("ID del estudiante: "))
                Curso.listar()
                id_curso = int(input("ID del curso: "))
                Inscripcion.eliminar_inscripcion(id_est, id_curso)
            elif op == "0":
                break
            else:
                print("Opción inválida.")


if __name__ == "__main__":
    menu = MenuSistema()
    menu.menu_principal()
