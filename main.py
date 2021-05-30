from tkinter import *
import pandas
import random
timer = None

BACKGROUND_COLOR = "#B1DDC6"
FONT_1 = ("Ariel", 40, "italic")
FONT_2 = ("Ariel", 60, "bold")
to_learn = {}
current_card = {}
# --------------------------------- RANDOM CARDS ------------------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(main_display, image=card_image)
    canvas.itemconfig(title_text, text="French", fill="Black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="Black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(main_display, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# --------------------------------- UI SETUP ------------------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_image = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
main_display = canvas.create_image(400, 263, image=card_image)
title_text = canvas.create_text(400, 150, text="", font=FONT_1)
word_text = canvas.create_text(400, 263, text="", font=FONT_2)
canvas.grid(row=0, column=0, columnspan=2)
wrong_btn = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_btn.grid(row=1, column=0)
right_btn = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
right_btn.grid(row=1, column=1)

next_card()

window.mainloop()