from tkinter import *
from tkinter import messagebox, ttk
import re
import pandas as pd
from pandas.core.base import SelectionMixin
from tabulate import tabulate

FONT = "Yu Gothic"

# <div>Ícones feitos por <a href="https://www.flaticon.com/br/autores/dimitry-miroliubov" title="Dimitry Miroliubov">Dimitry Miroliubov</a> from <a href="https://www.flaticon.com/br/" title="Flaticon">www.flaticon.com</a></div>
def invertSign(function):
    func = ""
    for x in range(len(function)):
        if x == 0:
            if function[x] == "-":
                func += "+"
            elif function[x] == "+":
                func += "-"
            else:
                func += "-" + function[x]
        elif(function[x] == "+"):
            func += "-"
        elif(function[x] == "-"):
            func += "+"
        else:
            func += function[x]
    return func

def my_key(item):
    alpha = ''.join(i for i in item if i.isalpha())
    num = ''.join(i for i in item if i.isdigit())
    if num:
        return (alpha, int(num))
    return (alpha, 0)

def sorting(label):
    if (label == "Z"):
        return 1
    elif (bool(re.match("(x\d+)",label))):
        return 2
    elif (bool(re.match("(xF\d+)",label))):
        return 3
    elif (bool(re.match("(a\d+)",label))):
        return 4
    else:
        return 5
        
def getListVariableValues(variable, function, restrictions):
    list_values = []
    if variable != "b":
        if (function.lower().find(variable.lower()) == -1):
            list_values.append(0)
        else:
            if (bool(re.match("(a\d+)",variable))):
                list_values.append(variable.replace("a","M"))
            else:
                valores =  re.findall("(\+|\-)?(\d+)?"+ variable.lower() +"\D", function.lower())
                value = None
                sign = None
                if valores[0][1] == '':
                    value = 1
                else:
                    value = valores[0][1]
                if valores[0][0] == '+':
                    sign = ''
                else:
                    sign = valores[0][0]
                list_values.append(sign+str(value))
        for r in restrictions:
            if (r.lower().find(variable.lower()) == -1):
                list_values.append(0)
            else:
                valores =  re.findall("(\+|\-)?(\d+)?"+ variable +"\D", r)
                value = None
                sign = None
                if valores[0][1] == '':
                    value = 1
                else:
                    value = valores[0][1]
                if valores[0][0] == '+':
                    sign = ''
                else:
                    sign = valores[0][0]
                list_values.append(sign+str(value))
        return list_values
    else:
        list_values.append(function.split("=")[1])
        for r in restrictions:
            list_values.append(r.split("=")[1])
        return list_values

def genDataForFrame(function, restrictions):
    labels_column = []
    labels_column.append("Z")
    labels_column.append("b")
    for r in restrictions:  
        labels_column += re.findall("(xF\d+|x\d+|a\d+)",r)
    labels_column = list(set(labels_column))
    labels_column.sort()
    labels_column.sort(key=sorting, reverse=False)

    labels_row = []
    labels_row.append("Z")
    for x in range(len(restrictions)):
        labels_row.append("F"+str(x+1))

    data = {}
    for lc in labels_column:
        data[lc]= getListVariableValues(lc, function, restrictions)

    return pd.DataFrame(data, index=labels_row, dtype=object), len(labels_row), len(labels_column)

def adjustFunctions(function, restrictions):
    i=1
    function = function.replace(" ", "")
    
    for x in range(len(restrictions)):
        naoNegatividade = bool(re.match("((x\d+|x\d+),*)+(>=|≥)0",restrictions[x]))
        if not naoNegatividade:
            if restrictions[x].find("<=") != -1 or restrictions[x].find("≤") != -1:
                restrictions[x] = restrictions[x].replace("<=","≤")
                restriction_split = re.split('≤',restrictions[x])
                restrictions[x] = restriction_split[0] + "+xF" + str(i) + "=" + restriction_split[1]
            elif restrictions[x].find(">=") != -1 or restrictions[x].find("≥") != -1:
                restrictions[x] = restrictions[x].replace(">=","≥")
                restriction_split = re.split('≥',restrictions[x])
                restrictions[x] = restriction_split[0] + "-xF" + str(i) + "+a" + str(i) + "=" + restriction_split[1]
                function = function + "-M" + str(i)+ "a" + str(i)
            elif restrictions[x].find("=") != -1:
                function = function + "-M" + str(i)+ "a" + str(i)
                restriction_split = re.split('=',restrictions[x])
                restrictions[x] = restriction_split[0] + "+a" + str(i) + "=" + restriction_split[1]
        i+=1
    
    function = invertSign(function)
    print("Aqui ----------")
    print(re.sub("((\+|\-)*\d*(x\d+|xF\d+|M\d+a\d+))","",function))
    if(re.sub("((\+|\-)*\d*(x\d+|xF\d+|M\d+a\d+))","",function) != ""):
        b = 0 -float(re.sub("((\+|\-)*\d*(x\d+|xF\d+|M\d+a\d+))","",function))
    else:
        b = 0
    function = "z" + function + "=" + str(b)
    return function, restrictions

