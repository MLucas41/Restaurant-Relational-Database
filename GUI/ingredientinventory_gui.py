import FreeSimpleGUI as sg
import mysql.connector
import smtplib
from email.message import EmailMessage
import db

sentEmail = False

def fetch_table(table_name):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    headings = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return rows, headings

def send_zero_alert_email(row_id, column_name, table_name, to_email):
    msg = EmailMessage()
    msg["Subject"] = f"[DB ALERT] {table_name}.{column_name} hit 0 (id={row_id})"
    msg["From"] = "test.mertlich@gmail.com"
    msg["To"] = to_email

    body = (
        f"The column '{column_name}' in table '{table_name}' "
        f"has reached 0 for row with id={row_id}.\n\n"
        "You might want to restock / investigate."
    )
    msg.set_content(body)

    # WARNING: use an app password, not your real login password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "test.mertlich@gmail.com"
    password = "vyxv sjqd wxvv wyri"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

def updateData(row_data, headings):
    layout = [
        [sg.Text("Editing selected ingredient")],
        [sg.Text(f"{headings[0]} (ID): {row_data[0]}")],  # PK read-only
    ]

    # Inputs for all non-PK columns
    for i, col_name in enumerate(headings[1:], start=1):
        layout.append(
            [
                sg.Text(col_name + ":", size=(20, 1)),
                sg.Input(
                    default_text=row_data[i] if row_data[i] is not None else "",
                    key=f"-EDIT-{col_name}-"
                ),
            ]
        )

    layout.append([sg.Button("FINISH"), sg.Button("Cancel")])

    win = sg.Window("UPDATE INGREDIENT", layout, modal=True)
    result = None

    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "FINISH":
            # Return dict of edited values
            result = {col: values[f"-EDIT-{col}-"] for col in headings[1:]}
            break

    win.close()
    return result


def addData():
    """
    Window to add a new ingredient.
    PK is auto-increment → not entered manually.
    """
    layout = [
        [sg.Text("Ingredient name:"), sg.Input(key="-NAME-")],
        [sg.Text("Unit (optional):"), sg.Input(key="-UNIT-")],
        [sg.Text("Quantity:"), sg.Input(key="-QTY-")],
        [sg.Text("Info / notes:"), sg.Multiline(key="-INFO-", size=(40, 5))],
        [sg.Button("FINISH"), sg.Button("Cancel")],
    ]

    win = sg.Window("ADD INGREDIENT", layout, modal=True)
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
    table_name = "ingredientInventory"
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

    window = sg.Window("Ingredient Inventory", layout, resizable=True, size=(850, 600))

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
                conn = db.get_connection()
                cursor = conn.cursor()

                sql = """
                    INSERT INTO ingredientInventory
                    (ingredient_name, ingredient_unit, ingredient_quantity, ingredient_info)
                    VALUES (%s, %s, %s, %s)
                """
                params = (
                    vals["-NAME-"],
                    vals["-UNIT-"],
                    vals["-QTY-"],
                    vals["-INFO-"],
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
                    pk_col = headings[0]
                    pk_val = row_data[0]

                    new_qty = None
                    if "ingredient_quantity" in edited:
                        try:
                            new_qty = int(edited["ingredient_quantity"])
                        except ValueError:
                            new_qty = None  # user typed something non-numeric

                    # ---- build and run UPDATE as before ----
                    cols = headings[1:]  # non-PK
                    set_clause = ", ".join(f"{col} = %s" for col in cols)
                    sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_col} = %s"
                    params = [edited[col] for col in cols] + [pk_val]

                    conn = db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(sql, params)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    # ---- if quantity is exactly 0, send email ----
                    if new_qty == 0:
                        send_zero_alert_email(
                            row_id=pk_val,
                            column_name="ingredient_quantity",
                            table_name=table_name,
                            to_email="lucas.mertlich@gmail.com",  # where alerts go
                        )

                    data, headings = fetch_table(table_name)
                    window["-TABLE-"].update(values=data)
                    if 0 <= selected_row_index < len(data):
                        window["-TABLE-"].update(select_rows=[selected_row_index])

        # ---- DELETE ----
        if event == "DELETE":
            if selected_row_index is None:
                sg.popup_error("Please select a row first.")
            else:
                row_data = data[selected_row_index]
                pk_col = headings[0]
                pk_val = row_data[0]

                confirm = sg.popup_yes_no(
                    f"Delete this ingredient?\n\n{row_data}"
                )

                if confirm == "Yes":
                    conn = db.get_connection()
                    cursor = conn.cursor()

                    sql = f"DELETE FROM {table_name} WHERE {pk_col} = %s"

                    try:
                        cursor.execute(sql, (pk_val,))
                        conn.commit()
                    except mysql.connector.Error as e:
                        sg.popup_error(f"MySQL Error:\n{e}")
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
