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
    Edit a single VendorOrders row.
    PK (order_id) is read-only.
    """
    layout = [
        [sg.Text("Editing selected vendor order")],
        [sg.Text(f"{headings[0]} (order_id): {row_data[0]}")],
    ]

    # Inputs for all non-PK columns
    for i, col_name in enumerate(headings[1:], start=1):
        layout.append(
            [
                sg.Text(col_name + ":", size=(22, 1)),
                sg.Input(
                    default_text=row_data[i] if row_data[i] is not None else "",
                    key=f"-EDIT-{col_name}-",
                ),
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
            # Collect edited values for all non-PK columns
            result = {col: values[f"-EDIT-{col}-"] for col in headings[1:]}
            break

    win.close()
    return result


def addData():
    """
    Window to add a new VendorOrders row.
    PK (order_id) is auto-increment → not entered.
    """
    layout = [
        [sg.Text("vendor_id:"), sg.Input(key="-VENDOR-")],
        [sg.Text("ingredient_id:"), sg.Input(key="-INGID-")],
        [sg.Text("ingredient_unit (optional):"), sg.Input(key="-UNIT-")],
        [sg.Text("ingredient_quantity (optional):"), sg.Input(key="-QTY-")],
        [sg.Text("total_order_price (optional):"), sg.Input(key="-PRICE-")],
        [sg.Text("date_last_ordered_from (YYYY-MM-DD, optional):"), sg.Input(key="-DATE-")],
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
    table_name = "VendorOrders"  # exact name from your CREATE TABLE
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

    window = sg.Window("Vendor Orders", layout, resizable=True, size=(950, 600))

    selected_row_index = None

    while True:
        event, values = window.read()

        # Track selected row
        if event == "-TABLE-":
            sel = values["-TABLE-"]
            selected_row_index = sel[0] if sel else None

        # ---------- ADD ----------
        if event == "ADD":
            vals = addData()
            if vals is not None:
                conn = db.get_connection()
                cursor = conn.cursor()

                sql = """
                    INSERT INTO VendorOrders
                    (vendor_id,
                     ingredient_id,
                     ingredient_unit,
                     ingredient_quantity,
                     total_order_price,
                     date_last_ordered_from)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (
                    vals["-VENDOR-"],
                    vals["-INGID-"],
                    vals["-UNIT-"],
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

        # ---------- UPDATE ----------
        if event == "UPDATE":
            if selected_row_index is None:
                sg.popup_error("Please select a row to update.")
            else:
                row_data = data[selected_row_index]
                edited = updateData(row_data, headings)

                if edited is not None:
                    pk_col = headings[0]   # order_id
                    pk_val = row_data[0]

                    cols = headings[1:]     # non-PK columns
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
