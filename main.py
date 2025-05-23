import numpy as np
import cv2
import os
import PIL
from PIL import ImageTk
import PIL.Image
import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import Label, Text, Button
from keras.models import load_model
from keras.preprocessing import image

# Load trained model
MODEL_PATH = 'model.h5'
classifier = load_model(MODEL_PATH)

# Constants
IMAGE_SIZE = (64, 64)
CHARACTERS = "ABCDEFGHIJKMNOPQRSTUVWXYZ"

# Paths
OP_DEST = r"E:\Python_projects\New folder\fitered_data"
ALPHA_DEST = r"E:\Python_projects\New folder\alphabet"

# Prepare file map
file_map = {}
for file in os.listdir(OP_DEST):
    if file.endswith(".webp"):
        word_key = file.replace(".webp", "").lower()
        file_map[word_key] = file


def check_similarity(word):
    """Check if the word exists in file_map"""
    word = word.lower()
    if word in file_map:
        return file_map[word]
    return None


def generate_gif(text):
    """Generate sign language GIF"""
    frames = []
    words = text.lower().split()

    for word in words:
        file = check_similarity(word)
        if file:
            img = PIL.Image.open(os.path.join(OP_DEST, file)).convert("RGBA")
            frames.append(img)
        else:
            for char in word:
                try:
                    img = PIL.Image.open(os.path.join(ALPHA_DEST, f"{char.lower()}_small.gif")).convert("RGBA")
                    frames.append(img)
                except Exception as e:
                    print(f"Error loading {char}:", e)

    if frames:
        frames[0].save("output.gif", save_all=True, append_images=frames[1:], duration=1000, loop=0)
    return frames


class SpeechToSignApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech to Sign Language Translator")
        self.geometry("800x600")
        self.configure(bg="#e6f7ff")  # Light pastel blue background

        Label(self, text="Speech to Sign Language Translator", font=("Verdana", 14, "bold"), bg="#e6f7ff").pack(pady=10)

        self.frames = []
        self.index = 0
        self.label = Label(self, bg="#e6f7ff")
        self.label.pack()

        Label(self, text="Enter Text or Record Voice:", bg="#e6f7ff", font=("Verdana", 12)).pack()

        self.input_text = Text(self, height=4, width=30, font=("Verdana", 12))
        self.input_text.pack()

        Button(self, text="Record Voice", command=self.record_voice, font=("Verdana", 10), bg="#b3e0ff",
               fg="black").pack(pady=5)
        Button(self, text="Convert", command=self.start_conversion, font=("Verdana", 10), bg="#99d6ff",
               fg="black").pack(pady=5)
        Button(self, text="Exit", command=self.quit, font=("Verdana", 10), bg="#80ccff", fg="black").pack(pady=5)

    def record_voice(self):
        def recognize():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.input_text.delete("1.0", "end")  # Clear previous text
                self.input_text.insert("1.0", "Recording...")  # Show status
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio)
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("1.0", text)
                except sr.UnknownValueError:
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("1.0", "Could not understand audio")
                except sr.RequestError:
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("1.0", "Error connecting to speech service")

        threading.Thread(target=recognize, daemon=True).start()

    def start_conversion(self):
        text = self.input_text.get("1.0", "end-1c")
        self.frames = generate_gif(text)
        self.index = 0
        self.show_frames()

    def show_frames(self):
        if self.index < len(self.frames):
            img = ImageTk.PhotoImage(self.frames[self.index])
            self.label.config(image=img)
            self.label.image = img
            self.index += 1
            self.after(2000, self.show_frames)  # Slowing down display duration


if __name__ == "__main__":
    app = SpeechToSignApp()
    app.mainloop()
