from functools import partial
import tkinter as tk


class Text(tk.Text):
    '''Features
    > Built-in vertical and horizontal auto-hide scrollbars
    > More frequent undo registration'''

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.after_id = None
        self.bind('<KeyRelease>', self.on_key_release)

        h_scroll = Scrollbar(
            self.master,
            orient='horizontal',
            command=self.xview
        )
        v_scroll = Scrollbar(
            self.master,
            orient='vertical',
            command=self.yview
        )
        self.config(
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set
        )

        self.grid(row=0, column=0, sticky='nsew')
        h_scroll.grid(row=1, column=0, sticky='ew')
        v_scroll.grid(row=0, column=1, sticky='ns')

    def on_key_release(self, event):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.after_id = self.after(500, self.edit_separator)


class Scrollbar(tk.Scrollbar):
    '''Features
    > Auto-hide scrollbar when there is nothing to scroll'''

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.gm_forget()
        else:
            self.gm_add()
        super().set(lo, hi)

    def grid(self, **kwargs):
        self.gm_add = partial(super().grid, **kwargs)
        self.gm_forget = super().grid_forget

    def pack(self, **kwargs):
        self.gm_add = partial(super().pack, **kwargs)
        self.gm_forget = super().pack_forget

    def place(self, **kwargs):
        self.gm_add = partial(super().place, **kwargs)
        self.gm_forget = super().place_forget
