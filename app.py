import tkinter as tk
from tkinter import font
from custom_widgets import Text
import keybindings
from file_dialog import FileDialog
import sys

# Define window size
window_width = 800
window_height = 600

# Create the main application window
root = tk.Tk()
x = (root.winfo_screenwidth() - window_width) // 2
y = (root.winfo_screenheight() - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# Create the Dark Text widget
editor = Text(root)
editor.config(
    font=font.Font(family='Fira Code', size=16),
    wrap='none', undo=True,
    bg='#2e2e2e', fg='#ffffff',
    selectbackground='#4f4f4f',
    padx=8, pady=8,
    insertbackground='grey',
    insertontime=0, insertofftime=0
)
editor.grid(row=0, column=0, sticky='nsew')
editor.focus_set()


# Resolving blurred tkinter text + scaling on Windows 10 high DPI displays
if sys.platform.startswith('win'):
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

# Adding keybindings
keybindings.bind_all(editor)
fd = FileDialog(root, editor)
fd.default_bind()

# Start the Tkinter main event loop
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        fd.read_file(file)
    root.mainloop()
