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
    Edit a single ingredient vendor row.
    PK (vendor_ingredient_id) is read-only.
    """
    layout = [
        [sg.Text("Editing selected ingredient vendor")],
        [sg.Text(f"{headings[0]} (ID): {row_data[0]}")],
    ]

    # Inputs for all non-PK columns
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

    win = sg.Window("UPDATE INGREDIENT VENDOR", layout, modal=True)
    result = None

    while True:
        event, values = win.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            # Build dict of edited values for non-PK columns
            result = {}
            for col in headings[1:]:
                val = values[f"-EDIT-{col}-"]
                if col == "employee_id":
                    val = val.strip()
                    val = val if val != "" else None
                result[col] = val
            break

    win.close()
    return result


def addData():
    """
    Collect data for a NEW ingredient vendor row.
    PK is auto-increment, so we don’t ask for it.
    """
    layout = [
        [sg.Text("Employee ID (optional):"), sg.Input(key="-EMPID-")],
        [sg.Text("Vendor name:"), sg.Input(key="-VNAME-")],
        [sg.Text("Date last ordered (YYYY-MM-DD):"), sg.Input(key="-DATE-")],
        [sg.Text("Notes:"), sg.Multiline(key="-NOTES-", size=(40, 5))],
        [sg.Button("FINISH"), sg.Button("Cancel")],
    ]

    win = sg.Window("ADD INGREDIENT VENDOR", layout, modal=True)
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
    table_name = "ingredientVendors"
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

    window = sg.Window("Ingredient Vendors", layout, resizable=True, size=(800, 600))

    selected_row_index = None

    while True:
        event, values = window.read()

        # Track which row is selected
        if event == "-TABLE-":
            selected = values["-TABLE-"]
            selected_row_index = selected[0] if selected else None

        # -------- ADD --------
        if event == "ADD":
            vals = addData()
            if vals is not None:
                conn = db.get_connection()
                cursor = conn.cursor()

                emp_raw = vals["-EMPID-"].strip()
                emp_val = emp_raw if emp_raw != "" else None

                sql = """
                    INSERT INTO ingredientVendors
                    (employee_id, vendor_name, date_last_ordered_from, vendor_ingredient_notes)
                    VALUES (%s, %s, %s, %s)
                """
                params = (
                    emp_val,
                    vals["-VNAME-"],
                    vals["-DATE-"],
                    vals["-NOTES-"],
                )

                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()

            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        # -------- UPDATE --------
        if event == "UPDATE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to update.")
            else:
                row_data = data[selected_row_index]
                edited = updateData(row_data, headings)

                if edited is not None:
                    pk_col = headings[0]
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

        # -------- DELETE --------
        if event == "DELETE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to delete.")
            else:
                row_data = data[selected_row_index]
                pk_col = headings[0]
                pk_val = row_data[0]

                confirm = sg.popup_yes_no(
                    f"Are you sure you want to delete this ingredient vendor?\n\n{row_data}"
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

        # -------- REFRESH --------
        if event == "REFRESH":
            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()
