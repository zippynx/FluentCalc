import tkinter as tk
import math

WINDOW_BG = "#F3F3F3"

BTN_WHITE = "#FFFFFF"
BTN_LIGHT = "#F8F8F8"

BTN_BLUE = "#005FB8"
BTN_BLUE_HOVER = "#0A6ED1"

TEXT = "#1B1B1B"
TEXT_MUTED = "#7A7A7A"

window = tk.Tk()

window.title("Kalkulator")
window.geometry("402x640")
window.minsize(360, 580)

window.configure(bg=WINDOW_BG)

try:
    window.iconbitmap("calculatoricon.ico")
except:
    pass

current_input = "0"
stored_value = None
current_operator = None
reset_screen = False

history_var = tk.StringVar(value="")
display_var = tk.StringVar(value="0")

main = tk.Frame(
    window,
    bg=WINDOW_BG
)

main.pack(
    fill="both",
    expand=True,
    padx=6,
    pady=6
)

topbar = tk.Frame(
    main,
    bg=WINDOW_BG,
    height=48
)

topbar.pack(
    fill="x",
    pady=(2, 0)
)

topbar.pack_propagate(False)

menu_icon = tk.Label(
    topbar,
    text="☰",
    bg=WINDOW_BG,
    fg=TEXT,
    font=("Segoe UI Symbol", 17)
)

menu_icon.pack(
    side="left",
    padx=(8, 16)
)

title = tk.Label(
    topbar,
    text="Standar",
    bg=WINDOW_BG,
    fg=TEXT,
    font=("Segoe UI Semibold", 19)
)

title.pack(side="left")

history_icon = tk.Label(
    topbar,
    text="◷",
    bg=WINDOW_BG,
    fg=TEXT,
    font=("Segoe UI Symbol", 16)
)

history_icon.pack(
    side="right",
    padx=(0, 10)
)

display_frame = tk.Frame(
    main,
    bg=WINDOW_BG,
    height=160
)

display_frame.pack(
    fill="x",
    pady=(0, 8)
)

display_frame.pack_propagate(False)

history_label = tk.Label(
    display_frame,
    textvariable=history_var,
    anchor="e",
    bg=WINDOW_BG,
    fg=TEXT_MUTED,
    font=("Segoe UI", 16)
)

history_label.pack(
    fill="x",
    padx=12,
    pady=(28, 0)
)

display_label = tk.Label(
    display_frame,
    textvariable=display_var,
    anchor="e",
    bg=WINDOW_BG,
    fg=TEXT,
    font=("Segoe UI Variable", 40, "bold")
)

display_label.pack(
    fill="x",
    padx=10,
    pady=(8, 0)
)

memory_frame = tk.Frame(
    main,
    bg=WINDOW_BG,
    height=34
)

memory_frame.pack(
    fill="x",
    pady=(0, 8)
)

memory_frame.pack_propagate(False)

memory_buttons = ["MC", "MR", "M+", "M-", "MS", "M∨"]

for item in memory_buttons:

    lbl = tk.Label(
        memory_frame,
        text=item,
        bg=WINDOW_BG,
        fg="#B7B7B7" if item in ["MC", "MR"] else TEXT,
        font=("Segoe UI Semibold", 10)
    )

    lbl.pack(
        side="left",
        expand=True
    )

buttons_frame = tk.Frame(
    main,
    bg=WINDOW_BG
)

buttons_frame.pack(
    fill="both",
    expand=True
)

for i in range(6):
    buttons_frame.rowconfigure(i, weight=1)

for j in range(4):
    buttons_frame.columnconfigure(j, weight=1)

def format_indo(value):

    try:

        value = str(value)

        if value.endswith(".0"):
            value = value[:-2]

        negative = value.startswith("-")

        if negative:
            value = value[1:]

        if "." in value:

            int_part, dec_part = value.split(".")

            int_part = f"{int(int_part):,}".replace(",", ".")

            result = f"{int_part},{dec_part}"

        else:

            result = f"{int(value):,}".replace(",", ".")

        if negative:
            result = "-" + result

        return result

    except:
        return str(value)

def update_display(value):

    display_var.set(format_indo(value))

def append_number(number):

    global current_input
    global reset_screen

    if reset_screen:

        current_input = number
        reset_screen = False

    else:

        if current_input == "0":
            current_input = number
        else:
            current_input += number

    update_display(current_input)

def add_decimal():

    global current_input
    global reset_screen

    if reset_screen:

        current_input = "0"
        reset_screen = False

    if "." not in current_input:

        current_input += "."

    update_display(current_input)

