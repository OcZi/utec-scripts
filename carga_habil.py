"""
Carga hábil script:
    Load all pdf's tables and converts it to csv
    adapted to his format (the first table has the columns, other tables are extensions of it)
"""

import pandas as pd
import pdfplumber as reader
import os.path as fs

affirmative = ["true", "yes", "si", "sí"]
negative = ["false", "no"]

# Hardcoded names woo
pdf_input = "carga_habil.pdf"
csv_output = "carga_habil.csv"

if not fs.exists(pdf_input):
    print("No se ha encontrado el archivo", pdf_input, "en la carpeta")
    print("Saliendo...")
    exit(1)

if fs.exists(csv_output):
    print("Ya existe un", csv_output, "en la carpeta!")
    while (command := input("Desea sobreescribirlo? : ").lower()) not in affirmative:
        if command in negative:
            print("Saliendo...")
            exit(0)

        continue
    print("")

columns = None
values = []
with reader.open(pdf_input) as pdf:
    print(f"PDF cargado: {pdf_input} [{len(pdf.pages)}]")
    for num, page in enumerate(pdf.pages):
        table = page.extract_table()
        print(f"Procesando página {num + 1}...")
        # Only the first page has columns
        if num == 0:
            # Get first element as columns
            # and ignore it to process the rows
            columns = table[0]
            table = table[1:]

        for i, row in enumerate(table):
            for j in range(len(row)):
                # Remove newlines by pdf to avoid bad formatting with csv
                row[j] = row[j].replace("\n", " ")
            values.append(row)

print("")
if columns is None or len(values) == 0:
    print("No se pudo continuar! (no hay valores por procesar)")
else:
    result = pd.DataFrame(data=values, columns=columns)
    # Show complete table
    pd.set_option('display.max_rows', len(values) + 1)
    pd.set_option('display.max_columns', len(columns) + 1)
    pd.set_option('display.width', 1000)
    print("Resultado:")
    print(result)

    result.to_csv(csv_output)
    print("Resultado guardado en", csv_output)