def calculateWithM(dataframe, n_columns, n_rows, interaction):
    # Finish if M variables equal 0
    variables = VB_VNB(dataframe, n_columns, n_rows)
    stop = True
    for x in range(n_columns):
        if (bool(re.match("a\d+",dataframe.iloc[:, x].name))):
            if variables[dataframe.iloc[:, x].name] != 0:
                stop = False
    if stop:
        print("Remover Colunas M")
        return dataframe, True
    # Get lowest values in z
    lowest_value = None
    lowest_index = None
    # Column, Row, Value
    Pivot = (None,None)
    for x in range(n_columns):
        if(not bool(re.match("(Z|b|a\d+)",dataframe.iloc[[0]].iloc[:, x].name))):
            if(lowest_value == None):
                lowest_value = dataframe.iloc[[0]].iloc[:, x].values[0]
                lowest_index = dataframe.iloc[[0]].iloc[:, x].name
            elif (float(dataframe.iloc[[0]].iloc[:, x].values[0]) < float(lowest_value)):
                lowest_value = dataframe.iloc[[0]].iloc[:, x].values[0]
                lowest_index = dataframe.iloc[[0]].iloc[:, x].name
    # Get if all values are positives
    if(float(lowest_value) >= 0):
        print("Não é possível calcular")
        return dataframe, False
    else:
        # Column, Row, Value
        Pivot = (lowest_index,None,None)
        #Calculate pivot
        for x in range(1,n_rows):
            if(Pivot[2] != None):
                if(float(dataframe[Pivot[0]].iloc[[x]].values[0]) != 0):
                    value = float(dataframe.iloc[[x]].b.values[0])/float(dataframe[Pivot[0]].iloc[[x]].values[0])
                    if (value < float(dataframe.b[Pivot[1]])/float(dataframe[Pivot[0]][Pivot[1]]) and value >=0):
                        Pivot = (Pivot[0],dataframe[Pivot[0]].iloc[[x]].index[0],float(dataframe[Pivot[0]].iloc[[x]].values[0]))
            else:
                if (float(dataframe[Pivot[0]].iloc[[x]].values[0]) != 0):
                    value = float(dataframe.iloc[[x]].b.values[0])/float(dataframe[Pivot[0]].iloc[[x]].values[0])
                    if(value >= 0):
                        Pivot = (Pivot[0],dataframe[Pivot[0]].iloc[[x]].index[0],float(dataframe[Pivot[0]].iloc[[x]].values[0]))
        if(Pivot[2] == None or Pivot[1] == None):
            print("Incapaz de calcular o pivô")
            return dataframe, False
        print(f"PIVOT: {Pivot}")
        # New Pivot Row
        for x in range(n_columns):
            new_value = float(dataframe.iloc[:, x][Pivot[1]])/Pivot[2]
            dataframe.iloc[:, x][Pivot[1]] = new_value
        print("Pivot Row")
        
        print(tabulate(pd.DataFrame(dataframe.loc[Pivot[1],:]), headers = 'keys', tablefmt = 'psql'))
        
        #Calcular novas linhas
        for j in range(n_rows):
            multiplier = -float(dataframe[Pivot[0]].iloc[j])
            for i in range(n_columns):
                # Not Pivot Row
                if dataframe.iloc[:, i].iloc[[j]].index[0] != Pivot[1]:
                    # Not Z Row
                    if j != 0:
                        new_value = (multiplier) * float(dataframe[dataframe.iloc[:, i].iloc[[j]].name][Pivot[1]]) + float(dataframe.iloc[:, i].iloc[[j]].values[0])
                        dataframe[dataframe.iloc[:, i].iloc[[j]].name][dataframe.iloc[:, i].iloc[[j]].index[0]] = new_value
                    else:
                        # New Z
                        if (not bool(re.match("(a\d+)",dataframe.iloc[:, i].iloc[[j]].name))):
                            new_value = (multiplier) * float(dataframe[dataframe.iloc[:, i].iloc[[j]].name][Pivot[1]]) + float(dataframe.iloc[:, i].iloc[[j]].values[0])
                            dataframe[dataframe.iloc[:, i].iloc[[j]].name][dataframe.iloc[:, i].iloc[[j]].index[0]] = new_value
        print(f"This Result after {interaction} interections")
        variables = VB_VNB(dataframe, n_columns, n_rows)
        print(variables)
        print(tabulate(dataframe, headers = 'keys', tablefmt = 'psql'))
        return calculateWithM(dataframe, n_columns, n_rows,interaction+1)

