"""
Search hábil script:
    Load a "carga_habil.csv" to do search operations.
"""

import os.path as fs

import fire
import pandas as pd

days_week = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]

csv_input = "carga_habil.csv"


def __show_schedule__(schedule_map, title=None):
    if title is None:
        title = f"Horarios [{len(schedule_map)}]"
    print(title)
    for day, hours in schedule_map.items():
        print(f"  {day}:")
        for hora in hours:
            print(f"  - {hora}")


def __sort_schedule__(schedule_map: dict, index: int):
    return dict(sorted(schedule_map.items(), key=lambda item: days_week.index(item[index])))


class CursoHabil:

    def __init__(self):
        if not fs.exists(csv_input):
            print("CSV", csv_input, "no encontrado en la carpeta")
            print("Saliendo...")
            exit(1)
        self.data = pd.read_csv(csv_input, index_col=False)

    def courses(self):
        course_set = self.data["Curso"].unique()
        print(f"Cursos disponibles [{len(course_set)}]:")
        for curso in course_set:
            print(f"- {curso}")

    def rows(self, course: str, cli: bool = True) -> pd.DataFrame | None:
        rows = self.data.loc[self.data["Curso"] == course]
        if cli:
            print(f"Entradas de {course}:")
            print(rows)
            return None

        return rows

    def sections(self, course: str):
        rows = self.rows(course, cli=False)
        total_sections = max(rows["Sección"].unique())
        print(f"Secciones: {total_sections}")

    def teachers(self, course: str):
        rows = self.data.loc[self.data["Curso"] == course]
        teachers = rows["Docente"].unique()
        print(f"Docentes [{len(teachers)}]:")
        for teacher in teachers:
            sections = self.data.loc[self.data["Docente"] == teacher]["Sesión Grupo"]
            if type(teacher) is float:
                teacher = "*Vacante abierta"
            print(f"- {teacher}", f"({len(sections)} secciones)")

    def schedules(self, course: str):
        rows = self.rows(course, cli=False)
        sub_rows = rows[["Docente", "Sesión Grupo", "Horario"]]
        schedule_map = dict()
        values = sorted(sub_rows.values, key=lambda value: value[2][5:])
        for row in values:
            professor = row[0]
            section = row[1]
            schedule = row[2]
            day = schedule[:3]
            if day not in schedule_map:
                schedule_map[day] = []
            schedule_map[day].append(f"{schedule[5:]} -> {professor} ({section})")

        __show_schedule__(__sort_schedule__(schedule_map, 0))

    def teacher_schedules(self, teacher: str, course: str):
        rows = self.rows(course, cli=False)
        sub_rows = rows[["Docente", "Sesión Grupo", "Horario"]]
        sub_rows: pd.DataFrame = sub_rows.loc[sub_rows["Docente"] == teacher]

        schedule_map = dict()
        for entrada in sub_rows.values:
            horario = entrada[2]
            day = horario[:3]
            if day not in schedule_map:
                schedule_map[day] = []
            schedule_map[day].append(horario[5:] + ": " + entrada[1])

        __show_schedule__(schedule_map, f"Horarios - {teacher} [{len(schedule_map)}]")


if __name__ == "__main__":
    fire.Fire(CursoHabil)
