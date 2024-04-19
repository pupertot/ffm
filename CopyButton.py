from curses.textpad import Textbox
from tkinter import *
from tkinter import ttk
from tkinter import Menu
from tkinter import scrolledtext
from tkinter.ttk import Combobox

class CopyButton(Button):

    def right_click(self, event):
        event.widget.configure(bg="red")

    def __init__(self, win, cpwin, txt, copy_text, xLoc, yLoc):
        super().__init__(win, text=txt)
        
        if copy_text == "init":
            self.configure(command=lambda : cpwin.add_button(win))
        else:
            self.configure(command=lambda : cpwin.copyval(win, copy_text))
        
        self.x = xLoc
        self.y = yLoc
        self.grid(row=self.x, column=self.y)
        self.win = win
        self.text = txt
        self.copy_text = copy_text
        self.bind("<Button-3>", print("wtf"))
        self.bkgcolor = 'light blue'
        self.configure(bg=self.bkgcolor)
        self.bind("<Button-3>", self.right_click)
        