def VB_VNB(dataframe, n_columns, n_rows):
    dict_variaveis = {}

    for i in range(1,n_columns-1):
        num_1 = 0
        linha = None
        for j in range(1,n_rows):
            if(float(dataframe.iloc[:, i].iloc[j]) == 1):
                num_1 +=1
                linha = j
            elif(float(dataframe.iloc[:, i].iloc[j]) != 0):
                num_1 = 2
                linha = j
        if (num_1 != 1):
            dict_variaveis[dataframe.iloc[:, i].name] = 0
        else:
            dict_variaveis[dataframe.iloc[:, i].name] = dataframe.iloc[:,n_columns-1].iloc[linha]
    return dict_variaveis

def removeM(dataframe, n_columns):
    aux = n_columns
    columns_list = dataframe.columns.tolist()
    for i in columns_list:
        print(i)
        if(bool(re.match("a\d+",i))):
            print("Remove")
            dataframe.drop([i], axis='columns', inplace=True)
            aux -=1
    return dataframe, aux

# Tem erro na hora de calcular o pivo
def calculateOptimumValue(dataframe, n_columns, n_rows, interaction):
    # Get lowest values in z
    lowest_value = None
    lowest_index = None
    # Column, Row, Value
    Pivot = (None,None)
    for x in range(n_columns):
        if(not bool(re.match("(Z|b|a\d+)",dataframe.iloc[[0]].iloc[:, x].name))):
            if(lowest_value == None):
                lowest_value = dataframe.iloc[[0]].iloc[:, x].values[0]
                lowest_index = dataframe.iloc[[0]].iloc[:, x].name
            elif (float(dataframe.iloc[[0]].iloc[:, x].values[0]) < float(lowest_value)):
                lowest_value = dataframe.iloc[[0]].iloc[:, x].values[0]
                lowest_index = dataframe.iloc[[0]].iloc[:, x].name
    # Get if all values are positives
    if(float(lowest_value) >= 0):
        print("Não há mais o que calcular")
        return dataframe
    else:
        # Column, Row, Value
        Pivot = (lowest_index,None,None)
        #Calculate pivot
        for x in range(1,n_rows):
            if(Pivot[2] != None):
                if(float(dataframe[Pivot[0]].iloc[[x]].values[0]) != 0):
                    value = float(dataframe.iloc[[x]].b.values[0])/float(dataframe[Pivot[0]].iloc[[x]].values[0])
                    if (value < float(dataframe.b[Pivot[1]])/float(dataframe[Pivot[0]][Pivot[1]]) and value >=0):
                        Pivot = (Pivot[0],dataframe[Pivot[0]].iloc[[x]].index[0],float(dataframe[Pivot[0]].iloc[[x]].values[0]))
            else:
                if (float(dataframe[Pivot[0]].iloc[[x]].values[0]) != 0):
                    value = float(dataframe.iloc[[x]].b.values[0])/float(dataframe[Pivot[0]].iloc[[x]].values[0])
                    if(value >= 0):
                        Pivot = (Pivot[0],dataframe[Pivot[0]].iloc[[x]].index[0],float(dataframe[Pivot[0]].iloc[[x]].values[0]))
        if(Pivot[2] == None or Pivot[1] == None):
            print("Incapaz de calcular o pivô")
            return dataframe, False
        print(f"PIVOT: {Pivot}")
        # New Pivot Row
        for x in range(n_columns):
            new_value = float(dataframe.iloc[:, x][Pivot[1]])/Pivot[2]
            dataframe.iloc[:, x][Pivot[1]] = new_value
        print("Pivot Row")
        
        print(tabulate(pd.DataFrame(dataframe.loc[Pivot[1],:]), headers = 'keys', tablefmt = 'psql'))
        
        #Calcular novas linhas
        for j in range(n_rows):
            multiplier = -float(dataframe[Pivot[0]].iloc[j])
            for i in range(n_columns):
                # Not Pivot Row
                if dataframe.iloc[:, i].iloc[[j]].index[0] != Pivot[1]:
                    # Not Z Row
                    if j != 0:
                        new_value = (multiplier) * float(dataframe[dataframe.iloc[:, i].iloc[[j]].name][Pivot[1]]) + float(dataframe.iloc[:, i].iloc[[j]].values[0])
                        dataframe[dataframe.iloc[:, i].iloc[[j]].name][dataframe.iloc[:, i].iloc[[j]].index[0]] = new_value
                    else:
                        # New Z
                        if (not bool(re.match("(a\d+)",dataframe.iloc[:, i].iloc[[j]].name))):
                            new_value = (multiplier) * float(dataframe[dataframe.iloc[:, i].iloc[[j]].name][Pivot[1]]) + float(dataframe.iloc[:, i].iloc[[j]].values[0])
                            dataframe[dataframe.iloc[:, i].iloc[[j]].name][dataframe.iloc[:, i].iloc[[j]].index[0]] = new_value
        print(f"This Result after {interaction} interections")
        variables = VB_VNB(dataframe, n_columns, n_rows)
        print(variables)
        print(tabulate(dataframe, headers = 'keys', tablefmt = 'psql'))
        return calculateOptimumValue(dataframe, n_columns, n_rows,interaction+1)

