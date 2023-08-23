import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

def calculate_color_similarity(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2)) * 100 / np.sqrt(255 ** 2 * 3)

def click_color(event):
    global clicked_color, first_color_clicked
    x, y = event.x, event.y
    b, g, r = image[y, x]
    clicked_color = (r, g, b)
    
    if not first_color_clicked:
        first_color_clicked = True
        canvas.config(cursor="hand2")
        message_label.config(text="Clique no objeto a ser comparado")
    else:
        similarity = calculate_color_similarity(clicked_color, target_color)
        result_label.config(text=f"Similarity: {similarity:.2f}%")

def compare_colors():
    global first_color_clicked
    first_color_clicked = False
    canvas.config(cursor="hand2")
    message_label.config(text="Clique no objeto de referência")
    result_label.config(text="")
    compare_button.config(state="disabled")

def upload_image():
    global image, target_color, first_color_clicked
    first_color_clicked = False

    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        target_color = image[0, 0]

        img = Image.fromarray(image)
        img.thumbnail((600, 600))
        img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=img)
        canvas.image = img

        canvas.config(cursor="hand2")
        message_label.config(text="Clique no objeto de referência")
        result_label.config(text="")
        compare_button.config(state="disabled")

# Create the main application window
app = tk.Tk()
app.title("GPSOFT - Sistema de Comparações Similares de Cores")

# Create widgets
canvas = tk.Canvas(app, width=600, height=600)
canvas.pack()

upload_button = tk.Button(app, text="Upload Image", command=upload_image)
upload_button.pack()

message_label = tk.Label(app, text="Clique no objeto de referência")
message_label.pack()

compare_button = tk.Button(app, text="Compare Colors", command=compare_colors, state="disabled")
compare_button.pack()

result_label = tk.Label(app, text="")
result_label.pack()

image = None
target_color = None
clicked_color = None
first_color_clicked = False

canvas.bind("<Button-1>", click_color)

app.mainloop()
