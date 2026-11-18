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
    Opens a window to edit a single equipment row.
    PK (equipment_id) is read-only.
    Generated column (equipment_replacement_date) is displayed but not editable.
    """
    layout = [
        [sg.Text("Editing selected equipment item")],
        [sg.Text(f"{headings[0]} (ID): {row_data[0]}")],
    ]

    for i, col_name in enumerate(headings[1:], start=1):
        # Generated column: show as read-only text
        if col_name == "equipment_replacement_date":
            layout.append(
                [
                    sg.Text(col_name + ":", size=(25, 1)),
                    sg.Text(str(row_data[i]), key=f"-VIEW-{col_name}-"),
                ]
            )
            continue

        # Default: editable input
        layout.append(
            [
                sg.Text(col_name + ":", size=(25, 1)),
                sg.Input(default_text=row_data[i] if row_data[i] is not None else "",
                         key=f"-EDIT-{col_name}-"),
            ]
        )

    layout.append([sg.Button("FINISH"), sg.Button("Cancel")])

    win = sg.Window("UPDATE EQUIPMENT", layout, modal=True)
    result = None

    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            # Build dict for all editable, non-PK, non-generated columns
            result = {}
            for col_name in headings[1:]:
                if col_name == "equipment_replacement_date":
                    continue
                result[col_name] = values[f"-EDIT-{col_name}-"]
            break

    win.close()
    return result


def addData():
    """
    Collect data for a NEW equipment row.
    We do NOT ask for equipment_id (PK) or equipment_replacement_date (generated).
    """
    layout = [
        [sg.Text("Equipment name:"), sg.Input(key="-NAME-")],
        [sg.Text("Unit (e.g. 'pcs'):"), sg.Input(key="-UNIT-")],
        [sg.Text("Quantity:"), sg.Input(key="-QTY-")],
        [sg.Text("Date last purchased (YYYY-MM-DD):"),
         sg.Input(key="-DATEPUR-")],
        [sg.Text("Lifespan (days):"), sg.Input(key="-LIFE-")],
        [sg.Text("Info / notes:")],
        [sg.Multiline(key="-INFO-", size=(40, 5))],
        [sg.Button("FINISH"), sg.Button("Cancel")],
    ]

    win = sg.Window("ADD EQUIPMENT", layout, modal=True)
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
    table_name = "equipmentInventory"  # use your exact table name here
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

    window = sg.Window("Equipment Inventory", layout, resizable=True, size=(900, 600))

    selected_row_index = None

    while True:
        event, values = window.read()

        if event == "-TABLE-":
            selected = values["-TABLE-"]
            selected_row_index = selected[0] if selected else None

        if event == "ADD":
            vals = addData()
            if vals is not None:
                conn = db.get_connection()
                cursor = conn.cursor()
                sql = """
                    INSERT INTO equipmentInventory
                    (equipment_name,
                     equipment_unit,
                     equipment_quantity,
                     equipment_date_last_purchased,
                     equipment_lifespan_days,
                     equipment_info)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (
                    vals["-NAME-"],
                    vals["-UNIT-"],
                    vals["-QTY-"],
                    vals["-DATEPUR-"],
                    vals["-LIFE-"],
                    vals["-INFO-"],
                )
                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()

            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == "UPDATE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to update.")
            else:
                row_data = data[selected_row_index]
                edited = updateData(row_data, headings)

                if edited is not None:
                    pk_col = headings[0]
                    pk_val = row_data[0]

                    # Explicit list of updatable columns (skip PK + generated)
                    updatable_cols = [
                        "equipment_name",
                        "equipment_unit",
                        "equipment_quantity",
                        "equipment_date_last_purchased",
                        "equipment_lifespan_days",
                        "equipment_info",
                    ]
                    set_clause = ", ".join(col + " = %s" for col in updatable_cols)
                    sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_col} = %s"

                    params = [edited[col] for col in updatable_cols]
                    params.append(pk_val)

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

        if event == "DELETE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to delete.")
            else:
                row_data = data[selected_row_index]
                pk_col = headings[0]
                pk_val = row_data[0]

                confirm = sg.popup_yes_no(
                    f"Are you sure you want to delete this row?\n\n{row_data}"
                )
                if confirm == "Yes":
                    conn = db.get_connection()
                    cursor = conn.cursor()
                    sql = f"DELETE FROM {table_name} WHERE {pk_col} = %s"
                    try:
                        cursor.execute(sql, (pk_val,))
                        conn.commit()
                    except mysql.connector.Error as e:
                        sg.popup_error(f"MYSQL ERROR while deleting:\n{e}")
                    finally:
                        cursor.close()
                        conn.close()

                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)
                    selected_row_index = None

        if event == "REFRESH":
            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()
