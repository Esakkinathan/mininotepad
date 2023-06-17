from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pyperclip as pipe
import os
root=Tk()
#root.attributes("-fullscreen", True)
root.state('zoomed')
style=ttk.Style()
#style.theme_use('default')
#style.configure("Vertical.TScrollbar", background="black", arrowcolor="red")

# file name with extension
def on_cls():
    try:        
        textdata=t.get("1.0", "end-1c") 
    except:
        pass
        #if(messagebox.askokcancel("mininotepad","Do you want to save?")):
def thememode():
    if cbval==0:
        pass
    else:
        pass
def select_all():
    t.tag_add("sel", "1.0","end") 
    t.tag_config("sel",background="#0000FF",foreground="white")

def cut_select():
    if t.selection_get():
        da=t.selection_get() 
        t.delete('sel.first','sel.last')
        pipe.copy(da)
def copy_select():
    if t.selection_get():
        da=t.selection_get() 
        pipe.copy(da)
def paste_select():
    da=pipe.paste()
    t.insert(END,da)
global new_val
new_val=1


def newfile(*a):
    nw=Toplevel()
    nw.state('zoomed')
    cbval=IntVar(value=0)

    menubar=Menu(nw, background='blue', fg='white')
    fmenu=Menu(menubar,tearoff=1)
    emenu=Menu(menubar,tearoff=1)
    menubar.add_cascade(label="File",menu=fmenu)
    menubar.add_cascade(label="Edit",menu=emenu)
    fmenu.add_command(label="New         Ctrl+N",command=newfile)
    fmenu.add_command(label="Open        Ctrl+O",command=openfile)
    fmenu.add_command(label="Save        Ctrl+S",command=savefile)
    fmenu.add_command(label="Save as     Ctrl+Shift+S",command=saveasfile)
    fmenu.add_separator()
    fmenu.add_command(label="Close       Alt+f4",command=root.destroy)

    #menubar.add_cascade(checkb,command=thememode)
    nw.config(menu=menubar)



    scroll1=ttk.Scrollbar(nw,orient='horizontal')
    scroll2=ttk.Scrollbar(nw)
    scroll1.pack(side = BOTTOM, fill = X)
    scroll2.pack(side = RIGHT, fill = Y)
    t=Text(nw,width=700,height=500,xscrollcommand = scroll1.set,yscrollcommand = scroll2.set,undo=True)
    t.pack(side=LEFT)
    scroll1.config(command=t.xview)
    scroll2.config(command=t.yview)

    emenu.add_command(label ="Select All\t\t",command=select_all)
    emenu.add_command(label ="Cut\t\t",command=cut_select)
    emenu.add_command(label ="Copy\t\t",command=copy_select)
    emenu.add_command(label ="Paste\t\t",command=paste_select)
    emenu.add_command(label ="Undo\t\t",command=t.edit_undo)
    emenu.add_command(label ="Redo\t\t",command=t.edit_redo)
    emenu.add_checkbutton(label="Dark mode",variable=cbval,command=switch)
    emenu.add_separator()
    emenu.add_command(label ="Rename\t\t")
    """m = Menu(root, tearoff = 0)
    m.add_command(label ="Select All\t\t",command=select_all)
    m.add_command(label ="Cut\t\t",command=cut_select)
    m.add_command(label ="Copy\t\t",command=copy_select)
    m.add_command(label ="Paste\t\t",command=paste_select)
    m.add_command(label ="Undo\t\t",command=t.edit_undo)
    m.add_command(label ="Redo\t\t",command=t.edit_redo)
    m.add_separator()
    m.add_command(label ="Rename\t\t")
    
    def do_popup(event):
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()
    """
    #root.protocol("WM_DELETE_WINDOW",on_cls) 
    t.bind("<Control-o>",openfile)
    t.bind("<Control-n>",newfile)
    t.bind("<Control-O>",openfile)
    t.bind("<Control-N>",newfile)
    t.bind("<Control-s>",savefile)
    t.bind("<Control-S>",savefile)
    t.bind("<Control--Shift-s>",saveasfile)
    t.bind("<Control-Shift-S>",saveasfile)
    t.bind("<Control-f>",search)
    t.bind("<Button-3>", do_popup)
        
    
    
    
def search(a):
    new=Toplevel()
    new.geometry('300x300')
    v=StringVar()
    E=Entry(new,textvariable=v)
    E.pack()
    b=Button(new,text='click',command=lambda:searchval(v.get()))
    b.pack(side=BOTTOM)
    def searchval(i):
        dat=t.get("1.0", "end-1c") 
        if i in dat:
            print("Found")
            print(dat.index(i))
        else:
            print("Not Found") 
