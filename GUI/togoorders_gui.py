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
    Edit a single TogoOrders row.
    PK (togo_id) is read-only.
    customer_id is nullable (blank -> NULL on update).
    pickup_time is editable as a DATETIME string.
    """
    layout = [
        [sg.Text("Editing selected to-go order")],
        [sg.Text(f"{headings[0]} (togo_id): {row_data[0]}")],
    ]

    for i, col_name in enumerate(headings[1:], start=1):
        value = "" if row_data[i] is None else row_data[i]

        if col_name == "instructions":
            layout.append(
                [
                    sg.Text(col_name + ":", size=(20, 1)),
                    sg.Multiline(
                        default_text=str(value),
                        key=f"-EDIT-{col_name}-",
                        size=(40, 5),
                    ),
                ]
            )
        else:
            layout.append(
                [
                    sg.Text(col_name + ":", size=(20, 1)),
                    sg.Input(
                        default_text=str(value),
                        key=f"-EDIT-{col_name}-",
                    ),
                ]
            )

    layout.append([sg.Button("FINISH"), sg.Button("Cancel")])

    win = sg.Window("UPDATE TO-GO ORDER", layout, modal=True)
    result = None

    while True:
        event, values = win.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            edited = {}
            for col in headings[1:]:
                val = values[f"-EDIT-{col}-"]
                if col == "customer_id":
                    val = val.strip()
                    val = val if val != "" else None
                edited[col] = val
            result = edited
            break

    win.close()
    return result


def addData():
    """
    Add a new TogoOrders row.
    PK (togo_id) and pickup_time are handled by the DB (auto, DEFAULT CURRENT_TIMESTAMP).
    """
    layout = [
        [sg.Text("sale_id:"), sg.Input(key="-SALE-")],
        [sg.Text("customer_id (optional):"), sg.Input(key="-CUSTID-")],
        [sg.Text("customer_name (optional):"), sg.Input(key="-CNAME-")],
        [sg.Text("customer_phone (optional):"), sg.Input(key="-CPHONE-")],
        [sg.Text("instructions (optional):")],
        [sg.Multiline(key="-INSTR-", size=(40, 5))],
        [sg.Button("FINISH"), sg.Button("Cancel")],
    ]

    win = sg.Window("ADD TO-GO ORDER", layout, modal=True)
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
    table_name = "TogoOrders"  # exact name from your CREATE TABLE
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

    window = sg.Window("To-Go Orders", layout, resizable=True, size=(950, 600))

    selected_row_index = None

    while True:
        event, values = window.read()

        # Track selection
        if event == "-TABLE-":
            sel = values["-TABLE-"]
            selected_row_index = sel[0] if sel else None

        # ---------- ADD ----------
        if event == "ADD":
            vals = addData()
            if vals is not None:
                cust_raw = vals["-CUSTID-"].strip()
                cust_val = cust_raw if cust_raw != "" else None

                conn = db.get_connection()
                cursor = conn.cursor()

                # Let DB fill pickup_time via DEFAULT CURRENT_TIMESTAMP
                sql = """
                    INSERT INTO TogoOrders
                    (sale_id,
                     customer_id,
                     customer_name,
                     customer_phone,
                     instructions)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (
                    vals["-SALE-"],
                    cust_val,
                    vals["-CNAME-"],
                    vals["-CPHONE-"],
                    vals["-INSTR-"],
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
                    pk_col = headings[0]   # togo_id
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
                    f"Delete this to-go order?\n\n{row_data}"
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
