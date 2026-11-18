import FreeSimpleGUI as sg
import mysql.connector
import db


def fetch_table(table_name):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    headings = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return rows, headings


def updateData(row_data, headings):
    """
    Edit a single row in `tables`.
    PK (table_id) is read-only.
    server_id is nullable → blank becomes NULL.
    """
    layout = [
        [sg.Text("Editing selected table")],
        [sg.Text(f"{headings[0]} (table_id): {row_data[0]}")],
    ]

    for i, col_name in enumerate(headings[1:], start=1):
        layout.append(
            [
                sg.Text(col_name + ":", size=(20, 1)),
                sg.Input(
                    default_text=row_data[i] if row_data[i] is not None else "",
                    key=f"-EDIT-{col_name}-",
                ),
            ]
        )

    layout.append([sg.Button("FINISH"), sg.Button("Cancel")])

    win = sg.Window("UPDATE TABLE", layout, modal=True)
    result = None

    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            edited = {}
            for col in headings[1:]:
                val = values[f"-EDIT-{col}-"]
                if col == "server_id":
                    val = val.strip()
                    val = val if val != "" else None
                edited[col] = val
            result = edited
            break

    win.close()
    return result


def addData():
    """
    Add a new row to `tables`.
    table_id is auto-increment; user enters:
      - server_id (optional)
      - table_seats (required)
      - table_notes (optional)
    """
    layout = [
        [sg.Text("server_id (optional):"), sg.Input(key="-SERVER-")],
        [sg.Text("table_seats:"), sg.Input(key="-SEATS-")],
        [sg.Text("table_notes:")],
        [sg.Multiline(key="-NOTES-", size=(40, 5))],
        [sg.Button("FINISH"), sg.Button("Cancel")],
    ]

    win = sg.Window("ADD TABLE", layout, modal=True)
    result = None

    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == "FINISH":
            result = values
            break

    win.close()
    return result


def main():
    table_name = "tables"  # exact name from your CREATE TABLE
    data, headings = fetch_table(table_name)

    layout = [
        [sg.Table(
            values=data,
            headings=headings,
            auto_size_columns=True,
            display_row_numbers=False,
            justification="left",
            num_rows=20,
            key="-TABLE-",
            enable_events=True,
            select_mode=sg.SELECT_MODE_BROWSE,
        )],
        [sg.Button("ADD"), sg.Button("UPDATE"), sg.Button("DELETE")],
        [sg.Button("REFRESH")],
    ]

    window = sg.Window("Tables", layout, resizable=True, size=(800, 500))

    selected_row_index = None

    while True:
        event, values = window.read()

        # track selected row
        if event == "-TABLE-":
            sel = values["-TABLE-"]
            selected_row_index = sel[0] if sel else None

        # ---------- ADD ----------
        if event == "ADD":
            vals = addData()
            if vals is not None:
                conn = db.get_connection()
                cursor = conn.cursor()

                server_raw = vals["-SERVER-"].strip()
                server_val = server_raw if server_raw != "" else None

                sql = """
                    INSERT INTO tables
                    (server_id, table_seats, table_notes)
                    VALUES (%s, %s, %s)
                """
                params = (
                    server_val,
                    vals["-SEATS-"],
                    vals["-NOTES-"],
                )

                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()

            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        # ---------- UPDATE ----------
        if event == "UPDATE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to update.")
            else:
                row_data = data[selected_row_index]
                edited = updateData(row_data, headings)

                if edited is not None:
                    pk_col = headings[0]  # table_id
                    pk_val = row_data[0]

                    cols = headings[1:]
                    set_clause = ", ".join(f"{col} = %s" for col in cols)
                    sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_col} = %s"

                    params = [edited[col] for col in cols] + [pk_val]

                    conn = db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(sql, params)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)
                    if 0 <= selected_row_index < len(data):
                        window["-TABLE-"].update(select_rows=[selected_row_index])

        # ---------- DELETE ----------
        if event == "DELETE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to delete.")
            else:
                row_data = data[selected_row_index]
                pk_col = headings[0]
                pk_val = row_data[0]

                confirm = sg.popup_yes_no(
                    f"Delete this table record?\n\n{row_data}"
                )
                if confirm == "Yes":
                    conn = db.get_connection()
                    cursor = conn.cursor()
                    sql = f"DELETE FROM {table_name} WHERE {pk_col} = %s"
                    try:
                        cursor.execute(sql, (pk_val,))
                        conn.commit()
                    except mysql.connector.Error as e:
                        sg.popup_error(f"MySQL error while deleting:\n{e}")
                    finally:
                        cursor.close()
                        conn.close()

                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)
                    selected_row_index = None

        # ---------- REFRESH ----------
        if event == "REFRESH":
            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()
