#import tkinter as tk
#import tkinter.messagebox

#top = tk.Tk()

#def helloCallBack():  
#    tkinter.messagebox.showinfo( "Hello Python", "Hello World")
#B = tkinter.Button(top, text ="Hello", command = helloCallBack)

#B.pack()
#op.mainloop()

#from tkinter import *
import tkinter

root = tkinter.Tk(  )
for r in range(50):
   for c in range(50):
      tkinter.Frame(root, bg='white', height='20', width='20', bd=0, highlightbackground='black', highlightcolor='black', highlightthickness='.5').grid(row=r,column=c)
root.mainloop(  )