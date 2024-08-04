import tkinter as tk
from tkinter import font


def bind_all(text: tk.Text):
    bind = text.bind
    bind('<Control-+>', increase_font_size)
    bind('<Control-=>', increase_font_size)
    bind('<Control-minus>', decrease_font_size)
    bind('<Control-BackSpace>', delete_word_left)
    bind('<Control-Delete>', delete_word_right)
    bind('<Shift-Return>', insert_newline)


def increase_font_size(event: tk.Event):
    w = event.widget
    active_font = font.Font(font=w['font'])
    if active_font.actual('size') < 72:
        active_font.config(size=active_font.actual('size') + 1)
    w.config(font=active_font)


def decrease_font_size(event: tk.Event):
    w = event.widget
    curr_font = font.Font(font=w['font'])
    if curr_font.actual('size') > 8:
        curr_font.config(size=curr_font.actual('size') - 1)
    w.config(font=curr_font)


def delete_word_left(event):
    w = event.widget
    insert_col = w.index('insert').split('.')[1]
    insert_col = int(insert_col)

    i = 1
    while i < insert_col and w.get(f'insert-{i}c') == ' ':
        i += 1
    while i < insert_col and w.get(f'insert-{i+1}c') != ' ':
        i += 1

    w.delete(f'insert-{i}c', 'insert')
    return 'break'


def delete_word_right(event):
    w = event.widget
    insert_col = w.index('insert').split('.')[1]
    line_end_col = w.index('insert lineend').split('.')[1]
    line_end_col = int(line_end_col) - int(insert_col)

    i = 1
    while i < line_end_col and w.get(f'insert+{i}c') == ' ':
        i += 1
    while i < line_end_col and w.get(f'insert+{i-1}c') != ' ':
        i += 1

    w.delete(f'insert', f'insert+{i}c')
    return 'break'


def insert_newline(event: tk.Event):
    w = event.widget
    line_end = w.index(f'insert lineend')
    w.insert(line_end, '\n')
    w.mark_set(tk.INSERT, f'{line_end}+1c')
    return 'break'