def doubtsFunc():
    messagebox.showinfo("Dúvidas", 
    "Variáveis:\nDevem identificadas com a letra x e mais um número. Exemplo: x1\nFunção Objetivo:\nSem usar espaços em branco. Não pode ser usado sinais de maior, menor e igualdade.\nExemplo de Função Objetivo:\n-2x1 + x2 - 4x3 + 400")

def doubtsRests():
    messagebox.showinfo("Dúvidas", 
    "Variáveis:\nDevem identificadas com a letra x e mais um número. Exemplo: x1\nRestrições:\nSem usar espaços em branco.\nExemplos Restrições:\n2x1 + x2 – x3 <= 10\nx1 + x2 + 2x3 >= 20\n2x1 + x2 + 3x3 = 60\n-2x1 - 2x2 – 6x3 ≤ 500\n2x1 + x2 + 2x3 ≥ 10")

def errorPopUp():
    messagebox.showerror("Error", "Função Objetivo ou Restrições inválidas!")

def calc():
    error = False
    input_rest = textbox_rest.get("1.0",END)
    if(str(input_func.get()) == ""):
        error = True
    elif (re.sub("((((\+|-|)(\d*x\d+)))*)((((\+|-|)(\d+)))*)", "", str(input_func.get())) != ""):
        error = True
    input_rest = input_rest.split("\n")
    input_rest.pop()

    if (error != True and len(input_rest) != 0):
        for x in range(len(input_rest)):
            if(str(input_rest[x]) == ""):
                error == True
            elif (re.sub("((((\+|-|)(\d*x\d+)))*)(>=|<=|≥|≤|=)\d+", "", str(input_rest[x])) != ""):
                error = True
    else:
        error = True
    if error:
        errorPopUp()
    else:
        # Formulas
        str_func, input_rest = adjustFunctions(input_func.get(),input_rest)

        df, num_rows, num_columns = genDataForFrame(str_func, input_rest)

        M_Method = False
        for key in VB_VNB(df, num_columns, num_rows):
            if key.startswith("a"):
                print('TRUE')
                M_Method = True

        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
        resposta = 2
        if (M_Method):
            print("M_Method")
            df, continuar = calculateWithM(df, num_columns, num_rows,1)
        else:
            print("NOT M_Method")
            continuar = True

        if(continuar):
            if(M_Method):
                print("Remove M")
                df, num_columns = removeM(df, num_columns)
            print("Normal Simplex")
            print("Calcular Valor Otimo")
            # Calcular valor otimo
            df = calculateOptimumValue(df, num_columns, num_rows, 1)
        elif(M_Method):
            print("Undefined Solution")
            resposta = 0

        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
        print(VB_VNB(df, num_columns, num_rows))
        print(f"Resposta: {resposta}")
        if resposta == 2:
            df_head = df.head(1)
            for x in df.head(1):
                if df_head[x].values[0] < 0:
                    resposta = 1

        valorZ = df['b']['Z']
        Vb = VB_VNB(df, num_columns, num_rows)
        aux = VB_VNB(df, num_columns, num_rows)
        Vnb = {}
        
        for x in aux:
            if(Vb[x] == 0):
                Vnb[x] = Vb.pop(x)
        
        #Vb = '\n'.join(map(str,Vb))
        Vb = '\n'.join('{} : {}'.format(key, round(value, 2)) for key, value in Vb.items())
        Vnb = '\n'.join('{} : {}'.format(key, round(value, 2)) for key, value in Vnb.items())

        # Tela
        result = Tk()
        result.title("Resposta Calculadora Simplex")
        result.geometry("500x400")

        main_frame = Frame(result)
        main_frame.pack(fill=BOTH, expand=1)

        result_canvas = Canvas(
                main_frame,
                bg = "#D7D7D7",
                height = 1000,
                width = 460,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge")
        result_canvas.pack(side=LEFT,fill=BOTH, expand=1)

        Label(result_canvas, text=f"VB:\n{Vb}").place(x = 100,y = 200, anchor = CENTER)
        Label(result_canvas, text=f"VNB:\n{Vb}").place(x = 250,y = 200, anchor = CENTER)
        resposta_str = None
        if(resposta == 2):
            resposta_str = f"Valor de Z:\n{valorZ}\nSolução Ótima"
        else:
            resposta_str = f"Valor de Z:\n{valorZ}\nSolução Não Ótima\n"
            if (resposta == 0):
                resposta_str += f"Indefinido"
            elif (resposta == 1):
                resposta_str += f"Sem Solução"

        Label(result_canvas, text=resposta_str).place(x = 400,y = 200, anchor = CENTER)

        # result_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=result_canvas.yview)
        # result_scrollbar.pack(side=RIGHT,fill=Y)

        # result_canvas.configure(yscrollcommand=result_scrollbar.set)
        # result_canvas.bind('<Configure>', lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))

        # Mostrar Resultado
        tv1 = ttk.Treeview(result_canvas)
        tv1.place(height=150,relwidth=1)
        treescrolly = Scrollbar(tv1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
        treescrollx = Scrollbar(tv1, orient="horizontal", command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")
        # Dataframe to treeview
        tv1["column"] = list(df.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column)
        
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            tv1.insert("", "end", values=row)

        second_frame = Frame(result_canvas)

        result_canvas.create_window((0,0), window=second_frame, anchor="nw")
        result.mainloop()
    
window = Tk()

input_func = StringVar()
window.title("Calculadora Simplex")
ICON = PhotoImage(file='calculadora.png')
window.tk.call('wm', 'iconphoto', window._w, ICON)
window.geometry("460x590")
window.configure(bg = "#D7D7D7")
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

photo = PhotoImage(file = "question-circle.png")

questionButton1 = Button(window, image = photo, border=0, background="#d7d7d7", activebackground="#d7d7d7", command=doubtsFunc)
questionButton1.place(x=178, y=91)

questionButton2 = Button(window, image = photo, border=0, background="#d7d7d7", activebackground="#d7d7d7", command=doubtsRests)
questionButton2.place(x=123, y=199)

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

textbox_func = Entry(window, textvariable=input_func, bg="#CBC9C9", fg="#393939", font=(FONT, 12)).place(x=20, y=129, width=420,height=45)

textbox_rest = Text(window, bg="#CBC9C9", fg="#393939", font=(FONT, 12))
textbox_rest.place(x=20, y=267, width=420,height=175)

window.resizable(False, False)
window.mainloop()