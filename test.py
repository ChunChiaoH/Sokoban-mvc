from tkinter import *
from PIL import Image, ImageTk

root = Tk()

topFrame =Frame(root, width=500, height=50,)
topFrame.grid(row=0, column= 0)

btnframe = LabelFrame(topFrame, width = 50, height = 50)
btnframe.place(x = 450, y= 5 )

def Mute():
    pass

mute_image = Image.open("images/broken.png")
mute_image = mute_image.resize((50,50))
mute_icon = ImageTk.PhotoImage(mute_image)

mute_button = Button(btnframe, width=50, height=50,
                     command=Mute, image=mute_icon)
mute_button.image = mute_icon
mute_button.pack()

root.mainloop()
