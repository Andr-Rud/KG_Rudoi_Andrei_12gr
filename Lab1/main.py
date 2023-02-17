from tkinter import colorchooser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

color_code = (1, 1, 1)


def digit(st):
    if len(st) > 0:
        if st[0] == '-':
            if len(st) > 1 and st[1:].isdigit():
                return True
            else:
                return False
        else:
            if st.isdigit():
                return True
            else:
                return False
    else:
        return False


def get_rgb(rgb):
    return "#%02x%02x%02x" % rgb


root = Tk()


def F1(x):
    if x >= 0.04045:
        return ((x + 0.055) / 1.055) ** (2.4)
    else:
        return x / 12.92


def F2(x):
    if x >= 0.008856:
        return x ** (1 / 3)
    else:
        return 7.787 * x + 16 / 116


def F3(x):
    if x ** 3 >= 0.008856:
        return x ** 3
    else:
        return (x - 16 / 116) / 7.787


def F4(x):
    if x >= 0.0031308:
        return 1.055 * x ** (1 / 2.5) - 0.055
    else:
        return x * 12.92


def CMYK_to_RGB(C1, M1, Y1, K1):
    C = C1 / 100
    M = M1 / 100
    K = K1 / 100
    Y = Y1 / 100

    R = 255 * (1 - C) * (1 - K)
    G = 255 * (1 - M) * (1 - K)
    B = 255 * (1 - Y) * (1 - K)
    return R, G, B


def RGB_to_XYZ(R, G, B):
    Rn = F1(R / 255) * 100
    Gn = F1(G / 255) * 100
    Bn = F1(B / 255) * 100

    X = 0.412453 * Rn + 0.357580 * Gn + 0.180423 * Bn
    Y = 0.212671 * Rn + 0.715160 * Gn + 0.072169 * Bn
    Z = 0.019334 * Rn + 0.119193 * Gn + 0.950227 * Bn

    return X, Y, Z


def XYZ_to_LAB(X, Y, Z):
    Xw = 95.047
    Yw = 100.0
    Zw = 108.883

    L = 116 * F2(Y / Yw) - 16
    A = 500 * (F2(X / Xw) - F2(Y / Yw))
    B = 200 * (F2(Y / Yw) - F2(Z / Zw))

    return L, A, B


def LAB_to_XYZ(L, A, B):
    Xw = 95.047
    Yw = 100.0
    Zw = 108.883

    Y = F3((L + 16) / 116) * Xw
    X = F3(A / 500 + (L + 16) / 116) * Yw
    Z = F3((L + 16) / 116 - B / 200) * Zw

    return X, Y, Z


def XYZ_to_RGB(X, Y, Z):
    X1 = X / 100
    Y1 = Y / 100
    Z1 = Z / 100

    Rn = 3.2406 * X1 - 1.5372 * Y1 - 0.4986 * Z1
    Gn = -0.9689 * X1 + 1.8758 * Y1 + 0.0415 * Z1
    Bn = 0.0557 * X1 - 0.2040 * Y1 + 1.0570 * Z1

    R = F4(Rn) * 255
    G = F4(Gn) * 255
    B = F4(Bn) * 255

    return R, G, B


def RGB_to_CMYK(R, G, B):
    K = min(1 - R / 255, 1 - G / 255, 1 - B / 255)
    C = (1 - R / 255 - K) / (1 - K)
    M = (1 - G / 255 - K) / (1 - K)
    Y = (1 - B / 255 - K) / (1 - K)

    return C, M, Y, K


