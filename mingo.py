# MINGO BY REMTII 2020

import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import os

ams = tk.Tk()
ams.title('Mingo')
ams.geometry('1200x800')

main_menu = tk.Menu()
file = tk.Menu(main_menu, tearoff=False)
edit = tk.Menu(main_menu, tearoff=False)
view = tk.Menu(main_menu, tearoff=False)
help = tk.Menu(main_menu, tearoff=False)

# Cascade
main_menu.add_cascade(label='File', menu=file)
main_menu.add_cascade(label='Edit', menu=edit)
main_menu.add_cascade(label='View', menu=view)
main_menu.add_cascade(label='Help', menu=help)

#### Toolbar ####

tool_bar = ttk.Label(ams)
tool_bar.pack(side=tk.TOP, fill=tk.X)

# font box
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar, width=30, textvariable=font_family, state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0, column=0, padx=5)

# size box
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar, width=14, textvariable=size_var, state='readonly')
font_size['values'] = tuple(range(8, 80, 2))
font_size.current(4)
font_size.grid(row=0, column=1, padx=5)

# font color button
#color_icon = tk.PhotoImage(file='color.png')
font_color_btn = ttk.Button(tool_bar, text='Color')
font_color_btn.grid(row=0, column=5, padx=5)

#### ` Toolbar ####

#### Text Editor ####

text_editor = tk.Text(ams)
text_editor.config(wrap='word', relief=tk.FLAT)

scroll_bar = tk.Scrollbar(ams)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

# font family and font size functionality
current_font_family = 'Courier New'
current_font_size = 12

def change_font(event=None):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.configure(font=(current_font_family, current_font_size))
    
def change_fontsize(event=None):
    global current_font_size
    current_font_size = size_var.get()
    text_editor.configure(font=(current_font_family, current_font_size))
    
font_box.bind("<<ComboboxSelected>>", change_font)
font_size.bind("<<ComboboxSelected>>", change_fontsize)

# font color functionality
def change_font_color():
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])
    
font_color_btn.configure(command=change_font_color)

text_editor.configure(font=('Arial', 12))

#### ` Text Editor ####


#### Status Bar ####

status_bar = ttk.Label(ams, text='Status Bar')
status_bar.pack(side=tk.BOTTOM)

text_changed = False
def changed(event=None):
    global text_changed
    if text_editor.edit_modified():
        text_changed = True
        words = len(text_editor.get(1.0, 'end-1c').split())
        characters = len(text_editor.get(1.0, 'end-1c').replace(' ', ''))
        status_bar.config(text=f'Characters : {characters} Words : {words}')
    text_editor.edit_modified(False)
    
text_editor.bind('<<Modified>>', changed)

#### ` Status Bar ####


#### Main Menu Functions ####

# variable
url = ''
# new_file functions
def new_file(event=None):
    global url
    url = ''
    text_editor.delete(1.0, tk.END)
# file commands
file.add_command(label='New', compound=tk.LEFT, accelerator='Ctrl+N', command=new_file)

# open_file functions
def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '*.txt'), ('All Files', '*.*')))
    try:
        with open(url, 'r') as fr:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    ams.title(os.path.basename(url))
file.add_command(label='Open', compound=tk.LEFT, accelerator='Ctrl+O', command=open_file)

# save_file functions
def save_file(event=None):
    global url
    try:
        if url:
            content = str(text_editor.get(1.0, tk.END))
            with open(url, 'w', encoding='utf-8') as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All Files', '*.*')))
            content2 = text_editor.get(1.0, tk.END)
            url.write(content2)
            url.close()
    except:
        return
file.add_command(label='Save', compound=tk.LEFT, accelerator='Ctrl+S', command=save_file)

# save_as_file functions
def save_as_file(event=None):
    global url
    try:
        content = text_editor.get(1.0, tk.END)
        url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All Files', '*.*')))
        url.write(content)
        url.close()
    except:
        return
file.add_command(label='Save As', compound=tk.LEFT, accelerator='Ctrl+Alt+S', command=save_as_file)

# exit functions
def quit(event=None):
    global url, text_changed
    try:
        if text_changed:
            mbox = messagebox.asktesnocancel('Warning', 'Do you want to save the file ????')
            if mbox is True:
                if url:
                    content = text_editor.get(1.0, tk.END)
                    with open(url, 'w', encoding='utf-8') as fw:
                        fw.write(content)
                        ams.destroy()
                else:
                    content2 = str(texteditor.get(1.0, tk.END))
                    url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All Files', '*.*')))
                    url.write(content2)
                    url.close()
                    ams.destroy()
            elif mbox is False:
                ams.destroy()
        else:
            ams.destroy()
    except:
        return
file.add_command(label='Quit', compound=tk.LEFT, accelerator='Ctrl+Q', command=quit)

# def run(event=None):
#   os.system("python ams")
# file.add_command(label='Run', compound=tk.LEFT, accelerator='Ctrl+R', command=run)

# edit commands
edit.add_command(label='Copy', compound=tk.LEFT, accelerator='Ctrl+C', command=lambda:text_editor.event_generate("<Control c>"))
edit.add_command(label='Paste', compound=tk.LEFT, accelerator='Ctrl+V', command=lambda:text_editor.event_generate("<Control v>"))
edit.add_command(label='Cut', compound=tk.LEFT, accelerator='Ctrl+X', command=lambda:text_editor.event_generate("<Control x>"))

# view commands
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar = False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP, fill=tk.X)
        text_editor.pack(fill=tk.BOTH, expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar = True

def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar = False
    else:
        status_bar.pack(side=tk.BOTTOM)
        show_statusbar = True

view.add_checkbutton(label="Tool Bar", onvalue=True, offvalue=0, variable=show_toolbar, compound=tk.LEFT, command=hide_toolbar)
view.add_checkbutton(label="Status Bar", onvalue=1, offvalue=False, variable=show_statusbar, compound=tk.LEFT, command=hide_statusbar)

# about
def about(event=None):
	aboutw = tk.Toplevel()
	aboutw.geometry('500x250+500+200')
	aboutw.title('About')
	aboutw.resizable(0, 0)

help.add_command(label='About', compound=tk.LEFT, command=about)

#### ` Main Menu Functions ####

ams.config(menu=main_menu)

#### Key Shortcuts ####

ams.bind("<Control-n>", new_file)
ams.bind("<Control-o>", open_file)
ams.bind("<Control-s>", save_file)
ams.bind("<Control-Alt-s>", save_as_file)
#ams.bind("<Control-q>", exit)

#### ` Key Shortcuts ####

ams.mainloop()