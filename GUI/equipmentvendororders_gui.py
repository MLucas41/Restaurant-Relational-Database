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
    Opens a window to edit a vendor order row.
    PK (order_id) is displayed but not editable.
    """
    layout = [
        [sg.Text("Editing selected equipment vendor order")],
        [sg.Text(f"{headings[0]} (Order ID): {row_data[0]}")],
    ]

    # Generate editable inputs for all non-PK columns
    for i, col_name in enumerate(headings[1:], start=1):
        layout.append(
            [
                sg.Text(col_name + ":", size=(25, 1)),
                sg.Input(default_text=row_data[i] if row_data[i] is not None else "",
                         key=f"-EDIT-{col_name}-"),
            ]
        )

    layout.append([sg.Button("FINISH"), sg.Button("Cancel")])

    win = sg.Window("UPDATE VENDOR ORDER", layout, modal=True)
    result = None

    while True:
        event, values = win.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            result = {col: values[f"-EDIT-{col}-"] for col in headings[1:]}
            break

    win.close()
    return result


def addData():
    """
    Window to create a new vendor order row.
    PK is auto-inc → not included.
    """
    layout = [
        [sg.Text("Vendor ID:"), sg.Input(key="-VENDOR-")],
        [sg.Text("Equipment ID:"), sg.Input(key="-EQID-")],
        [sg.Text("Equipment Quantity:"), sg.Input(key="-QTY-")],
        [sg.Text("Total Order Price:"), sg.Input(key="-PRICE-")],
        [sg.Text("Date Last Ordered (YYYY-MM-DD):"), sg.Input(key="-DATE-")],
        [sg.Button("FINISH"), sg.Button("Cancel")],
    ]

    win = sg.Window("ADD VENDOR ORDER", layout, modal=True)
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
    table_name = "equipmentVendorOrders"
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

    window = sg.Window("Equipment Vendor Orders", layout, resizable=True, size=(900, 600))

    selected_row_index = None

    while True:
        event, values = window.read()

        # Track selection
        if event == "-TABLE-":
            sel = values["-TABLE-"]
            selected_row_index = sel[0] if sel else None

        # --- ADD ---
        if event == "ADD":
            vals = addData()
            if vals is not None:
                conn = db.get_connection()
                cursor = conn.cursor()

                sql = """
                    INSERT INTO equipmentVendorOrders
                    (vendor_id, equipment_id, equipment_quantity,
                     total_order_price, date_last_ordered_from)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (
                    vals["-VENDOR-"],
                    vals["-EQID-"],
                    vals["-QTY-"],
                    vals["-PRICE-"],
                    vals["-DATE-"],
                )

                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
                conn.close()

            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        # --- UPDATE ---
        if event == "UPDATE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to update.")
            else:
                row_data = data[selected_row_index]
                edited = updateData(row_data, headings)

                if edited is not None:
                    pk_col = headings[0]
                    pk_val = row_data[0]

                    # Update all columns except PK
                    cols = headings[1:]
                    set_clause = ", ".join(col + " = %s" for col in cols)
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

        # --- DELETE ---
        if event == "DELETE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to delete.")
            else:
                row_data = data[selected_row_index]
                pk_col = headings[0]
                pk_val = row_data[0]

                confirm = sg.popup_yes_no(
                    f"Delete this vendor order?\n\n{row_data}"
                )

                if confirm == "Yes":
                    conn = db.get_connection()
                    cursor = conn.cursor()

                    sql = f"DELETE FROM {table_name} WHERE {pk_col} = %s"

                    try:
                        cursor.execute(sql, (pk_val,))
                        conn.commit()
                    except mysql.connector.Error as e:
                        sg.popup_error(f"MySQL error:\n{e}")
                    finally:
                        cursor.close()
                        conn.close()

                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)
                    selected_row_index = None

        # --- REFRESH ---
        if event == "REFRESH":
            data, headings = fetch_table(table_name)
            window["-TABLE-"].update(values=data)
            selected_row_index = None

        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()
