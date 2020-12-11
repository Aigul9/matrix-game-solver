from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from fractions import Fraction
import numpy as np
import sys
import time
import copy


# обработка при нажатии "Выход"
def exit_click():
    if messagebox.askokcancel("Выход", "Вы действительно хотите завершить работу?"):
        root.destroy()


# обработка при нажатии "Помощь"
def about_click():
    messagebox.showinfo("О программе", "Модифицированный симплексный метод 1.0\n"
                                       "Автор: Сибгатуллина А.И.")


# отрисовка формы при нажатии "Ввести вручную"
def hand_click():
    label.pack_forget()
    labelImage.place_forget()
    labelFileName.place_forget()
    fileName_entry.place_forget()
    browse_btn.place_forget()
    file_calc_btn.place_forget()
    count_vars_entry.place(relx=.7, rely=.3, anchor="s")
    count_rest_entry.place(relx=.7, rely=.5, anchor="s")
    next_btn.place(relx=.4, rely=.7)
    labelVars.place(relx=.1, rely=.2)
    labelRest.place(relx=.1, rely=.4)


# отрисовка формы при нажатии "Ввести из файла"
def file_click():
    label.pack_forget()
    labelImage.place_forget()
    labelVars.place_forget()
    labelRest.place_forget()
    count_vars_entry.place_forget()
    count_rest_entry.place_forget()
    next_btn.place_forget()
    labelFileName.place(relx=.1, rely=.2)
    fileName_entry.place(relx=.1, rely=.3)
    browse_btn.place(relx=.7, rely=.5)
    file_calc_btn.place(relx=.4, rely=.7)


# диалоговое окно выбора текстового файла
def open_file_click():
    name = askopenfilename(filetypes=(('text files', 'txt'),))
    try:
        fileName_entry.delete(1.0, END)
        fileName_entry.insert(1.0, name)
    except ValueError:
        fileName_entry.insert(1.0, name)


# отрисовка формы ввода исходных данных
def next_btn_click():
    rest = count_vars.get()
    vars = count_rest.get()
    if vars <= 0 or rest <= 0:
        messagebox.showwarning("Ошибка", "Введите положительные элементы.")
    elif vars > 15 or rest > 15:
        messagebox.showwarning("Ошибка", "Введите меньшее количество элементов.")
    else:
        kf = vars
        if vars < rest:
            kf = rest
        window = Toplevel(root)
        window.geometry("+%d+%d" % (w, h))
        window.configure(background='#cdeae6')
        window.resizable(width=False, height=False)
        label_rest = Label(window, text="Матричная игра:",
                           justify="left",
                           fg="#006080",
                           bg="#cdeae6",
                           font=("Times New Roman", "12"),
                           wraplength=200)
        label_rest.grid(row=0, column=0, columnspan=kf, padx=20, pady=5)
        ent_rest_list = [[] for i in range(rest)]
        for row in range(1, rest+1):
            for col in range(vars):
                ent_rest = IntVar()
                ent = Entry(window, width=6, textvariable=ent_rest)
                if col == 0:
                    ent.grid(row=row, column=col, padx=(20, 0), pady=(10, 0))
                else:
                    ent.grid(row=row, column=col, pady=(10, 0))
                ent_rest_list[row - 1].append(ent_rest)
        calc_btn = Button(window, text="Рассчитать",
                          width=10,
                          height=1,
                          bd=1,
                          relief="ridge",
                          command=lambda: calc_func(vars, rest, ent_rest_list))
        calc_btn.grid(row=rest+1,
                      column=kf+1,
                      padx=20,
                      pady=20)


# получение введенных данных
def calc_func(vars, rest, ent_rest_list):
    vars_list = [1] * vars
    b_list = [1] * rest
    rest_list = [[] for i in range(rest)]
    for row in range(rest):
        for col in range(vars):
            rest_list[row].append(ent_rest_list[row][col].get())
    simplex(vars, rest, vars_list, b_list, rest_list, 1)


# считывание данных из файла
def file_calc_func():
    file_name = fileName_entry.get(1.0, END).rstrip()
    with open(file_name, "r") as f:
        kol = int(f.readline().rstrip())
        for k in range(kol):
            rest = int(f.readline().rstrip())
            vars = int(f.readline().rstrip())
            if vars <= 0 or rest <= 0:
                messagebox.showwarning("Ошибка", "Количество переменных и ограничений должно быть положительно.")
                return
            rest_list = []
            for i in range(rest):
                rest_list.append(f.readline())
            rest_list = [line.rstrip().split(" ") for line in rest_list]
            for i in range(len(rest_list)):
                for j in range(len(rest_list[i])):
                    rest_list[i][j] = int(rest_list[i][j])
            vars_list = [1] * vars
            b_list = [1] * rest
            simplex(vars, rest, vars_list, b_list, rest_list, k+1)


