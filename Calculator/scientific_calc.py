from tkinter import *
import math
# Global state
expression = ''
# Functions
def press(char):
    global expression
    expression += str(char)
    input_text.set(expression)
def equal():
    global expression
    try:
        result = str(eval(expression))
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""
def clear():
    global expression
    expression = ''
    input_text.set('')
def backspace():
    global expression
    expression = expression[:-1]
    input_text.set(expression)
def apply_function(func):
    global expression
    try:
        val = eval(expression)
        if func == 'sqrt':
            result = math.sqrt(val)
        elif func == 'square':
            result = val ** 2
        elif func == 'sin':
            result = math.sin(math.radians(val))
        elif func == 'cos':
            result = math.cos(math.radians(val))
        elif func == 'tan':
            result = math.tan(math.radians(val))
        elif func == 'log':
            result = math.log10(val)
        elif func == 'ln':
            result = math.log(val)
        elif func == 'fact':
            result = math.factorial(int(val))
        input_text.set(str(round(result, 6)))
        expression = str(result)
    except:
        input_text.set("Error")
        expression = ''
def insert_constant(constant):
    global expression
    if constant == 'pi':
        expression += str(math.pi)
    elif constant == 'e':
        expression += str(math.e)
    input_text.set(expression)
# Window Setup
root = Tk()
root.title("Scientific Calculator")
root.geometry("420x600")
root.resizable(0, 0)
root.configure(bg='#2196F3')  # Blue theme
# Entry Display
input_text = StringVar()
entry = Entry(root, textvariable=input_text, font=('consolas', 28),
              bg='#E3F2FD', fg='black', justify='right', bd=0, relief=FLAT)
entry.pack(fill='both', padx=10, pady=(20, 10), ipady=10)
# Button Colors & Fonts
btn_font = ('consolas', 16)
btn_bg = '#42A5F5'
btn_fg = 'white'
btn_active = '#64B5F6'
# Frame for Buttons
frame = Frame(root, bg='#2196F3')
frame.pack(expand=True, fill='both')
# Button layout
buttons = [
    # Row 1
    ('C', clear), ('⌫', backspace), ('(', lambda: press('(')), (')', lambda: press(')')), ('π', lambda: insert_constant('pi')), ('e', lambda: insert_constant('e')),
    # Row 2
    ('sin', lambda: apply_function('sin')), ('cos', lambda: apply_function('cos')),
    ('tan', lambda: apply_function('tan')), ('log', lambda: apply_function('log')),
    ('ln', lambda: apply_function('ln')), ('√', lambda: apply_function('sqrt')),
    # Row 3
    ('7', lambda: press('7')), ('8', lambda: press('8')), ('9', lambda: press('9')), ('/', lambda: press('/')),
    ('x²', lambda: apply_function('square')), ('xʸ', lambda: press('**')),
    # Row 4
    ('4', lambda: press('4')), ('5', lambda: press('5')), ('6', lambda: press('6')), ('*', lambda: press('*')),
    ('n!', lambda: apply_function('fact')), ('%', lambda: press('%')),
    # Row 5
    ('1', lambda: press('1')), ('2', lambda: press('2')), ('3', lambda: press('3')), ('-', lambda: press('-')),
    ('.', lambda: press('.')), ('=', equal),
    # Row 6
    ('0', lambda: press('0')), ('+', lambda: press('+')),
]
# Place buttons in grid (6 columns)
row = 0
col = 0
for (text, command) in buttons:
    btn = Button(frame, text=text, command=command, font=btn_font,
                 bg=btn_bg, fg=btn_fg, activebackground=btn_active,
                 activeforeground='white', relief=FLAT, bd=0)
    btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')
    col += 1
    if col > 5:
        col = 0
        row += 1
# Make rows & columns expand
total_rows = 6
total_cols = 6
for i in range(total_rows):
    frame.grid_rowconfigure(i, weight=1)
for j in range(total_cols):
    frame.grid_columnconfigure(j, weight=1)
root.mainloop()