def choose_color():
    global label

    color_code = colorchooser.askcolor(title="Choose color")
    print(color_code)
    label = ttk.Label(text="",
                      padding=40,
                      background=get_rgb(color_code[0]))

    label.place(x=100, y=10)

    C1, M1, Y1, K1 = RGB_to_CMYK(*color_code[0])

    X3, Y3, Z3 = RGB_to_XYZ(*color_code[0])

    L2, A2, B2 = XYZ_to_LAB(X3, Y3, Z3)

    txt_C1.delete(0, END)
    txt_C1.insert(INSERT, int(C1 * 100))

    txt_M1.delete(0, END)
    txt_M1.insert(INSERT, int(M1 * 100))

    txt_Y1.delete(0, END)
    txt_Y1.insert(INSERT, int(Y1 * 100))

    txt_K1.delete(0, END)
    txt_K1.insert(INSERT, int(K1 * 100))

    txt_L2.delete(0, END)
    txt_L2.insert(INSERT, int(L2))

    txt_A2.delete(0, END)
    txt_A2.insert(INSERT, int(A2))

    txt_B2.delete(0, END)
    txt_B2.insert(INSERT, int(B2))

    txt_X3.delete(0, END)
    txt_X3.insert(INSERT, int(X3))

    txt_Y3.delete(0, END)
    txt_Y3.insert(INSERT, int(Y3))

    txt_Z3.delete(0, END)
    txt_Z3.insert(INSERT, int(Z3))


def button1_click():
    C1 = txt_C1.get()
    M1 = txt_M1.get()
    Y1 = txt_Y1.get()
    K1 = txt_K1.get()

    if digit(C1) and digit(M1) and digit(Y1) and digit(K1):
        C1 = int(C1)
        M1 = int(M1)
        Y1 = int(Y1)
        K1 = int(K1)

        R, G, B = CMYK_to_RGB(C1, M1, Y1, K1)

        X, Y, Z = RGB_to_XYZ(R, G, B)

        L1, A1, B1 = XYZ_to_LAB(X, Y, Z)

        color_code = (int(R), int(G), int(B))
        print(color_code)

        if R >= 256 or G >= 256 or B >= 256 or R < 0 or G < 0 or B < 0:

            mb.showerror(
                "Ошибка",
                "Данные введены неверно")

        else:

            txt_L2.delete(0, END)
            txt_L2.insert(INSERT, int(L1))

            txt_A2.delete(0, END)
            txt_A2.insert(INSERT, int(A1))

            txt_B2.delete(0, END)
            txt_B2.insert(INSERT, int(B1))

            txt_X3.delete(0, END)
            txt_X3.insert(INSERT, int(X))

            txt_Y3.delete(0, END)
            txt_Y3.insert(INSERT, int(Y))

            txt_Z3.delete(0, END)
            txt_Z3.insert(INSERT, int(Z))

            label = ttk.Label(text="",
                              padding=40,
                              background=get_rgb(color_code))

            label.place(x=100, y=10)
    else:
        mb.showerror(
            "Ошибка",
            "Ожидались числовые значения")


def button2_click():
    L2 = txt_L2.get()
    A2 = txt_A2.get()
    B2 = txt_B2.get()

    if digit(L2) and digit(A2) and digit(B2):
        L2 = int(L2)
        A2 = int(A2)
        B2 = int(B2)

        X, Y, Z = LAB_to_XYZ(L2, A2, B2)

        R, G, B = XYZ_to_RGB(X, Y, Z)

        C, M, Y2, K = RGB_to_CMYK(R, G, B)

        color_code = (int(R), int(G), int(B))
        print(color_code)

        if R >= 256 or G >= 256 or B >= 256 or R < 0 or G < 0 or B < 0:

            mb.showerror(
                "Ошибка",
                "Данные введены неверно")

        else:

            txt_C1.delete(0, END)
            txt_C1.insert(INSERT, int(C * 100))

            txt_M1.delete(0, END)
            txt_M1.insert(INSERT, int(M * 100))

            txt_Y1.delete(0, END)
            txt_Y1.insert(INSERT, int(Y2 * 100))

            txt_K1.delete(0, END)
            txt_K1.insert(INSERT, int(K * 100))

            txt_X3.delete(0, END)
            txt_X3.insert(INSERT, int(X))

            txt_Y3.delete(0, END)
            txt_Y3.insert(INSERT, int(Y))

            txt_Z3.delete(0, END)
            txt_Z3.insert(INSERT, int(Z))

            color_code = (int(R), int(G), int(B))

            global label
            print(color_code)
            label = ttk.Label(text="",
                              padding=40,
                              background=get_rgb(color_code))

            label.place(x=100, y=10)
    else:
        mb.showerror(
            "Ошибка",
            "Ожидались числовые значения")


