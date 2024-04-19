from tkinter import *
from tkinter import ttk
from tkinter import Menu
from tkinter import scrolledtext
from tkinter.ttk import Combobox
from CopyButton import *
import ttp

class CopyWindow:
    def donothing():
        x = 0

    def copyval(self, win, val):
        win.clipboard_clear()
        win.clipboard_append(val)
        self.msglabel.config(text = "Successfully copyed this to clipboard: " + val)

    def add_button(self, win):
        win.clipboard_clear()

        newbtn = CopyButton(win, self, "TEST BUTTON"+str(self.lastY), "user entered value, eventually", self.lastX, self.lastY)
        self.btn_list.insert(0,newbtn)

        if (self.lastY + 1) == self.maxY:
            self.lastX += 1
            self.lastY = 0
        else:
            self.lastY += 1

    def __init__(self, win):
        
        win.geometry('900x600+250+200')
        win.clipboard_clear()
        self.lastX = 2
        self.lastY = 0
        self.maxX = 10
        self.maxY = 10

        self.btn_list = []

        self.addbtn = CopyButton(win, self, "Add New Button", "init", 0, 0)

        self.msglabel = Label(win)
        self.msglabel.grid(row=1, column=0)