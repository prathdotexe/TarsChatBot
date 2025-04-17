import tkinter as tk
from tkinter import scrolledtext, ttk
import google.generativeai as genai
import time
import threading
import pyttsx3
import re

# === CONFIGURE GEMINI API ===
genai.configure(api_key="AIzaSyAHfApekgjUuey-GD18OH2wy0XBClLxY1c")  # Replace with your actual key
model = genai.GenerativeModel("models/gemini-2.0-flash")

# === INITIATE CHAT MEMORY ===
chat_history = ""

# === INITIATE VOICE ENGINE ===
engine = pyttsx3.init()
engine.setProperty('rate', 155)
engine.setProperty('volume', 1.0)

# Choose a voice that sounds robotic
voices = engine.getProperty('voices')
for v in voices:
    if "Zira" in v.name or "David" in v.name or "Microsoft" in v.id:
        engine.setProperty('voice', v.id)
        break

# === FUNCTION TO SPEAK CLEAN TEXT ===
def speak(text):
    clean = re.sub(r"[^A-Za-z0-9 ,.'?!]", "", text)
    engine.say(clean)
    engine.runAndWait()

# === FUNCTION TO SIMULATE WORD BY WORD OUTPUT + SPEECH ===
def type_response(response_text):
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "TARS: ")
    chat_window.see(tk.END)

    def speak_thread():
        speak(response_text)

    threading.Thread(target=speak_thread).start()

    for word in response_text.split():
        chat_window.insert(tk.END, word + " ")
        chat_window.see(tk.END)
        chat_window.update()
        time.sleep(0.05)

    chat_window.insert(tk.END, "\n\n")
    chat_window.config(state=tk.DISABLED)

# === HANDLE CHAT FUNCTIONALITY ===
def send_message():
    global chat_history
    user_input = entry.get()
    if not user_input.strip():
        return

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_input + "\n")
    chat_window.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

    honesty_level = honesty_slider.get()
    humor_level = humor_slider.get()

    preprompt = (
        f"You are TARS from Interstellar, an intelligent AI robot. "
        f"Respond in a clear and witty manner, with an honesty level of {honesty_level}% "
        f"and a humor level of {humor_level}%. Keep answers helpful, with robotic tone but human-like clarity.\n"
    )

    full_prompt = preprompt + chat_history + "\nHuman: " + user_input + "\nTARS:"

    def fetch_response():
        global chat_history
        try:
            response = model.generate_content(full_prompt)
            reply = response.text.strip()
            chat_history += f"\nHuman: {user_input}\nTARS: {reply}"
        except Exception as e:
            reply = f"Error: {str(e)}"
        type_response(reply)

    threading.Thread(target=fetch_response).start()

# === CREATE GUI ===
root = tk.Tk()
root.title("TARS - Advanced Interstellar Chatbot")
root.geometry("700x600")
root.configure(bg="#0d0d0d")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#111", fg="#00ffcc", font=("Courier", 11))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_window.config(state=tk.DISABLED)

entry_frame = tk.Frame(root, bg="#0d0d0d")
entry_frame.pack(fill=tk.X, padx=10, pady=5)

entry = tk.Entry(entry_frame, font=("Courier", 12), bg="#222", fg="#00ffcc", insertbackground="#00ffcc")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(entry_frame, text="Send", command=send_message, bg="#00ffcc", fg="#000", font=("Courier", 10, "bold"))
send_button.pack(side=tk.RIGHT)

slider_frame = tk.Frame(root, bg="#0d0d0d")
slider_frame.pack(padx=10, pady=10, fill=tk.X)

honesty_label = tk.Label(slider_frame, text="Honesty %", fg="#00ffcc", bg="#0d0d0d", font=("Courier", 10))
honesty_label.pack(side=tk.LEFT)
honesty_slider = ttk.Scale(slider_frame, from_=0, to=100, orient="horizontal")
honesty_slider.set(90)
honesty_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

humor_label = tk.Label(slider_frame, text="Humor %", fg="#00ffcc", bg="#0d0d0d", font=("Courier", 10))
humor_label.pack(side=tk.LEFT)
humor_slider = ttk.Scale(slider_frame, from_=0, to=100, orient="horizontal")
humor_slider.set(30)
humor_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

# === START GUI ===
root.mainloop()