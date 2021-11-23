from tkinter import *
from tkinter import font
import tkinter.ttk
from PIL import Image, ImageTk
import re

FONT = "Yu Gothic"

def doubts():
    window2 = Tk()
    window2.title("Calculadora Simplex")
    canvas2 = Canvas(
    window,
    bg = "#ffffff",
    height = 1000,
    width = 460,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
    canvas2.create_text(
    0, 0,
    text = "TESTE",
    fill = "#000",
    font = (FONT, int(26.0)))

    window2.mainloop()

def calc():
    error = False
    input_rest = textbox_rest.get("1.0",END)
    if (re.sub("((\d*x\d+|x\d+)(\+|\-))*(\d+)", "", str(input_func.get())) == ""):
        error = True
        print('Yes')
    print(f"{input_func.get()}")
    input_rest = input_rest.split()

    for x in range(len(input_rest)):
        if error == True:
            break
        if (re.sub("((\d*x\d+|x\d+)(\+|\-))*(\d+)", "", str(input_rest[x])) != ""):
            error = True

window = Tk()
input_func = StringVar()
window.title("Calculadora Simplex")
window.geometry("460x590")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 1000,
    width = 460,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

canvas.create_rectangle(0, 0, 460, 70,
    outline="#393939", fill="#393939")

canvas.create_rectangle(0, 70, 460, 1000,
    outline="#D7D7D7", fill="#D7D7D7")

canvas.create_line(20, 468, 440, 468, width=2, fill='#393939')

calcButton = Button(window, text="Calcular", width=27, command=calc, fg="#D7D7D7", bg="#393939", font=(FONT, 14), activebackground="#D7D7D7", activeforeground="#393939")
calcButton.place(x=75, y=480)

photo = PhotoImage(file = r"question-circle.png")

style = tkinter.ttk.Style()
style.configure('TButton',
borderwidth=0, focusthickness=0, focuscolor='none')

questionButton1 = tkinter.ttk.Button(window, image = photo, style="TButton", command=doubts)
questionButton1.place(x=178, y=89)

questionButton2 = tkinter.ttk.Button(window, image = photo, style="TButton", command=doubts)
questionButton2.place(x=130, y=195)

canvas.create_line(20, 537, 440, 537, width=2, fill='#393939')

canvas.create_text(
    230, 35.0,
    text = "Calculadora Simplex",
    fill = "#d7d7d7",
    font = (FONT, int(26.0)))

canvas.create_text(
    100, 100,
    text = "Função Objetivo",
    fill = "#393939",
    font = (FONT, int(14.0)))


canvas.create_text(
    150, 220,
    text = "Restrições\n(Exceto: Não Negatividade)",
    fill = "#393939",
    font = (FONT, int(14.0)))

canvas.create_text(
    230, 565,
    text = "Arthur H Dorneles - 2021",
    fill = "#393939",
    font = (FONT, int(12.0)))

textbox_func = Entry(window, textvariable=input_func, bg="#CBC9C9", fg="#393939", font=(FONT, 10)).place(x=20, y=129, width=420,height=45)
#textbox_func = Text(window, bg="#CBC9C9", fg="#393939", font=(FONT, 12))
#textbox_func.place(x=20, y=129, width=420,height=45)

textbox_rest = Text(window, bg="#CBC9C9", fg="#393939", font=(FONT, 12))
textbox_rest.place(x=20, y=267, width=420,height=175)

window.resizable(False, False)
window.mainloop()