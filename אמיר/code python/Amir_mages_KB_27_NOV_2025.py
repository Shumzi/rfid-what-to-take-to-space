import tkinter as tk
from PIL import Image, ImageTk, ImageOps

# consts
STRING_END = "Return"
RFID_1 = "4294947269"  # card tad
RFID_2 = "11579"  # blue tag
RFID_3 = "15834"  # sticker 1
RFID_4 = "15578"  # sticker 2
RFID_5 = "15322"  # sticker 3
RFID_6 = "15066"  # sticker 4

BG_IMAGE_SIZE = [1200, 900]
BG_IMAGE_TL = [0, 0]

IMAGE_PREFIX = "pic/IMAGE_"
IMAGE_TYPE = ".jpg"  # png
START_BG_IMAGE_INDEX = 7

# globals
current_bg_image_index = START_BG_IMAGE_INDEX
bg_image_tk = None
input_string = ""
# ====
root = tk.Tk()
root.title("RFID READ TEST")
root.geometry("1200x900")  #
canvas = tk.Canvas(root)
# canvas = tk.Canvas(root,width=80,height=80)
canvas.pack(fill="both", expand=True)


def load_BG_image(image_name, X_size, Y_size, Left, Top):
    global bg_image_tk  # !!!!!
    try:
        bg_image_pil = Image.open(image_name)
    except FileNotFoundError:
        print(f"Error: Background image '{image_name}' not found.")
        root.destroy()
        return
    resize_image = bg_image_pil.resize((X_size, Y_size), Image.Resampling.BICUBIC)
    bg_image_tk = ImageTk.PhotoImage(resize_image)
    canvas.create_image(Left, Top, image=bg_image_tk, anchor="nw")


def load_BG_image_INDEX(image_index):
    bk_image_name = IMAGE_PREFIX + str(image_index) + IMAGE_TYPE
    load_BG_image(bk_image_name, BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1], BG_IMAGE_TL[0], BG_IMAGE_TL[1])


def index_up(index_type):

    global input_string
    global current_bg_image_index, current_fg_image_index
    print(index_type)
    print(input_string)
    input_string = input_string + index_type
    if index_type == STRING_END:
        if input_string == RFID_1 + STRING_END:
            load_BG_image_INDEX(1)
        elif input_string == RFID_2 + STRING_END:
            load_BG_image_INDEX(2)
        elif input_string == RFID_3 + STRING_END:
            load_BG_image_INDEX(3)
        elif input_string == RFID_4 + STRING_END:
            load_BG_image_INDEX(4)
        elif input_string == RFID_5 + STRING_END:
            load_BG_image_INDEX(5)
        elif input_string == RFID_6 + STRING_END:
            load_BG_image_INDEX(6)
        else:
            load_BG_image_INDEX(7)

        input_string = ""


def on_keypress(event):
    index_up(event.keysym)


def give_focus(event):
    canvas.focus_set()


canvas.bind("<Enter>", give_focus)
canvas.bind("<Key>", on_keypress)

####reset####
load_BG_image_INDEX(current_bg_image_index)
canvas.focus_set()

root.mainloop()
