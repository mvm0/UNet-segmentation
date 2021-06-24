import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from threading import Thread

import modifyBackground as mB
import predict


# Графический интерфейс
class windowCreator:
    def __init__(self):
        # Поля класса для дальнейшего использования
        self.originalImage = Image
        self.resizedOriginalImage = Image
        self.newImage = Image
        self.resizedNewImage = Image
        self.mask = Image
        self.background = Image
        # Создание и настройка окна
        self.window = tk.Tk()
        self.window.geometry("495x500")  # размеры окна 495x500
        self.window.title("Semantic Segmentation with CNN (U-Net)")  # заголовок окна
        self.window.resizable(False, False)  # запрет на изменение размеров окна

        # Надписи над изображениями
        tk.Label(text="Исходное изображение", font="Arial 13").place(x=160, y=10)
        tk.Label(text="Обработанное изображение", font="Arial 13").place(x=660, y=10)

        # Создание и настройка кнопок
        self.btn1 = tk.Button(text="Выбрать изображение", command=self.click1, font="Arial 11")
        self.btn1.place(height=30, width=460, x=20, y=385)

        self.btn2 = tk.Button(text="Убрать фон", state=tk.DISABLED, command=self.click2, font="Arial 11")
        self.btn2.place(height=30, width=229, x=20, y=420)

        self.btn3 = tk.Button(text="Размыть фон", state=tk.DISABLED, command=self.click3, font="Arial 11")
        self.btn3.place(height=30, width=229, x=20 + 231, y=420)

        self.btn4 = tk.Button(text="Заменить фон на пользовательский",
                              state=tk.DISABLED, command=self.click4, font="Arial 11")
        self.btn4.place(height=30, width=460, x=20, y=455)

        self.btn5 = tk.Button(text="Сохранить обработанное изображение",
                              font="Arial 12", command=self.click5)
        self.btn5.place(height=100, width=460, x=520, y=385)

        # Настройка контейнеров для изображений
        frm1 = tk.Frame(relief=tk.RIDGE, borderwidth=2)
        frm1.place(height=340, width=460, x=20, y=40)
        frm2 = tk.Frame(relief=tk.RIDGE, borderwidth=2)
        frm2.place(height=340, width=460, x=520, y=40)

        # Поля для размытия
        self.frm3 = tk.Frame(relief=tk.RIDGE, borderwidth=2)
        self.label = tk.Label(text="Степень размытия", font="Arial 13")
        self.radiobuttonChecked = tk.IntVar()
        for i in range(1, 11):
            tk.Radiobutton(self.frm3, text=str(i), value=i, variable=self.radiobuttonChecked, padx=5, pady=2,
                           command=self.selectRButton).grid(row=1, column=i-1)

        # Настройка графических областей для изображений
        self.canvas1 = tk.Canvas(frm1, height=340, width=460)
        self.canvas1.pack()
        self.canvas2 = tk.Canvas(frm2, height=340, width=460)
        self.canvas2.pack()

        # Запуск слушателя событий
        self.window.mainloop()

    # Если нажал на кнопку "Выбрать изображение"
    def click1(self):
        pathToFile = tk.filedialog.askopenfilename(filetypes=(("PNG files", "*.png"),
                                                              ("JPG files", "*.jpg"),
                                                              ("JPEG files", "*.jpeg"),
                                                              ("BMP files", "*.bmp")))
        if pathToFile:
            self.originalImage = Image.open(pathToFile)
            self.resizedOriginalImage = self.originalImage
            if self.resizedOriginalImage.size[0] > 460:
                self.resizedOriginalImage = self.originalImage.resize((460, int(460 * self.originalImage.size[1]
                                                                                / self.originalImage.size[0])),
                                                                      Image.ANTIALIAS)
            if self.resizedOriginalImage.size[1] > 340:
                self.resizedOriginalImage = self.originalImage.resize((int(340 * self.originalImage.size[0]
                                                                           / self.originalImage.size[1]), 340),
                                                                      Image.ANTIALIAS)
            self.resizedOriginalImage = ImageTk.PhotoImage(self.resizedOriginalImage)
            self.canvas1.create_image(230, 170, anchor="center", image=self.resizedOriginalImage)

            self.thread1 = Thread(target=self.maskThread)
            self.thread1.start()

            self.btn2.config(state=tk.NORMAL)
            self.btn3.config(state=tk.NORMAL)
            self.btn4.config(state=tk.NORMAL)
            self.window.geometry("495x500")


    def maskThread(self):
        self.mask = predict.predictMask(self.originalImage)



    # Если нажал на кнопку "Убрать фон"
    def click2(self):
        self.thread1.join()
        self.newImage = mB.deleteBackground(self.originalImage, self.mask)
        self.resizeNewImage()
        self.canvas2.create_image(230, 170, anchor="center", image=self.resizedNewImage)

        self.btn5.place(height=100, width=460, x=520, y=385)
        self.frm3.place_forget()
        self.label.place_forget()
        self.window.geometry("1000x500")

    # Если нажал на кнопку "Размыть фон"
    def click3(self):
        self.newImage = self.originalImage
        self.resizeNewImage()
        self.canvas2.create_image(230, 170, anchor="center", image=self.resizedNewImage)

        self.btn5.place(height=40, width=460, x=520, y=445)
        self.frm3.place(height=30, width=430, x=535, y=410)
        self.label.place(x=670, y=385)
        self.window.geometry("1000x500")

    # Если нажал на кнопку "Заменить фон на пользовательский"
    def click4(self):
        pathToFile = tk.filedialog.askopenfilename(filetypes=(("PNG files", "*.png"),
                                                              ("JPG files", "*.jpg"),
                                                              ("JPEG files", "*.jpeg"),
                                                              ("BMP files", "*.bmp")))
        if pathToFile:
            if Image.open(pathToFile).size[0] < self.originalImage.size[0] \
                    or Image.open(pathToFile).size[1] < self.originalImage.size[1]:
                messagebox.showerror(title="Ошибка", message="Размер фона должен быть больше "
                                                             "\nразмера исходного изображения!")
            else:
                self.background = Image.open(pathToFile)
                self.thread1.join()
                self.newImage = mB.changeBackground(self.originalImage, self.mask, self.background)
                self.resizeNewImage()
                self.canvas2.create_image(230, 170, anchor="center", image=self.resizedNewImage)

                self.btn5.place(height=100, width=460, x=520, y=385)
                self.frm3.place_forget()
                self.label.place_forget()
                self.window.geometry("1000x500")

    # Если нажал на кнопку "Сохранить обработанное изображение"
    def click5(self):
        fileName = filedialog.asksaveasfilename(defaultextension="png", filetypes=(("PNG files", "*.png"),
                                                                                   ("BMP files", "*.bmp")))
        if fileName:
            self.newImage.save(fileName)
            print(5)

    # Изменение размера под окно просмотра
    def resizeNewImage(self):
        self.resizedNewImage = self.newImage
        if self.resizedNewImage.size[0] > 460:
            self.resizedNewImage = self.newImage.resize((460, int(460 * self.newImage.size[1]
                                                                  / self.newImage.size[0])),
                                                        Image.ANTIALIAS)
        if self.resizedNewImage.size[1] > 340:
            self.resizedNewImage = self.newImage.resize((int(340 * self.newImage.size[0]
                                                             / self.newImage.size[1]), 340),
                                                        Image.ANTIALIAS)
        self.resizedNewImage = ImageTk.PhotoImage(self.resizedNewImage)

    # Если нажал на один из пунктов
    def selectRButton(self):
        self.thread1.join()
        self.newImage = mB.blurBackground(self.originalImage, self.mask, self.radiobuttonChecked.get())
        self.resizeNewImage()
        self.canvas2.create_image(230, 170, anchor="center", image=self.resizedNewImage)


if __name__ == '__main__':
    mainWindow = windowCreator()
    del mainWindow
