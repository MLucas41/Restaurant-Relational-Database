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
    layout = [
        [sg.Text("Editing selected customer")],
        [sg.Text(f"{headings[0]} (ID): {row_data[0]}")],  # show PK, read-only
    ]

    # For each non-PK column, make a labeled input prefilled with current value
    for i, col_name in enumerate(headings[1:], start=1):
        layout.append(
            [
                sg.Text(col_name + ":", size=(20, 1)),
                sg.Input(default_text=row_data[i], key=f"-EDIT-{col_name}-")
            ]
        )

    layout.append([sg.Button("FINISH"), sg.Button("Cancel")])

    win = sg.Window("UPDATE ROW", layout, modal=True)
    result = None

    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            # Build dict: {col_name: new_value, ...} for all non-PK columns
            result = {col_name: values[f"-EDIT-{col_name}-"] for col_name in headings[1:]}
            break

    win.close()
    return result


def addData():
    layout = [
        [sg.Text("First name:"), sg.Input(key="-FNAME-")],
        [sg.Text("Last name:"), sg.Input(key="-LNAME-")],
        [sg.Text("Usual item:"), sg.Input(key="-ITEM-")],
        [sg.Text("Times visited:"), sg.Input(key="-TIMES-")],
        [sg.Text("Date last visited:"), sg.Input(key="-DATE-")],
        [sg.Text("Notes:"), sg.Input(key="-NOTES-")],
        [sg.Button("FINISH"), sg.Button("Cancel")]
    ]
    win = sg.Window("ADD ROW", layout, modal=True)

    result = None
    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == "FINISH":
            result = values  # whole dict
            break

    win.close()
    return result


def main():

    data, headings = fetch_table("customers")

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
    [sg.Button("REFRESH")]
    ]
    
    window = sg.Window("Customer Window", layout, resizable=True, size=(800, 600))

    selected_row_index = None

    while True:
        event, values, = window.read()

        # track which row is selected
        if event == "-TABLE-":
            selected = values["-TABLE-"]
            if selected:
                selected_row_index = selected[0]
            else:
                selected_row_index = None

        if event == "ADD":
            vals = addData()
            if vals is not None:
                conn = db.get_connection()
                cursor = conn.cursor()
                sql = """
                    INSERT INTO customers
                    (customer_fname, customer_lname, customer_usual_menuitem, customer_timesvisited, customer_lastvisit_date, customer_notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (
                    vals["-FNAME-"],
                    vals["-LNAME-"],
                    vals["-ITEM-"],
                    vals["-TIMES-"],
                    vals["-DATE-"],
                    vals["-NOTES-"],
                )
                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()

            data, headings = fetch_table("customers")
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == "UPDATE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to update.")
            else:
                row_data = data[selected_row_index]
                edited = updateData(row_data, headings)

                if edited is not None:
                    table_name = "customers"
                    pk_col = headings[0]
                    pk_val = row_data[0]

                    # Build: SET col2=%s, col3=%s, ...
                    set_clause = ", ".join(f"{col} = %s" for col in headings[1:])
                    sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_col} = %s"

                    params = [edited[col] for col in headings[1:]]  # in same order
                    params.append(pk_val)  # WHERE pk = ?

                    conn = db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(sql, params)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    # refresh table after update
                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)
                    # try to keep same row selected
                    if 0 <= selected_row_index < len(data):
                        window["-TABLE-"].update(select_rows=[selected_row_index])


        if event == "DELETE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to delete.")
            else:
                # row data from the current data list
                row_data = data[selected_row_index]
                pk_col = headings[0]   # assume first column is primary key
                pk_val = row_data[0]

                confirm = sg.popup_yes_no(
                    f"Are you sure you want to delete this row?\n\n{row_data}"
                )
                if confirm == "Yes":
                    conn = db.get_connection()
                    cursor = conn.cursor()

                    sql = f"DELETE FROM customers WHERE {pk_col} = %s"
                    try:
                        cursor.execute(sql, (pk_val,))
                        conn.commit()
                    except mysql.connector.Error as e:
                        sg.popup_error(f"MYSQL ERROR while deleting:\n{e}")
                    finally:
                        cursor.close()
                        conn.close()

                    # refresh table after delete
                    data, headings = fetch_table("customers")
                    window["-TABLE-"].update(values=data)
                    selected_row_index = None

        if event == "REFRESH":
            data, headings = fetch_table("customers")
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    main()