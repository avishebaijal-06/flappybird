from tkinter import *
screen=Tk() 
screen.config(relief="sunken",border=20)
screen.geometry("600x600")
Label(screen,text="toy shop",fg="green").pack(pady=20)
Entry(screen).pack(pady=10)
Button(screen,text="click here").pack()
screen.mainloop()