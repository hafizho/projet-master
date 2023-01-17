from PIL import Image, ImageTk
import tkinter as tk
import time

IMAGE_PATH = './imgs/11.png'
WIDTH, HEIGTH = 800, 900

screen = tk.Tk()
#window = Toplevel(screen)
#window.state('zoomed')
screen.geometry('{}x{}'.format(WIDTH, HEIGTH))

canvas = tk.Canvas(screen, width=WIDTH, height=HEIGTH)
canvas.pack()

img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize(
    (WIDTH, HEIGTH), Image.ANTIALIAS))
canvas.background = img
bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)


screen.after(2500, screen.destroy)
screen.mainloop()
if True:
    import login