def clear():

    global current_input
    global stored_value
    global current_operator
    global reset_screen

    current_input = "0"
    stored_value = None
    current_operator = None
    reset_screen = False

    history_var.set("")

    update_display(current_input)

def clear_entry():

    global current_input

    current_input = "0"

    update_display(current_input)

def backspace():

    global current_input
    global reset_screen

    if reset_screen:
        return

    if current_input != "0":

        current_input = current_input[:-1]

        if current_input.endswith("."):
            current_input = current_input[:-1]

        if current_input == "":
            current_input = "0"

    update_display(current_input)

def toggle_sign():
    global current_input

    try:

        value = float(current_input) * -1

        if value.is_integer():
            current_input = str(int(value))
        else:
            current_input = str(value)

        update_display(current_input)

    except:
        pass

def set_operator(op):

    global stored_value
    global current_operator
    global reset_screen

    try:

        stored_value = float(current_input)

        current_operator = op

        history_var.set(
            f"{format_indo(current_input)} {op}"
        )

        reset_screen = True

    except:
        pass

def calculate():

    global current_input
    global stored_value
    global current_operator
    global reset_screen

    try:

        if stored_value is None or current_operator is None:
            return

        second_value = float(current_input)

        history_var.set(
            f"{format_indo(stored_value)} "
            f"{current_operator} "
            f"{format_indo(second_value)} ="
        )

        if current_operator == "+":
            result = stored_value + second_value

        elif current_operator == "-":
            result = stored_value - second_value

        elif current_operator == "×":
            result = stored_value * second_value

        elif current_operator == "÷":

            if second_value == 0:
                update_display("Error")
                return

            result = stored_value / second_value

        else:
            return

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        current_input = str(result)

        update_display(current_input)

        stored_value = None
        current_operator = None

        reset_screen = True

    except:
        update_display("Error")

def create_button(text, row, col, command):

    white_buttons = [
        "7", "8", "9",
        "4", "5", "6",
        "1", "2", "3",
        "+/-", "0", ","
    ]

    if text == "=":

        bg = BTN_BLUE
        fg = "white"
        active = BTN_BLUE_HOVER

    elif text in white_buttons:

        bg = BTN_WHITE
        fg = TEXT
        active = "#F1F1F1"

    else:

        bg = BTN_LIGHT
        fg = TEXT
        active = "#ECECEC"

    button = tk.Button(
        buttons_frame,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=active,
        activeforeground=fg,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground="#E6E6E6",
        highlightcolor="#E6E6E6",
        font=("Segoe UI", 17),
        cursor="hand2"
    )

    button.grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=2,
        pady=2,
        ipadx=0,
        ipady=0
    )

buttons = [

    ("%", 0, 0, lambda: None),
    ("CE", 0, 1, clear_entry),
    ("C", 0, 2, clear),
    ("⌫", 0, 3, backspace),

    ("¹/x", 1, 0, lambda: None),
    ("x²", 1, 1, lambda: None),
    ("²√x", 1, 2, lambda: None),
    ("÷", 1, 3, lambda: set_operator("÷")),

    ("7", 2, 0, lambda: append_number("7")),
    ("8", 2, 1, lambda: append_number("8")),
    ("9", 2, 2, lambda: append_number("9")),
    ("×", 2, 3, lambda: set_operator("×")),

    ("4", 3, 0, lambda: append_number("4")),
    ("5", 3, 1, lambda: append_number("5")),
    ("6", 3, 2, lambda: append_number("6")),
    ("-", 3, 3, lambda: set_operator("-")),

    ("1", 4, 0, lambda: append_number("1")),
    ("2", 4, 1, lambda: append_number("2")),
    ("3", 4, 2, lambda: append_number("3")),
    ("+", 4, 3, lambda: set_operator("+")),

    ("+/-", 5, 0, toggle_sign),
    ("0", 5, 1, lambda: append_number("0")),
    (",", 5, 2, add_decimal),
    ("=", 5, 3, calculate),
]

for text, row, col, command in buttons:
    create_button(text, row, col, command)
    
def key_press(event):

    key = event.keysym
    char = event.char

    if char in "0123456789":
        append_number(char)

    elif char in ".,":
        add_decimal()

    elif char == "+":
        set_operator("+")

    elif char == "-":
        set_operator("-")

    elif char == "*":
        set_operator("×")

    elif char == "/":
        set_operator("÷")

    elif key == "Return":
        calculate()

    elif key == "BackSpace":
        backspace()

    elif key == "Escape":
        clear()

window.bind("<Key>", key_press)
window.mainloop()