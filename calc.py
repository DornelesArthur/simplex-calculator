from tkinter import *
from tkinter import messagebox
import tkinter.ttk
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

def errorPopUp():
    messagebox.showerror("Error", "Função Objetivo ou Restrições inválidas!")

def calc():
    error = False
    input_rest = textbox_rest.get("1.0",END)
    if(str(input_func.get()) == ""):
        error = True
    elif (re.sub("((((\+|-|)( *)(\d*x\d+)( *)))*)((((\+|-|)( *)(\d+)( *)))*)", "", str(input_func.get())) != ""):
        error = True
    input_rest = input_rest.split("\n")
    input_rest.pop()

    if (error != True and len(input_rest) != 0):
        print("Error False")
        print(len(input_rest))
        for x in range(len(input_rest)):
            if(str(input_rest[x]) == ""):
                error == True
            elif (re.sub("((((\+|-|)( *)(\d*x\d+)( *)))*)(>=|<=|≥|≤|=)( *)\d+", "", str(input_rest[x])) != ""):
                error = True
    else:
        error = True
    if error:
        errorPopUp()
    else:
        pass
    
window = Tk()

input_func = StringVar()
window.title("Calculadora Simplex")
window.geometry("460x590")
window.configure(bg = "#D7D7D7")
frame = Frame(window)
canvas = Canvas(
    window,
    bg = "#D7D7D7",
    height = 1000,
    width = 460,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

canvas.create_rectangle(0, 0, 460, 70,
    outline="#393939", fill="#393939")

#canvas.create_rectangle(0, 70, 460, 1000,
#    outline="#D7D7D7", fill="#D7D7D7")

canvas.create_line(20, 468, 440, 468, width=2, fill='#393939')

calcButton = Button(window, text="Calcular", width=27, command=calc, fg="#D7D7D7", bg="#393939", font=(FONT, 14), activebackground="#D7D7D7", activeforeground="#393939")
calcButton.place(x=55, y=485)

photo = PhotoImage(file = "question-circle3.png")

style = tkinter.ttk.Style()
style.configure('TButton', border=0,
borderwidth=0, focusthickness=0, focuscolor='none')
frame.place(x=178, y=89)
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

textbox_rest = Text(window, bg="#CBC9C9", fg="#393939", font=(FONT, 12))
textbox_rest.place(x=20, y=267, width=420,height=175)

window.resizable(False, False)
window.mainloop()