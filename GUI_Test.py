import FreeSimpleGUI as sg

layout = [
    [sg.Text("Hello from FreeSimpleGUI!")],
    [sg.Button("OK")]
]

window = sg.Window("Test Window", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "OK":
        break

window.close()