def save_file_click(A, x, y, v):
    f = open("output/results.txt", 'a')
    f.write("A: " + str(A) + "\nx: ")
    for i in x:
        f.write(str(i) + " ")
    f.write("\ny: ")
    for i in y:
        f.write(str(i) + " ")
    f.write("\nv: " + str(v) + "\n\n")
    f.close()
    messagebox.showinfo("Сохранение", "Результаты сохранены!")


# основной метод
def simplex(n, m, c, b, A, kol):
    for i in range(m):
        row_min = min(A[i])
        for j in range(n):
           column = [col[j] for col in A]
           col_max = max(column)
           if col_max == row_min:
               str1 = "Матричная игра №" + str(kol) + " может быть решена в чистых стратегиях:\n" + \
                     "Цена игры: " + str(col_max) + "\n" + "Стратегия 1-го игрока: " + str((i + 1)) + "\n" +\
                      "Стратегия 2-го игрока: " + str((j + 1))
               messagebox.showinfo("Результат", str1)
               return

    window = Toplevel(root)
    window.withdraw()
    window.geometry("310x270+{}+{}".format(w, h))
    window.configure(background='#cdeae6')
    window.resizable(width=False, height=False)
    label_kol = Label(window, text="Задача № " + str(kol),
                      justify="left",
                      fg="#006080",
                      bg="#cdeae6",
                      font=("Times New Roman", "12"),
                      wraplength=230)
    label_kol.place(relx=.1, rely=.0)
    label_x = Label(window, text="x:",
                         justify="left",
                         fg="#006080",
                         bg="#cdeae6",
                         font=("Times New Roman", "12"),
                         wraplength=230)
    label_x.place(relx=.1, rely=.1)
    entResX = Entry(window, width=40)
    entResX.place(relx=.1, rely=.2)
    label_y = Label(window, text="y:",
                    justify="left",
                    fg="#006080",
                    bg="#cdeae6",
                    font=("Times New Roman", "12"),
                    wraplength=230)
    label_y.place(relx=.1, rely=.3)
    entResY = Entry(window, width=40)
    entResY.place(relx=.1, rely=.4)
    label_F = Label(window, text="Цена игры:",
                    justify="left",
                    fg="#006080",
                    bg="#cdeae6",
                    font=("Times New Roman", "12"),
                    wraplength=230)
    label_F.place(relx=.1, rely=.5)
    entResF = Entry(window, width=40)
    entResF.place(relx=.1, rely=.6)
    save_btn = Button(window, text="Сохранить в файл",
                      width=20,
                      height=1,
                      bd=1,
                      relief="ridge",
                      command=lambda: save_file_click(A1, x_res, y_res, v))
    save_btn.place(relx=.3, rely=.8)
    # A - матрица коэффициентов
    # b - столбец свободных членов
    # x - базисные переменные
    # B - матрица базисных коэффициентов
    # n - количество переменных
    # m - количество строк-ограничений
    # c - коэффициенты целевой функции
    # B_1 - обратная матрица
    start_time = time.time()
    A1 = copy.deepcopy(A)
    # поиск базисных переменных
    minimum = min([e for elem in A for e in elem])
    if minimum < 0:
        for i in range(m):
            for j in range(n):
                A[i][j] -= (minimum - 1)
    x = []
    for i in range(m):
        for j in range(m):
            if i == j:
                A[i].append(1)
            else:
                A[i].append(0)
        x.append(n + i)
        c.append(0)
    B = [[] for i in range(len(x))]
    for i in range(len(x)):
        for j in range(len(x)):
            B[i].append(A[i][x[j]])
    B_1 = np.linalg.inv(B)
    B_1 = B_1.astype(np.int64)
    B_1P = np.dot(B_1, b)
    while True:
        # запись базисных коэффициентов
        c_B = []
        for i in range(len(x)):
            c_B.append(c[x[i]])
        lamb = np.dot(c_B, B_1)
        # поиск оценок
        rates = []
        for i in range(n):
            P_j = [col[i] for col in A]
            rates.append(np.dot(lamb, P_j) - c[i])
        # r - входящий элемент
        r = 0
        for i in range(len(rates)):
            if rates[i] < 0:
                min_rate = min(rates)
                r = rates.index(min_rate)
                break
            # базис оптимален
            elif i == len(rates) - 1:
                v_res = [0] * n
                for p in range(n):
                    for j in range(len(x)):
                        if x[j] == p:
                            v_res[p] = B_1P[j]
                u_res = list(np.dot(c_B, B_1))
                v = Fraction(1, sum(v_res))
                x_res = [i * v for i in u_res]
                y_res = [i * v for i in v_res]
                entResX.insert(0, x_res)
                entResY.insert(0, y_res)
                if minimum < 0:
                    v += minimum - 1
                entResF.insert(0, v)
                window.deiconify()
                return
        col_in_A = [col[r] for col in A]    # ведущий столбец
        B_1Pj = np.dot(B_1, col_in_A)
        columns = []
        for i in range(len(x)):
            try:
                columns.append(Fraction(B_1P[i], B_1Pj[i]))
            except ZeroDivisionError:
                columns.append(-sys.maxsize)
        min_value = min([n for n in columns if n >= 0])
        ind_s = columns.index(min_value)
        # s - выводимый элемент
        s = x[ind_s]
        # преобразования Гаусса
        B_1 = B_1.astype(object)
        for j in range(len(B_1)):
            B_1[ind_s][j] = Fraction(B_1[ind_s][j], B_1Pj[ind_s])
        B_1P = B_1P.astype(object)
        B_1P[ind_s] = Fraction(B_1P[ind_s], B_1Pj[ind_s])
        for i in range(len(B)):
            for j in range(len(B)):
                if i != ind_s:
                    B_1[i][j] = B_1[i][j] - B_1[ind_s][j] * B_1Pj[i]
                else:
                    continue
            if i != ind_s:
                B_1P[i] = B_1P[i] - B_1P[ind_s] * B_1Pj[i]
        # новый базис
        x.insert(ind_s, r)
        x.remove(s)