def fileloc():
    global loc
    filetypes = [("Text Files", "*.txt"),('All files', '*.*')]
    loc= fd.askopenfilename(title='Open a file',filetypes=filetypes)
    #print(d)
    return loc
def openfile(*a):
    loc=fileloc()
    f=open(loc,"r")
    #print("opened")
    data=f.read()
    #print(data)
    f.close()
    t.insert('1.0',data)
    title_win()
is_on=False
def switch():
    if(cbval.get()==1):
       #on_button.config(image = on)
        root.config(bg='black')
        t.config(bg="black",fg='white',insertbackground="white")
        #scroll1.configure(bg="#454545")
        #scroll2.configure(bg="#454545")
        fmenu.config(bg="black",fg='white')
        fmenu.config(bg="black",fg='white') 
        
    else:
        #on_button.config(image = off)
        root.config(bg='white')
        t.config(bg="white",fg='black',insertbackground="black")
        #scroll1.configure(bg="white")
        #scroll1.configure(bg="white")
        fmenu.config(bg="white",fg='black')
        fmenu.config(bg="white",fg='black')
        
def savefile(*a): 
    dat=t.get("1.0", "end-1c") 
    try:
        
        f=open(loc,"w")
        f.write(dat)
        f.close()
    except NameError:
        saveasfile()
def saveasfile(*a):
    name=fd.asksaveasfile(mode='w',defaultextension=".txt")
    text2save=str(t.get(0.0,END))
    name.write(text2save)
    name.close
# Define Our Images
on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")
 
# Create A Button
#on_button = Button(root, image = off, bd = 0,command = switch)
#on_button.pack(side=TOP,pady = 5)
cbval=IntVar(value=0)

menubar=Menu(root, background='blue', fg='white')
fmenu=Menu(menubar,tearoff=1)
emenu=Menu(menubar,tearoff=1)
menubar.add_cascade(label="File",menu=fmenu)
menubar.add_cascade(label="Edit",menu=emenu)
fmenu.add_command(label="New         Ctrl+N",command=newfile)
fmenu.add_command(label="Open        Ctrl+O",command=openfile)
fmenu.add_command(label="Save        Ctrl+S",command=savefile)
fmenu.add_command(label="Save as     Ctrl+Shift+S",command=saveasfile)
fmenu.add_separator()
fmenu.add_command(label="Close       Alt+f4",command=root.destroy)

#menubar.add_cascade(checkb,command=thememode)
root.config(menu=menubar)



scroll1=ttk.Scrollbar(root,orient='horizontal')
scroll2=ttk.Scrollbar(root)
scroll1.pack(side = BOTTOM, fill = X)
scroll2.pack(side = RIGHT, fill = Y)
t=Text(root,width=700,height=500,xscrollcommand = scroll1.set,yscrollcommand = scroll2.set,undo=True)
t.pack(side=LEFT)
scroll1.config(command=t.xview)
scroll2.config(command=t.yview)

emenu.add_command(label ="Select All\t\t",command=select_all)
emenu.add_command(label ="Cut\t\t",command=cut_select)
emenu.add_command(label ="Copy\t\t",command=copy_select)
emenu.add_command(label ="Paste\t\t",command=paste_select)
emenu.add_command(label ="Undo\t\t",command=t.edit_undo)
emenu.add_command(label ="Redo\t\t",command=t.edit_redo)
emenu.add_checkbutton(label="Dark mode",variable=cbval,command=switch)
emenu.add_separator()
emenu.add_command(label ="Rename\t\t")
m = Menu(root, tearoff = 0)
m.add_command(label ="Select All\t\t",command=select_all)
m.add_command(label ="Cut\t\t",command=cut_select)
m.add_command(label ="Copy\t\t",command=copy_select)
m.add_command(label ="Paste\t\t",command=paste_select)
m.add_command(label ="Undo\t\t",command=t.edit_undo)
m.add_command(label ="Redo\t\t",command=t.edit_redo)
m.add_separator()
m.add_command(label ="Rename\t\t")
  
def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
def title_win():
    try:
        file_name = os.path.basename(loc)
        root.title(file_name)
    except NameError:
        root.title("newfile")
title_win()
#root.protocol("WM_DELETE_WINDOW",on_cls) 
t.bind("<Control-o>",openfile)
t.bind("<Control-n>",newfile)
t.bind("<Control-O>",openfile)
t.bind("<Control-N>",newfile)
t.bind("<Control-s>",savefile)
t.bind("<Control-S>",savefile)
t.bind("<Control--Shift-s>",saveasfile)
t.bind("<Control-Shift-S>",saveasfile)
t.bind("<Control-f>",search)
t.bind("<Button-3>", do_popup)
root.mainloop()