def button3_click():
    X3 = txt_X3.get()
    Y3 = txt_Y3.get()
    Z3 = txt_Z3.get()

    if digit(X3) and digit(Y3) and digit(Z3):
        X3 = int(X3)
        Y3 = int(Y3)
        Z3 = int(Z3)

        R, G, B = XYZ_to_RGB(X3, Y3, Z3)

        C, M, Y, K = RGB_to_CMYK(R, G, B)

        L1, A1, B1 = XYZ_to_LAB(X3, Y3, Z3)

        color_code = (int(R), int(G), int(B))
        print(color_code)

        if R >= 256 or G >= 256 or B >= 256 or R < 0 or G < 0 or B < 0:

            mb.showerror(
                "Ошибка",
                "Данные введены неверно")

        else:

            txt_C1.delete(0, END)
            txt_C1.insert(INSERT, int(C * 100))

            txt_M1.delete(0, END)
            txt_M1.insert(INSERT, int(M * 100))

            txt_Y1.delete(0, END)
            txt_Y1.insert(INSERT, int(Y * 100))

            txt_K1.delete(0, END)
            txt_K1.insert(INSERT, int(K * 100))

            txt_L2.delete(0, END)
            txt_L2.insert(INSERT, int(L1))

            txt_A2.delete(0, END)
            txt_A2.insert(INSERT, int(A1))

            txt_B2.delete(0, END)
            txt_B2.insert(INSERT, int(B1))

            color_code = (int(R), int(G), int(B))

            global label
            print(color_code)
            label = ttk.Label(text="",
                              padding=40,
                              background=get_rgb(color_code))

            label.place(x=100, y=10)
    else:
        mb.showerror(
            "Ошибка",
            "Ожидались числовые значения")


button = Button(root, text="Select color",
                command=choose_color)
button.place(x=0, y=10)

lbl_C1 = Label(text="C:")
lbl_M1 = Label(text="M:")
lbl_Y1 = Label(text="Y:")
lbl_K1 = Label(text="K:")

txt_C1 = Entry(root, width=15)
txt_M1 = Entry(root, width=15)
txt_Y1 = Entry(root, width=15)
txt_K1 = Entry(root, width=15)
btn_1 = Button(root, text="Enter", command=button1_click, width=15)

lbl_C1.pack()
txt_C1.pack()
lbl_M1.pack()
txt_M1.pack()
lbl_Y1.pack()
txt_Y1.pack()
lbl_K1.pack()
txt_K1.pack()
btn_1.pack()

Label(text="").pack()
Label(text="").pack()

lbl_L2 = Label(text="L:")
lbl_A2 = Label(text="A:")
lbl_B2 = Label(text="B:")

txt_L2 = Entry(root, width=15)
txt_A2 = Entry(root, width=15)
txt_B2 = Entry(root, width=15)
btn_2 = Button(root, text="Enter", command=button2_click, width=15)

lbl_L2.pack()
txt_L2.pack()
lbl_A2.pack()
txt_A2.pack()
lbl_B2.pack()
txt_B2.pack()
btn_2.pack()

Label(text="").pack()
Label(text="").pack()

lbl_X3 = Label(text="X:")
lbl_Y3 = Label(text="Y:")
lbl_Z3 = Label(text="Z:")

txt_X3 = Entry(root, width=15)
txt_Y3 = Entry(root, width=15)
txt_Z3 = Entry(root, width=15)
btn_3 = Button(root, text="Enter", command=button3_click, width=15)

lbl_X3.pack()
txt_X3.pack()
lbl_Y3.pack()
txt_Y3.pack()
lbl_Z3.pack()
txt_Z3.pack()
btn_3.pack()

root.geometry("2000x2000")
root.mainloop()