# Начальное окно
root = Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 2
w = w - 200
h = h - 200
root.title("Программа")
root.geometry("400x310+{}+{}".format(w, h))
root.configure(background='#cdeae6')
root.resizable(width=False, height=False)
label = Label(text="Модифицированный симплексный метод",
               fg="#006080",
               bg="#cdeae6",
               anchor="e",
               bd=7,
               font=("Times New Roman", "16", "bold"),
               wraplength=300)
label.pack(expand="False", side="top")
logo = PhotoImage(file="assets/matrix.png")
labelImage = Label(bd=0,
                   image=logo)
labelImage.place(x=45, y=100)

main_menu = Menu()
settings_menu = Menu(tearoff=0)
settings_menu.add_command(label="Ввести из файла", command=file_click)
settings_menu.add_command(label="Ввести вручную", command=hand_click)
help_menu = Menu(tearoff=0)
help_menu.add_command(label="О программе", command=about_click)
main_menu.add_cascade(label="Новый расчет", menu=settings_menu)
main_menu.add_cascade(label="Помощь", menu=help_menu)
main_menu.add_cascade(label="Выход", command=exit_click)
root.config(menu=main_menu)

labelVars = Label(text="Введите количество стратегий 1-го игрока: ",
                  justify="left",
                  fg="#006080",
                  bg="#cdeae6",
                  font=("Times New Roman", "12"),
                  wraplength=200)
labelRest = Label(text="Введите количество стратегий 2-го игрока: ",
                  justify="left",
                  fg="#006080",
                  bg="#cdeae6",
                  font=("Times New Roman", "12"),
                  wraplength=200)
count_vars = IntVar()
count_vars_entry = Entry(textvariable=count_vars)
count_rest = IntVar()
count_rest_entry = Entry(textvariable=count_rest)
next_btn = Button(text="Далее",
                  width=10,
                  height=1,
                  bd=1,
                  relief="ridge",
                  command=next_btn_click)

labelFileName = Label(text="Путь к файлу:",
                      justify="left",
                      fg="#006080",
                      bg="#cdeae6",
                      font=("Times New Roman", "12"),
                      wraplength=200)
fileName_entry = Text(height=3, width=39)
browse_btn = Button(text="Открыть",
                    width=10,
                    height=1,
                    bd=1,
                    relief="ridge",
                    command=open_file_click)
file_calc_btn = Button(text="Рассчитать",
                       width=10,
                       height=1,
                       bd=1,
                       relief="ridge",
                       command=file_calc_func)

root.mainloop()
