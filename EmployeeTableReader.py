import FreeSimpleGUI as sg
import mysql.connector

def get_employees():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Luca$Mertducks0414",
        database="lukes_lasagna"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    headers = [col[0] for col in cursor.description]

    cursor.close()
    conn.close()

    return headers, rows

# ---------- INITIAL DATA LOAD ----------

headers, rows = get_employees()
table_data = [[str(cell) for cell in row] for row in rows]

layout = [
    [sg.Text("Employees Table Viewer", font=("Arial", 16))],
    [sg.Table(
        values=table_data,
        headings=headers,
        auto_size_columns=True,
        display_row_numbers=False,
        justification="left",
        num_rows=20,
        key="-TABLE-",
        enable_events=True,
        expand_x=True,
        expand_y=True
    )],
    [sg.Button("Refresh"), sg.Button("Exit")]
]

window = sg.Window("MySQL Employees Viewer", layout, resizable=True)

while True:
    event, values = window.read()

    if event in (None, "Exit"):
        break

    if event == "Refresh":
        headers, rows = get_employees()
        table_data = [[str(cell) for cell in row] for row in rows]
        window["-TABLE-"].update(values=table_data)  # <-- no headings here

window.close()