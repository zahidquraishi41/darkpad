import tkinter as tk
from tkinter import messagebox, filedialog
import os


class FileDialog:
    '''Features
    > Ctrl+O: Open file dialog
    > Ctrl+S: Save current file (Save As if no file is opened)
    > Ctrl+Shift+S: Open Save As dialog
    > Auto-updates window title
    > Prompts to save changes before closing'''

    def __init__(self, root: tk.Tk, text: tk.Text) -> None:
        self.file = None
        self.encoding = 'utf-8'
        self.root = root
        self.text = text

    def default_bind(self):
        self.root.bind('<Escape>', self._close_app)
        self.root.bind('<Control-w>', self._close_app)
        self.root.protocol('WM_DELETE_WINDOW', self._close_app)
        self.text.bind('<<Modified>>', self._update_title)
        self.text.bind('<Control-o>', self.open_file)
        self.text.bind('<Control-s>', self.save_file)
        self.text.bind('<Control-S>', self.save_as)
        self._update_title()

    def read_file(self, file: str):
        '''Reads and displays the content of a file; opens an untitled window if reading fails.'''
        try:
            self.text.delete(1.0, tk.END)
            self.text.edit_reset()
            with open(file, encoding=self.encoding) as f:
                while True:
                    chunk = f.read(1048576)
                    if not chunk:
                        break
                    self.text.insert(tk.END, chunk)
                    self.text.update()
            self.text.mark_set(tk.INSERT, '1.0')
            self.text.see(tk.INSERT)
            self.file = file
        except Exception as e:
            self.file = None
            self.text.delete(1.0, tk.END)
            self.root.after(100, lambda e=e: messagebox.showerror('Error', e))
        finally:
            self.text.edit_reset()
            self.text.edit_modified(False)

    def open_file(self, event: tk.Event) -> str:
        '''Opens a file dialog to select and read a file'''
        if not self.confirm_save():
            return 'break'

        file = filedialog.askopenfilename(
            title='Open File',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
        )
        if not file:
            return 'break'

        self.read_file(file)
        return 'break'

    def save_file(self, event: tk.Event) -> bool:
        '''Saves the current file if it's opened; prompts to save as if it's untitled.'''
        if not self.text.edit_modified():
            return True
        if not self.file:
            return self.save_as()
        return self._save()

    def save_as(self, event: tk.Event = None) -> bool:
        '''Opens a save-as dialog to specify a file location and saves the file.'''
        file = filedialog.asksaveasfilename(
            title='Save File',
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
        )
        if file:
            self.file = file
            return self._save()
        return False

    def confirm_save(self):
        '''Prompts the user to save changes if the text has been modified.'''
        if not self.text.edit_modified():
            return True
        response = messagebox.askyesnocancel(
            'Confirm',
            'Do you want to save changes?'
        )
        if response:
            if self.file:
                return self._save()
            return self.save_as()
        return response is False

    def _save(self) -> bool:
        '''Saves the current file's content; updates the title on success.'''
        try:
            with open(self.file, 'w', encoding=self.encoding) as f:
                f.write(self.text.get(1.0, tk.END))
                self.text.edit_modified(False)
                self._update_title()
                return True
        except Exception as e:
            messagebox.showerror('Error', e)
            return False

    def _update_title(self, event: tk.Event = None):
        '''Updates the window title based on the file's name or status.'''
        title = os.path.basename(self.file) if self.file else 'Untitled'
        if self.text.edit_modified():
            self.root.title(f'• {title}')
        else:
            self.root.title(title)

    def _close_app(self, event: tk.Event = None):
        '''Confirms saving changes before closing the application.'''
        if self.confirm_save():
            self.root.destroy()
