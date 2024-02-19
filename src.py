import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import *
import time
import os
import ctypes
import asyncio
import websockets
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

file_list = []

if not os.path.exists("launch.cfg"):
    tk.Tk().withdraw()
    messagebox.showinfo("ERROR", "You must place this application inside the Ro-Exec Folder!")
    sys.exit()


dir_path = os.path.dirname(os.path.abspath(sys.executable))
TokenHolder = os.path.join(dir_path, "launch.cfg")
if os.path.isfile(TokenHolder):
    with open(TokenHolder, 'r') as file:
        token = file.read()
        token = token.split("|RO-EXEC")[0]
        url = f"wss://loader.live/?login_token=%22{token}%22"


if not os.path.exists("scripts"):
    os.makedirs("scripts")

websocket = None

async def connect():
    global websocket
    websocket = await websockets.connect(url)

async def test():
    await connect()
    msg = "<SCRIPT>" + textbox.get("1.0", "end-1c")
    await websocket.send(msg)

async def ExeWait():
    await test()

def ExecuteFunction():
    loop = asyncio.get_event_loop()
    task = loop.create_task(ExeWait())
    loop.run_until_complete(task)


app = CTk()
app.geometry("700x400")
app.title("Rolox UI (Krampus/Ro-Exec)")
set_default_color_theme("dark-blue")

def ExeHandler():
    script = textbox.get("1.0", "end-1c")
    ExecuteFunction()

def ClearHandler():
    textbox.delete("1.0", "end")

def AttachHandler():
    script_dir = os.path.dirname(os.path.abspath(sys.executable))
    exe_files = [os.path.join(script_dir, filename) for filename in os.listdir(script_dir) if filename.endswith('.exe') and filename not in ["RoExec-AutoLauncher.exe", "KrampusY.exe"]]
    exe = exe_files[0] if exe_files else None

    time.sleep(1)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, None, None, 1)


def ScriptHandler(option):
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    file_path = os.path.join(exe_dir, 'scripts', option)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            script = file.read()
    textbox.delete("1.0", "end")
    textbox.insert("1.0", script)

def SaveHandler():
    script = textbox.get("1.0", "end-1c")
    dialog = ctk.CTkInputDialog(text="Enter Script Name:", title="Script Name Prompt")
    filename = dialog.get_input()
    if not filename == None:
        file_path = os.path.join("scripts", f'{filename}.txt')
        with open(file_path, 'w') as file:
            file.write(script)

def DeleteHandler():
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    option = SelectScript.get()
    file_path = os.path.join(exe_dir, 'scripts', option)
    os.remove(file_path)
    textbox.delete("1.0", "end")

textbox = CTkTextbox(master=app, width=640, height=330, scrollbar_button_color="#FFCC70", corner_radius=16, border_color="#FFCC70", border_width=2)
textbox.place(relx=0.5, rely=0.45, anchor="center")

SelectScript = CTkComboBox(master=app, command=ScriptHandler, values=file_list, fg_color="#FFCC70", button_color="#ffa600", border_color="#ffa600", corner_radius=8, text_color="#40341e", font=("Lexend Medium", 12), hover=False, dropdown_fg_color="#FFCC70", dropdown_text_color="#40341e", dropdown_hover_color="white", dropdown_font=("Lexend Medium", 12))
SelectScript.place(relx=0.15, rely=0.92, anchor ="center")

ExecuteButton = CTkButton(master = app, text="Execute", corner_radius=12, fg_color="#FFCC70", text_color="#40341e", font=("Trebuchet MS", 15), command=ExeHandler, width=80, hover_color="#ffa600")
ExecuteButton.place(relx=0.88, rely=0.92, anchor ="center")

ClearButton = CTkButton(master = app, text="Clear", corner_radius=12, fg_color="#FFCC70", text_color="#40341e", font=("Trebuchet MS", 15), command=ClearHandler, width=80, hover_color="#ffa600")
ClearButton.place(relx=0.76, rely=0.92, anchor ="center")

AttachButton = CTkButton(master = app, text="Attach", corner_radius=12, fg_color="#FFCC70", text_color="#40341e", font=("Trebuchet MS", 15), command=AttachHandler, width=80, hover_color="#ffa600")
AttachButton.place(relx=0.64, rely=0.92, anchor ="center")

SaveButton = CTkButton(master = app, text="Save", corner_radius=12, fg_color="#FFCC70", text_color="#40341e", font=("Trebuchet MS", 15), command=SaveHandler, width=80, hover_color="#ffa600")
SaveButton.place(relx=0.52, rely=0.92, anchor ="center")

DeleteButton = CTkButton(master = app, text="Delete", corner_radius=12, fg_color="#FFCC70", text_color="#40341e", font=("Trebuchet MS", 15), command=DeleteHandler, width=80, hover_color="#ffa600")
DeleteButton.place(relx=0.40, rely=0.92, anchor ="center")

def update_file_list():
    global file_list
    oldfilelist = file_list
    file_list = [f for f in os.listdir('scripts') if f.endswith(('.txt', '.lua'))]
    if not oldfilelist == file_list:
        SelectScript.configure(values=file_list)
    if len(file_list) == 0:
        SelectScript.set("No Scripts")
    else:
        SelectScript.set("Select Script...")

update_file_list()

class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        update_file_list()

observer = Observer()
observer.schedule(FileChangeHandler(), 'scripts', recursive=True)
observer.start()

app.mainloop()
