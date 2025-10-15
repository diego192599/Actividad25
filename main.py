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
    def modificar():
        ide = input("Ingrese ID del estudiante a modificar: ")
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM estudiantes WHERE id_estudiante = ?", (ide,))
            fila = cur.fetchone()
            if not fila:
                print("No se encontró el estudiante.")
                return
            nombre = input(f"Nuevo nombre [{fila['nombre']}]: ") or fila['nombre']
            carrera = input(f"Nueva carrera [{fila['carrera']}]: ") or fila['carrera']
            promedio = input(f"Nuevo promedio [{fila['promedio']}]: ") or fila['promedio']
            conn.execute("UPDATE estudiantes SET nombre=?, carrera=?, promedio=? WHERE id_estudiante=?",
                         (nombre, carrera, promedio, ide))
        print("Estudiante actualizado con éxito.")

    @staticmethod
    def eliminar():
        ide = input("Ingrese ID del estudiante a eliminar: ")
        with Estudiante._conn() as conn:
            cur = conn.execute("DELETE FROM estudiantes WHERE id_estudiante = ?", (ide,))
            if cur.rowcount == 0:
                print("No se encontró el estudiante.")
            else:
                print("Estudiante eliminado con éxito.")

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
    def __init__(self,nombre,puntaje):
        self.nombre=nombre
        self.puntaje=puntaje

    def guardar(self):
        with Estudiante._conn() as conn:
            conn.execute(
                "INSERT INTO cursos (nombre, creditos) VALUES (?, ?)",
                (self.nombre, self.puntaje)
            )
            print(f"Curso '{self.nombre}' guardado con éxito.")
    @staticmethod
    def listar():
        with Estudiante._conn() as conn:
            cur=conn.execute("SELECT * FRON cursos")
            fila=cur.fetchall()
            if not fila:
                print("No hay lista de cursos")
                return
            print("\n ---Lista de cursos---")
            for f in fila:
                print(f"ID: {f['id_curso']} | Nombre: {f['nombre']} | Créditos: {f['creditos']}")

class Docente:
    def __init__(self,id_docente,nombre,curso):
        self.id_docente=id_docente
        self.nombre=nombre
        self.curso=curso

    def guardar(self):
        with Estudiante._conn() as conn:
            conn.execute(
                "INSERT INTO Docente(id_docente,nombre,curso) VALUES (?, ?, ?)",
                (self.nombre,self.nombre,self.curso)
            )
            print(f"Docente {self.nombre} guardado correctamente")


    @staticmethod
    def listar_doce():
        with Estudiante._conn() as conn:
            doce=conn.execute("SELECT * FROM Docente")
            fila=doce.fetchall()
            if not fila:
                print("No hay ningun docente registrado")
                return
            print("\n Lista de docentes")
            for f in fila:
                print(f"ID: {f['id_docente']} | Nombre: {f['nombre']} | Curso: {f['curso']}")

# --- MENÚ PRINCIPAL ---
class MenuSistema:
    def __init__(self):
        pass

    def menu_estudiantes(self):
        while True:
            print("\n--- MENÚ ESTUDIANTES ---")
            print("1. Agregar estudiante")
            print("2. Listar estudiantes")
            print("3. Asignar estudiante a curso")
            print("4. Ver cursos asignados")
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
                Estudiante.asignar_a_curso()
            elif op == "4":
                Estudiante.ver_cursos()
            elif op == "5":
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
    menu()
