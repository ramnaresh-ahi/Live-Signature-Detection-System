import os
import pickle
import tkinter as tk
from tkinter import messagebox
import cv2


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    orb = cv2.ORB_create()
    _, descriptors_unknown = orb.detectAndCompute(img, None)

    if descriptors_unknown is None:
        print("No descriptors found in the input image.")
        return 'invalid', None

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    for filename in os.listdir(db_path):
        file_path = os.path.join(db_path, filename)
        with open(file_path, 'rb') as file:
            try:
                descriptors_stored = pickle.load(file)
                print(f"Loaded descriptors from {filename}")
            except (pickle.UnpicklingError, EOFError):
                print(f"Error reading file {filename}, skipping...")
                continue

            matches = bf.match(descriptors_stored, descriptors_unknown)
            matches = sorted(matches, key=lambda x: x.distance)

            good_matches = [m for m in matches if m.distance < 50]
            print(f"Number of good matches with {filename}: {len(good_matches)}")

            if len(good_matches) > 35:  
                name = filename.split('.')[0]
                print(f"Match found for {name} with {len(good_matches)} good matches.")
                return 'valid', name

    print("No matching signature found.")
    return 'invalid', None
