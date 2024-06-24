from tkinter import *
import ttkbootstrap as ttb
from tkinter import ttk,font,messagebox as mb
import pyperclip as pipe
import os
from tkinter import filedialog as fd
from functools import partial

file_types = [("Text files", "*.txt"), ("All files", "*.*")]
theme_names = ['cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 'yeti', 'pulse', 'united', 'morph', 'journal', 'darkly', 'superhero', 'solar', 'cyborg', 'vapor', 'simplex', 'cerculean']

def fileloc(*a):
    try :
        loc= fd.askopenfilename(title='Open a file',filetypes=file_types)
        return loc
    except FileNotFoundError :
        return None

class MyRootWindow:
    def __init__(self,root):
        
        self.file = None
        self.data = None
        text_font = font.Font(family="Consolas", size=14)
       
        self.root = root
        self.root.state('zoomed')
        width_win = root.winfo_screenwidth()
        height_win = root.winfo_screenheight()
        geometry = f"{width_win}x{height_win}+0+0"
        self.root.geometry(geometry)
        self.root.title('newfile')
        self.style = ttb.Style('cyborg')
        scroll1=ttk.Scrollbar(self.root,orient='horizontal')
        scroll2=ttk.Scrollbar(self.root)
        scroll1.pack(side = BOTTOM, fill = X)
        scroll2.pack(side = RIGHT, fill = Y)

        self.text_field = Text(self.root, wrap='word',undo=True,xscrollcommand = scroll1.set,yscrollcommand = scroll2.set,font=text_font)
        self.text_field.pack(expand=True, fill='both')
        scroll1.config(command=self.text_field.xview)
        scroll2.config(command=self.text_field.yview)

        self.menubar=Menu(self.root)
        self.fmenu=Menu(self.menubar,tearoff=1)
        self.emenu=Menu(self.menubar,tearoff=1)
        self.tmenu=Menu(self.menubar,tearoff=1)
        self.menubar.add_cascade(label="File",menu=self.fmenu)
        self.menubar.add_cascade(label="Edit",menu=self.emenu)
        self.menubar.add_cascade(label="Select Theme",menu=self.tmenu)
        self.fmenu.add_command(label="New         Ctrl+N",command=self.new_window)
        self.fmenu.add_command(label="Open        Ctrl+O",command=self.open_window)
        self.fmenu.add_command(label="Save        Ctrl+S",command=self.savefile)
        self.fmenu.add_command(label="Save as     Ctrl+Shift+S",command=self.saveasfile)
        self.fmenu.add_separator()
        self.fmenu.add_command(label="Close       Alt+f4",command = self.on_cls)
        self.emenu.add_command(label ="Select All\t\t")
        self.emenu.add_command(label ="Cut\t\t")
        self.emenu.add_command(label ="Copy\t\t")
        self.emenu.add_command(label ="Paste\t\t")
        self.emenu.add_command(label ="Undo\t\t")
        self.emenu.add_command(label ="Redo\t\t")
        self.emenu.add_checkbutton(label="Dark mode")
        self.emenu.add_separator()
        self.emenu.add_command(label ="Font\t\t")
        self.selected_theme = StringVar()
        self.selected_theme.set('cyborg')
        for theme in theme_names:
            self.tmenu.add_radiobutton(label=theme,variable=self.selected_theme,value=theme,command=partial(self.set_theme, theme))
        
        self.root.config(menu=self.menubar)
        
        self.pop_menu = Menu(root, tearoff = 0)
        self.pop_menu.add_command(label ="Select All\t\t",command=self.select_all)
        self.pop_menu.add_command(label ="Cut\t\t",command=self.cut_select)
        self.pop_menu.add_command(label ="Copy\t\t",command=self.copy_select)
        self.pop_menu.add_command(label ="Paste\t\t",command=self.paste_select)
        self.pop_menu.add_command(label ="Undo\t\t",command=self.text_field.edit_undo)
        self.pop_menu.add_command(label ="Redo\t\t",command=self.text_field.edit_redo)
      
        self.text_field.bind("<Control-o>",self.open_window)
        self.text_field.bind("<Control-n>",self.new_window)
        self.text_field.bind("<Control-O>",self.open_window)
        self.text_field.bind("<Control-N>",self.new_window)
        self.text_field.bind("<Control-s>",self.savefile)
        self.text_field.bind("<Control-S>",self.savefile)
        self.text_field.bind("<Control--Shift-s>",self.saveasfile)
        self.text_field.bind("<Control-Shift-S>",self.saveasfile)
        self.text_field.bind("<Button-3>", self.do_popup)
        self.root.protocol("WM_DELETE_WINDOW",self.on_cls)
           
    def select_all(self):
        self.text_field.tag_add("sel", "1.0","end") 
        self.text_field.tag_config("sel")
    def cut_select(self):
        if self.text_field.selection_get():
            da=self.text_field.selection_get() 
            self.text_field.delete('sel.first','sel.last')
            pipe.copy(da)
    
    def copy_select(self):
        if self.text_field.selection_get():
            da=self.text_field.selection_get() 
            pipe.copy(da)
    def paste_select(self):
        da=pipe.paste()
        self.text_field.insert(END,da)
    def new_window(self,*a):
        self.child_window = ttb.Toplevel()
        self.window = MyChildWindow(self.child_window)
    def open_window(self,*a):
        if self.file is  None:
            self.loc =  fileloc()
            if self.loc is not None:
                self.file_title = os.path.basename(self.loc)
                self.file = open(self.loc,'r+')
                self.text_field.delete('1.0', END)
                self.data = self.file.read()
                self.text_field.insert('1.0',self.data)
                self.root.title(self.file_title)
        else:
            self.file.close()
            self.loc = self.myFunctions.fileloc()
            if self.loc is not None:
                self.file_title = os.path.basename(self.loc)
                self.file = open(self.loc,'r+')
                self.text_field.delete('1.0', END)
                self.text_field.insert('1.0',self.file.read())
                self.root.title(self.file_title)
            
    def saveasfile(self,*a):
        self.name=fd.asksaveasfile(mode='w',defaultextension=".txt",filetypes=file_types)
        text2save=str(self.text_field.get(0.0,END))
        self.name.write(text2save)
        self.name.close()
    def savefile(self,*a):
        if self.file is not None:
            self.file.seek(0)
            self.file.truncate()
            self.file.write(self.text_field.get("1.0", "end-1c"))
            self.data=self.text_field.get("1.0", "end-1c")
        else:
            self.saveasfile()
    def do_popup(self,event):
        try:
            self.pop_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.pop_menu.grab_release()
    def set_theme(self,val):
        print(val)
        self.style.theme_use(val) 
    def on_cls(self,*a):
        if len(self.text_field.get("1.0", "end-1c")) != 0 :
            if self.data is not None:
                if self.text_field.get("1.0", "end-1c") != self.data :         
                    if mb.askyesno("Quit",'Do you want to save?') :
                        self.savefile()
                        self.file.close()
                        self.root.destroy()
                    else:
                        self.root.destroy()
                else:
                    self.root.destroy()
            else:
                print('here')
                if mb.askyesno("Quit",'Do you want to save?') :
                    self.savefile()
                    self.root.destroy()
                else:
                    self.root.destroy()
        else:
            self.root.destroy()                  
        
class MyChildWindow(MyRootWindow):
    def __init__(self,window):
        text_font = font.Font(family="Consolas", size=14)
        self.file = None 
        self.data = None       
        self.window = window
        self.window.state('zoomed')
        width_win = window.winfo_screenwidth()
        height_win = window.winfo_screenheight()
        geometry = f"{width_win}x{height_win}+0+0"
        self.window.geometry(geometry)
        self.window.title('newfile')
        self.style = ttb.Style('cyborg')
        scroll1=ttk.Scrollbar(self.window,orient='horizontal')
        scroll2=ttk.Scrollbar(self.window)
        scroll1.pack(side = BOTTOM, fill = X)
        scroll2.pack(side = RIGHT, fill = Y)

        self.text_field = Text(self.window, wrap='word',undo=True,xscrollcommand = scroll1.set,yscrollcommand = scroll2.set,font=text_font)
        self.text_field.pack(expand=True, fill='both')
        scroll1.config(command=self.text_field.xview)
        scroll2.config(command=self.text_field.yview)
        
        self.menubar=Menu(self.window)
        self.fmenu=Menu(self.menubar,tearoff=1)
        self.emenu=Menu(self.menubar,tearoff=1)
        self.tmenu=Menu(self.menubar,tearoff=1)
        self.menubar.add_cascade(label="File",menu=self.fmenu)
        self.menubar.add_cascade(label="Edit",menu=self.emenu)
        self.menubar.add_cascade(label="Select Theme",menu=self.tmenu)
        self.fmenu.add_command(label="New         Ctrl+N",command=self.new_window)
        self.fmenu.add_command(label="Open        Ctrl+O",command=self.open_window)
        self.fmenu.add_command(label="Save        Ctrl+S",command=self.savefile)
        self.fmenu.add_command(label="Save as     Ctrl+Shift+S",command=self.saveasfile)
        self.fmenu.add_separator()
        self.fmenu.add_command(label="Close       Alt+f4",command = self.on_cls)
        self.emenu.add_command(label ="Select All\t\t")
        self.emenu.add_command(label ="Cut\t\t")
        self.emenu.add_command(label ="Copy\t\t")
        self.emenu.add_command(label ="Paste\t\t")
        self.emenu.add_command(label ="Undo\t\t")
        self.emenu.add_command(label ="Redo\t\t")
        self.emenu.add_checkbutton(label="Dark mode")
        self.emenu.add_separator()
        self.emenu.add_command(label ="Font\t\t")
        self.selected_theme = StringVar()
        self.selected_theme.set('cyborg')
        for theme in theme_names:
            self.tmenu.add_radiobutton(label=theme,variable=self.selected_theme,value=theme,command=partial(self.set_theme, theme))
        
        self.window.config(menu=self.menubar)
        
        self.pop_menu = Menu(window, tearoff = 0)
        self.pop_menu.add_command(label ="Select All\t\t",command=self.select_all)
        self.pop_menu.add_command(label ="Cut\t\t",command=self.cut_select)
        self.pop_menu.add_command(label ="Copy\t\t",command=self.copy_select)
        self.pop_menu.add_command(label ="Paste\t\t",command=self.paste_select)
        self.pop_menu.add_command(label ="Undo\t\t",command=self.text_field.edit_undo)
        self.pop_menu.add_command(label ="Redo\t\t",command=self.text_field.edit_redo)
        
        self.text_field.bind("<Control-o>",self.open_window)
        self.text_field.bind("<Control-n>",self.new_window)
        self.text_field.bind("<Control-O>",self.open_window)
        self.text_field.bind("<Control-N>",self.new_window)
        self.text_field.bind("<Control-s>",self.savefile)
        self.text_field.bind("<Control-S>",self.savefile)
        self.text_field.bind("<Control--Shift-s>",self.saveasfile)
        self.text_field.bind("<Control-Shift-S>",self.saveasfile)
        self.text_field.bind("<Button-3>", self.do_popup)
        self.window.protocol("WM_DELETE_WINDOW",self.on_cls)
           
    def select_all(self):
        self.text_field.tag_add("sel", "1.0","end") 
        self.text_field.tag_config("sel")
    def cut_select(self):
        if self.text_field.selection_get():
            da=self.text_field.selection_get() 
            self.text_field.delete('sel.first','sel.last')
            pipe.copy(da)
    
    def copy_select(self):
        if self.text_field.selection_get():
            da=self.text_field.selection_get() 
            pipe.copy(da)
    def paste_select(self):
        da=pipe.paste()
        self.text_field.insert(END,da)
    def new_window(self):
        self.child_window = ttb.Toplevel()
        self.window = MyChildWindow(self.child_window)
    def open_window(self):
        self.loc = fileloc()
        self.file_title = os.path.basename(self.loc)
        self.file = open(self.loc,'r+')
        self.text_field.delete('1.0', END)
        self.data = self.file.read()
        self.text_field.insert('1.0',self.data)
        self.window.title(self.file_title)
    def saveasfile(self):
        self.name=fd.asksaveasfile(mode='w',defaultextension=".txt",filetypes=file_types)
        text2save=str(self.text_field.get(0.0,END))
        self.name.write(text2save)
        self.name.close()
    def savefile(self):
        if self.file is not None:
            self.file.seek(0)
            self.file.truncate()
            self.file.write(self.text_field.get("1.0", "end-1c"))
            self.data=self.text_field.get("1.0", "end-1c")
        else:
            self.saveasfile()
    def do_popup(self,event):
        try:
            self.pop_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.pop_menu.grab_release()
    def set_theme(self,val):
        print(val)
        self.style.theme_use(val)
    
    def on_cls(self,*a):
        if len(self.text_field.get("1.0", "end-1c")) != 0 :
            if self.data is not None:
                if self.text_field.get("1.0", "end-1c")!=self.data :         
                    if mb.askyesno("Quit",'Do you want to save?') :
                        self.savefile()
                        self.window.destroy()
                    else:
                        self.window.destroy()
                else:
                    self.window.destroy()
            else:
                if mb.askyesno("Quit",'Do you want to save?') :
                    self.savefile()
                    self.window.destroy()
                else:
                    self.window.destroy()
        else:
            self.window.destroy()

root_window = ttb.Window(themename="cyborg")
root = MyRootWindow(root_window)

mainloop()