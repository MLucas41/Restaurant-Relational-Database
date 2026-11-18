import FreeSimpleGUI as sg
import mysql.connector
import db

ENUM_TYPES = ["Entre", "Side", "Drink", "Dessert"]
BOOL_OPTIONS = ["True", "False"]


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
    Edit a single menuItem row.
    PK (menuItem_id) is shown but not editable.
    """
    layout = [
        [sg.Text("Editing menu item")],
        [sg.Text(f"{headings[0]} (ID): {row_data[0]}")],
    ]

    for i, col_name in enumerate(headings[1:], start=1):

        value = row_data[i] if row_data[i] is not None else ""

        # ENUM: menuItem_type
        if col_name == "menuItem_type":
            layout.append([
                sg.Text(col_name + ":", size=(20, 1)),
                sg.Combo(
                    values=ENUM_TYPES,
                    default_value=value,
                    readonly=True,
                    key=f"-EDIT-{col_name}-"
                )
            ])
            continue

        # BOOL: menuItem_isAvailable
        if col_name == "menuItem_isAvailable":
            layout.append([
                sg.Text(col_name + ":", size=(20, 1)),
                sg.Combo(
                    values=BOOL_OPTIONS,
                    default_value="True" if value == 1 else "False",
                    readonly=True,
                    key=f"-EDIT-{col_name}-"
                )
            ])
            continue

        # Default text input
        layout.append([
            sg.Text(col_name + ":", size=(20, 1)),
            sg.Input(default_text=value, key=f"-EDIT-{col_name}-")
        ])

    layout.append([sg.Button("FINISH"), sg.Button("Cancel")])
    win = sg.Window("UPDATE MENU ITEM", layout, modal=True)

    result = None

    while True:
        event, values = win.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            edited = {}
            for col in headings[1:]:
                val = values[f"-EDIT-{col}-"]

                if col == "menuItem_isAvailable":
                    val = 1 if val == "True" else 0

                edited[col] = val

            result = edited
            break

    win.close()
    return result


def addData():
    """
    Add a new menu item.
    PK auto-increments → not included.
    """
    layout = [
        [sg.Text("menuItem_name:"), sg.Input(key="-NAME-")],
        [sg.Text("menuItem_cost:"), sg.Input(key="-COST-")],
        [sg.Text("menuItem_isAvailable:"), sg.Combo(BOOL_OPTIONS, default_value="True", readonly=True, key="-AVAIL-")],
        [sg.Text("menuItem_type:"), sg.Combo(ENUM_TYPES, readonly=True, key="-TYPE-")],
        [sg.Button("FINISH"), sg.Button("Cancel")],
    ]

    win = sg.Window("ADD MENU ITEM", layout, modal=True)
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
    table_name = "menuItem"
    data, headings = fetch_table(table_name)

    layout = [
        [sg.Table(
            values=data,
            headings=headings,
            auto_size_columns=True,
            display_row_numbers=False,
            justification='left',
            num_rows=20,
            key='-TABLE-',
            enable_events=True,
            select_mode=sg.SELECT_MODE_BROWSE
        )],
        [sg.Button("ADD"), sg.Button("UPDATE"), sg.Button("DELETE")],
        [sg.Button("REFRESH")],
    ]

    window = sg.Window("Menu Items", layout, resizable=True, size=(850, 600))

    selected_row_index = None

    while True:
        event, values = window.read()

        if event == "-TABLE-":
            sel = values["-TABLE-"]
            selected_row_index = sel[0] if sel else None

        # ---- ADD ----
        if event == "ADD":
            vals = addData()
            if vals is not None:

                avail_val = 1 if vals["-AVAIL-"] == "True" else 0

                conn = db.get_connection()
                cursor = conn.cursor()

                sql = """
                    INSERT INTO menuItem
                    (menuItem_name, menuItem_isAvailable, menuItem_cost, menuItem_type)
                    VALUES (%s, %s, %s, %s)
                """
                params = (
                    vals["-NAME-"],
                    avail_val,
                    vals["-COST-"],
                    vals["-TYPE-"],
                )

                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()

            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        # ---- UPDATE ----
        if event == "UPDATE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to update.")
            else:
                row_data = data[selected_row_index]
                edited = updateData(row_data, headings)

                if edited is not None:
                    pk_col = headings[0]  # menuItem_id
                    pk_val = row_data[0]

                    cols = headings[1:]
                    set_clause = ", ".join(f"{col} = %s" for col in cols)
                    sql = f"UPDATE menuItem SET {set_clause} WHERE {pk_col} = %s"

                    params = [edited[col] for col in cols] + [pk_val]

                    conn = db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(sql, params)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)

        # ---- DELETE ----
        if event == "DELETE":
            if selected_row_index is None:
                sg.popup_error("Choose a row first.")
            else:
                pk_val = data[selected_row_index][0]

                confirm = sg.popup_yes_no(f"Delete this menu item?\n\nID: {pk_val}")

                if confirm == "Yes":
                    conn = db.get_connection()
                    cursor = conn.cursor()

                    sql = "DELETE FROM menuItem WHERE menuItem_id = %s"

                    try:
                        cursor.execute(sql, (pk_val,))
                        conn.commit()
                    except mysql.connector.Error as e:
                        sg.popup_error(f"MYSQL ERROR:\n{e}")
                    finally:
                        cursor.close()
                        conn.close()

                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)
                    selected_row_index = None

        # ---- REFRESH ----
        if event == "REFRESH":
            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()
