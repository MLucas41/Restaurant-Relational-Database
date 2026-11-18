import FreeSimpleGUI as fsg
import subprocess
import db
import sys
import os

TABLE_TO_SCRIPT = {
    "customers": "customers_gui.py",
    "employees": "employees_gui.py",
    "equipmentinventory": "equipmentinventory_gui.py",
    "equipmentvendororders": "equipmentvendororders_gui.py",
    "equipmentvendors": "equipmentvendors_gui.py",
    "ingredientinventory": "ingredientinventory_gui.py",
    "ingredientvendors": "ingredientvendors_gui.py",
    "menuitem": "menuitem_gui.py",
    "menuitemdetail": "menuitemdetail_gui.py",
    "orderitems": "orderitems_gui.py",
    "sales": "sales_gui.py",
    "seat": "seat_gui.py",
    "tables": "tables_gui.py",
    "vendororders": "vendororders_gui.py",
    "togo_orders" : "togoorders_gui.py"
}

def launch_script(script_name):
    if not os.path.exists(script_name):
        fsg.popup_error(f"File not found:\n{script_name}\n\nCreate this GUI file first.")
        return

    # Runs the file with the same python interpreter
    subprocess.Popen([sys.executable, script_name])


def main():
    fsg.theme("DarkBlue3")

    table_list = list(TABLE_TO_SCRIPT.keys())

    layout = [
        [fsg.Text("Luke's Lasagna - Database Manager", font=("Any", 18))],
        [fsg.Text("Select a table to manage:")],
        [fsg.Combo(table_list, key="-TABLE-", size=(40, 1))],
        [fsg.Button("Open Table", key="-OPEN-", size=(12, 1)),
         fsg.Button("Exit", size=(12, 1))]
    ]

    window = fsg.Window("Main Menu", layout)

    while True:
        event, values = window.read()
        if event in (fsg.WINDOW_CLOSED, "Exit"):
            break

        if event == "-OPEN-":
            selected = values["-TABLE-"]
            if not selected:
                fsg.popup("Please choose a table.")
                continue

            script = TABLE_TO_SCRIPT[selected]
            launch_script(script)

    window.close()


if __name__ == "__main__":
    main()
