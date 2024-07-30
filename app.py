import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import wav_lsb
import wav_parity_coding  # Import the new Parity Coding module

txt_file_path = None

def on_drop(event):
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path) and file_path.endswith(('.wav', '.aiff', '.pcm')):
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
    else:
        messagebox.showerror("Błąd", "Proszę upuścić plik .wav, .aiff lub .pcm")

def encode():
    file_path = file_entry.get()
    secret_message = message_entry.get()
    method = method_var.get()
    global txt_file_path

    if not file_path or (not secret_message and not txt_file_path):
        messagebox.showerror("Błąd", "Proszę podać plik oraz wiadomość lub plik tekstowy do zakodowania")
        return

    if txt_file_path:
        with open(txt_file_path, 'r') as file:
            secret_message = file.read()
        txt_file_path = None  # Reset the txt_file_path after use

    try:
        if method == 'LSB':
            output_file = wav_lsb.encode_audio(file_path, secret_message)
        elif method == 'Parity Coding':
            output_file = wav_parity_coding.parity_encode(file_path, secret_message)
        else:
            raise ValueError("Unsupported encoding method")
        messagebox.showinfo("Sukces", f"Wiadomość zakodowana w pliku {output_file}")
    except ValueError as e:
        messagebox.showerror("Błąd", str(e))

def decode():
    file_path = file_entry.get()
    method = method_var.get()
    if not file_path:
        messagebox.showerror("Błąd", "Proszę podać plik do odkodowania")
        return

    if method == 'LSB':
        decoded_message = wav_lsb.decode_audio(file_path)
    elif method == 'Parity Coding':
        decoded_message = wav_parity_coding.parity_decode(file_path)
    else:
        raise ValueError("Unsupported decoding method")
    messagebox.showinfo("Odkodowana wiadomość", decoded_message)

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.aiff *.pcm")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def browse_txt_files():
    global txt_file_path
    txt_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if txt_file_path:
        txt_file_entry.delete(0, tk.END)
        txt_file_entry.insert(0, txt_file_path)

root = TkinterDnD.Tk()
root.title("Audio Steganography")

root.geometry("700x500")
root.config(bg="#f0f0f0")

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(pady=20)

file_frame = tk.Frame(main_frame, bg="#f0f0f0")
file_frame.pack(pady=10)

file_label = tk.Label(file_frame, text="Plik Audio (WAV, AIFF, PCM):", bg="#f0f0f0", font=('Arial', 12))
file_label.grid(row=0, column=0, padx=5, pady=5)

file_entry = tk.Entry(file_frame, width=50, font=('Arial', 12))
file_entry.grid(row=1, column=0, padx=5, pady=5)

browse_button = tk.Button(file_frame, text="Przeglądaj", command=browse_files, font=('Arial', 12))
browse_button.grid(row=2, column=0, padx=5, pady=5)

message_frame = tk.Frame(main_frame, bg="#f0f0f0")
message_frame.pack(pady=10)

message_label = tk.Label(message_frame, text="Wiadomość:", bg="#f0f0f0", font=('Arial', 12))
message_label.grid(row=0, column=0, padx=5, pady=5)

message_entry = tk.Entry(message_frame, width=50, font=('Arial', 12))
message_entry.grid(row=0, column=1, padx=5, pady=5)

txt_file_frame = tk.Frame(main_frame, bg="#f0f0f0")
txt_file_frame.pack(pady=10)

txt_file_label = tk.Label(txt_file_frame, text="Plik tekstowy:", bg="#f0f0f0", font=('Arial', 12))
txt_file_label.grid(row=0, column=0, padx=5, pady=5)

txt_file_entry = tk.Entry(txt_file_frame, width=50, font=('Arial', 12))
txt_file_entry.grid(row=0, column=1, padx=5, pady=5)

browse_txt_button = tk.Button(txt_file_frame, text="Przeglądaj", command=browse_txt_files, font=('Arial', 12))
browse_txt_button.grid(row=1, column=1, padx=5, pady=5)

method_frame = tk.Frame(main_frame, bg="#f0f0f0")
method_frame.pack(pady=10)

method_label = tk.Label(method_frame, text="Metoda:", bg="#f0f0f0", font=('Arial', 12))
method_label.grid(row=0, column=0, padx=5, pady=5)

method_var = tk.StringVar(value="LSB")
method_menu = ttk.Combobox(method_frame, textvariable=method_var, values=["LSB", "Parity Coding"], font=('Arial', 12))
method_menu.grid(row=0, column=1, padx=5, pady=5)

button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(pady=10)

encode_button = tk.Button(button_frame, text="Zakoduj", command=encode, font=('Arial', 12))
encode_button.grid(row=0, column=0, padx=20, pady=10)

decode_button = tk.Button(button_frame, text="Odkoduj", command=decode, font=('Arial', 12))
decode_button.grid(row=0, column=1, padx=20, pady=10)

file_entry.drop_target_register(DND_FILES)
file_entry.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
