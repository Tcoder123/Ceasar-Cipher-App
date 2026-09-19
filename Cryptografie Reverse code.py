import customtkinter as ctk
import random

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("light")
mode = "light"

def dark_light_mode():
    global mode
    if mode== "light":
        ctk.set_appearance_mode("dark")
        mode = "dark"
        mode_switch_button.configure(text="Light mode")
    else:
        ctk.set_appearance_mode("light")
        mode = "light"
        mode_switch_button.configure(text= "Dark mode")

root = ctk.CTk()
root.title("En- and decryptor of Ceasar cipher")
root.geometry("800x600")

main_frame = ctk.CTkFrame(root)
main_frame.pack(fill= "both", expand=1)

my_canvas = ctk.CTkCanvas(main_frame)
my_canvas.pack(side="left", fill="both", expand=1)

scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=my_canvas.yview, cursor="dot")
scrollbar.pack(side="right", fill= "y")

my_canvas.configure(yscrollcommand=scrollbar.set)
def on_frame_configure(event):
    bbox = my_canvas.bbox("all")
    if bbox:
        my_canvas.configure(scrollregion=bbox)

second_frame = ctk.CTkFrame(my_canvas)

window_id = my_canvas.create_window((0,0), window=second_frame, anchor="nw")

second_frame.bind("<Configure>", on_frame_configure)

def on_canvas_configure(event):
    my_canvas.itemconfig(window_id, width=event.width)

my_canvas.bind("<Configure>", on_canvas_configure)

mode_switch_button = ctk.CTkButton(second_frame, text= "Dark mode", command=dark_light_mode)
mode_switch_button.pack(pady= 5)

cf = ctk.CTkFont(size=20)
message_label = ctk.CTkLabel(second_frame, text="Message:", pady=10, font=cf)
message_label.pack()
message_field = ctk.CTkTextbox(second_frame, width=500, height= 250, font=cf)
message_field.pack(expand=True)

def clear_text():
    message_field.delete("1.0", "end")

clear_text_button = ctk.CTkButton(second_frame, text="Clear text", command= clear_text)
clear_text_button.pack(pady=10)

key_label = ctk.CTkLabel(second_frame, text="Key:", pady=10, font=cf)
key_label.pack()
key_field = ctk.CTkEntry(second_frame, font=cf)
key_field.pack()

def key_generate():
    key = random.randint(1, 25)
    key_field.delete(0, "end")
    key_field.insert(0, key)

key_generate_button = ctk.CTkButton(second_frame, text="Generate key", command=key_generate)
key_generate_button.pack(pady= 5)

mode_label = ctk.CTkLabel(second_frame, text="Choose the mode:", pady=10, font = cf)
mode_label.pack()
mode_button_Var = ctk.IntVar()
decrypt_mode = ctk.CTkRadioButton(second_frame, text="Decrypt", value=0, variable=mode_button_Var)
encrypt_mode = ctk.CTkRadioButton(second_frame, variable=mode_button_Var, value=1, text="Encrypt")
brute_force_mode = ctk.CTkRadioButton(second_frame, variable= mode_button_Var, value= 2, text="Brute Force")
decrypt_mode.pack(pady= 5)
encrypt_mode.pack(pady= 5)
brute_force_mode.pack(pady=5)


def encrypt(mess, key, mode):
    message = mess.upper()
    Symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    translated = ""

    for symbol in message:
        if symbol in Symbols:
            symbolIndex = Symbols.find(symbol)
            if mode == 1:
                translatedIndex = symbolIndex + key
            elif mode == 0:
                translatedIndex = symbolIndex - key
            if translatedIndex >= len(Symbols):
                translatedIndex = translatedIndex -len(Symbols)
            elif translatedIndex < 0:
                translatedIndex = translatedIndex + len(Symbols)
            translated = translated + Symbols[translatedIndex]
        else: 
            translated = translated + symbol

    result_field.delete("1.0", "end")

    endmessage = translated.replace(" ", "")
    result_field.insert("1.0", endmessage)
    
def bruteforce(mess):
    message = mess.upper()
    Symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result_field.delete("1.0", "end")
    line = -1
    place = 0.9
    for key in range(len(Symbols)):
        translated =""
        for symbol in message:
            if symbol in Symbols:
                symbolIndex = Symbols.find(symbol)
                translatedIndex = symbolIndex - key
                if translatedIndex < 0:
                    translatedIndex = translatedIndex + len(Symbols)
                translated = translated + Symbols[translatedIndex]
            else:
                translated = translated + symbol
        line = line + 1
        result_field.insert("1.0", f"{line}. {translated} \n")



def get_userinput():
    mess = message_field.get("1.0", "end-1c")
    key = key_field.get()
    mode = mode_button_Var.get()
    if mode == 2:
        bruteforce(mess)
    else:
        key = int(key)
        encrypt(mess, key, mode)

submit_button = ctk.CTkButton(second_frame, text="Submit", command= get_userinput)
submit_button.pack(pady = 5)

result_label = ctk.CTkLabel(second_frame, text="Result:", pady=30, font= cf)
result_label.pack()
result_field = ctk.CTkTextbox(second_frame, width=500, height= 250, font=cf)
result_field.pack(expand=True)

def delete_results():
    result_field.delete("1.0", "end")

button_clear_results= ctk.CTkButton(second_frame, text="Clear results", command=delete_results)
button_clear_results.pack(pady=10)
root.mainloop()