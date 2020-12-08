from tkinter import *
from tkinter import messagebox as msgbx
from tkinter import filedialog
from random import randint
import json

root = Tk()
root.config(bg='#3e3c3c')
root.resizable(width=False, height=False)
root.overrideredirect(1)
root.geometry('1280x720')
root.hideids = {}

color = '#7e7e7e'
lastColor = 0
background = Frame(bg='#3e3c3c'); background.place(relx=0, rely=0, relwidth=1, relheight=1)
editor = Frame(bg='#efefef'); editor.movable = []; editor.functions = []
editorActive = False
editedWidget = None
editedBind = None
file = None

def exit(*args):
    root.destroy()
def exit_enter(*args):
    args[0].widget.config(bg='#e73b3b')
def exit_leave(*args):
    args[0].widget.config(bg='#808080')
def color_pick(*args):
    global color
    color = colorchooser.askcolor()
    colorLabel.config(bg=color[1])
def hide_screen(*args):
    root.overrideredirect(0)
    root.iconify()
def show_screen(*args):
    root.deiconify()
    root.overrideredirect(1)
def appear(*args):
    root.overrideredirect(1)
def alttab(event):
    root.overrideredirect(0)
    root.attributes('-topmost', False)
    root.iconify()
def changeState(widget):
    global state
    if state:
        widget.config(image='')
        state ^= True
        return
    widget.config(image=checkmark)
    widget.image = checkmark
    state ^= True
def discard_popup(event):
    event.widget.place_forget()
    generateFileButton.place_forget()
def generate(*args):
    global widthEntry, heightEntry, titleEntry, color, state, errorLabel, popup
    if not widthEntry.get() or not heightEntry.get():
        errorLabel.config(text='Some data is missing'); return
    errorLabel.config(text='')
    if not color:
        color = (None, '#efefef')
    else:
        color = (None, color)
    text = f'from tkinter import *\n\nroot = Tk()\nroot.resizable(width={state}, height={state})\n\
root.geometry(\'{widthEntry.get()}x{heightEntry.get()}\')\nroot.config(bg=\'{color[1]}\')\nroot.title(\'{titleEntry.get()}\')\n\n\
#your code here\n\n'
    for m in editor.movable:
        text += f'{m.name} = {str(m.type).split(".")[1][:-2]}(text=\'{m["text"]}\')\n'
    text += '\nroot.mainloop()'
    with open('file.py', 'w') as f:
        f.write(text)
    msgbx.showinfo(title='Success', message='File generated successfully')
def create(*args):
    global editor, widthEntry, heightEntry, editorSize, relSize, relPos, editorActive
    if not widthEntry.get() or not heightEntry.get():
        errorLabel.config(text='Width or height is missing'); return
    editorActive = True
    errorLabel.config(text='')
    editor.config(bg=color)
    offset = 0.25
    w, h = int(widthEntry.get()), int(heightEntry.get())
    scale = min([(1-offset)*1280/w, 720*0.965/h])
    editorSize = (w*scale, h*scale)
    relSize = (editorSize[0]/1280, editorSize[1]/720)
    relPos = ((1-offset-relSize[0])/2+offset, (1-0.035-relSize[1])/2+0.035)
    editor.place(relwidth=relSize[0], relheight=relSize[1], relx=relPos[0], rely=relPos[1])
    for m in editor.movable:
        try: a = m.my_relpos
        except:
            m.place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.1)
            make_draggable(m)

def showFileMenu(button):
    global generateFileButton
    generateFileButton.place(relx=0.035, rely=0.035, relwidth=0.125, relheight=0.035)
    saveProjectButton.place(relx=0.035,rely=0.07,relwidth=0.125,relheight=0.035)
    openProjectButton.place(relx=0.035, rely=0.105, relwidth=0.125, relheight=0.035)
    saveButton.place(relx=0.035, rely=0.14, relwidth=0.125, relheight=0.035)
    generateFileButton.lift(); saveProjectButton.lift(); openProjectButton.lift(); saveButton.lift()
    root.hideids = {}
    for ch in root.winfo_children():
        if ch not in [button, generateFileButton, saveProjectButton, openProjectButton, saveButton]: 
            root.hideids[str(ch)] = ch.bind('<Button-1>', hideFileMenu)
def hideFileMenu(event):
    global generateFileButton, saveProjectButton
    generateFileButton.place_forget()
    saveProjectButton.place_forget()
    openProjectButton.place_forget()
    saveButton.place_forget()
    for ch in root.winfo_children():
        try: ch.unbind('<Button-1>', root.hideids[str(ch)])
        except: pass
def showEditorMenu(button):
    global startEditorButton, addLabelEditor, addButtonEditor, addEntryEditor
    startEditorButton.place(relx=0.06, rely=0.035, relwidth=0.125, relheight=0.035)
    addLabelEditor.place(relx=0.06, rely=0.07, relwidth=0.125, relheight=0.035)
    addButtonEditor.place(relx=0.06, rely=0.105, relwidth=0.125, relheight=0.035)
    addEntryEditor.place(relx=0.06, rely=0.14, relwidth=0.125, relheight=0.035)
    startEditorButton.lift(); addLabelEditor.lift(); addButtonEditor.lift(); addEntryEditor.lift()
    root.hideids = {}
    for ch in root.winfo_children():
        if ch not in [button, addButtonEditor, addLabelEditor, addEntryEditor, startEditorButton]:
            root.hideids[str(ch)] = ch.bind('<Button-1>', hideEditorMenu)
def hideEditorMenu(event):
    global startEditorButton, addLabelEditor, addEntryEditor, addButtonEditor
    startEditorButton.place_forget()
    addLabelEditor.place_forget()
    addEntryEditor.place_forget()
    addButtonEditor.place_forget()
    for ch in root.winfo_children():
        try: 
            ch.unbind('<Button-1>', root.hideids[str(ch)])
            del root.hideids[str(ch)]
        except: pass
def draggable_slider(widget):
    widget.bind('<B1-Motion>', slider_drag_motion)
def slider_drag_motion(event):
    global lastColor, color
    widget = event.widget
    x = event.x_root
    if x/1280+0.01>0.032 and x/1280+0.01 < 0.192:
        widget.place(relx=x/1280)
        lastColor = int((((x-0.032*1280)/1280*0.16*100)+0.155)*100)
    h = hex(lastColor)[2:]
    h = '0'*(2-len(h))+h
    if widget == rSlider: 
        color = color[:1]+h+color[3:]
    elif widget == gSlider:
        color = color[:3]+h+color[5:]
    else:
        color = color[:5]+h

    colorLabel.config(bg=color)
    colorLabel2.config(text=color)
def widget_to_frame(button):
    if button == addLabelEditor:
        editor.movable.append(Label(text='Label', bg='#5a5a5a', fg='#e6e6e6'))
        editor.movable[-1].type = Label
    elif button == addButtonEditor:
        editor.movable.append(Label(text='Button', bg='#5a5a5a', fg='#e6e6e6'))
        editor.movable[-1].type = Button
    else:
        editor.movable.append(Label(text='Entry', bg='#5a5a5a', fg='#e6e6e6'))
        editor.movable[-1].type = Entry
    if editorActive:
        editor.movable[-1].place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.1)
        make_draggable(editor.movable[-1])
    editor.movable[-1].bind('<Button-3>', showOptions)
    editor.movable[-1].name = ''
    for _ in range(5):
        editor.movable[-1].name += chr(randint(97, 122))
def saveNew(*args):
    global file
    files = [('JSON', '*.json')]
    file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
    try: size = (int(widthEntry.get()), int(heightEntry.get()))
    except: size = (0, 0)
    with open(file, 'w') as f:
        data = {'title':titleEntry.get(), "width":size[0], "height":size[1],
        "bg":color, "resizable":state, "widgets":[], "editorStarted":editorActive}
        for m in editor.movable:
            data['widgets'].append({"name":m.name, "type":str(m.type), "color":m['bg'], "text":m['text'], "fg":m['fg'],
            "relx":m.my_relpos[0], "rely":m.my_relpos[1], "relwidth":m.my_relsize[0], "relheight":m.my_relsize[1]})
        f.write(json.dumps(data, indent=2))
    headerLabel['text'] = f'{file} - Tkinter App Generator'
def openProject(*args):
    global color, state, myCheckMark, file
    files = [('JSON', '*.json')]
    file = filedialog.askopenfilename(filetypes=files, defaultextension=files)
    with open(file) as f:
        data = json.loads(f.read())
    headerLabel['text'] = f'{file} - Tkinter App Generator'

    widthEntry.delete(0, END); widthEntry.insert(0, str(data['width']))
    heightEntry.delete(0, END); heightEntry.insert(0, str(data['height']))
    titleEntry.delete(0, END); titleEntry.insert(0, data['title'])

    c = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    rColor = data['bg'][1:3]
    rColor = c.index(rColor[0])*16+c.index(rColor[1])
    rSlider.place(relx=0.022+0.162*rColor/255)
    gColor = data['bg'][3:5]
    gColor = c.index(gColor[0])*16+c.index(gColor[1])
    gSlider.place(relx=0.022+0.162*gColor/255)
    bColor = data['bg'][5:7]
    bColor = c.index(bColor[0])*16+c.index(bColor[1])
    bSlider.place(relx=0.022+0.162*bColor/255)

    colorLabel['bg'] = data['bg']
    colorLabel2['text'] = data['bg']
    color = data['bg']

    if state != data['resizable']: changeState(myCheckMark)

    if data['editorStarted']: create()

    for m in data['widgets']:
        editor.movable.append(Label(text=m['text'], bg=m['color'], fg=m['fg']))

        if 'Label' in m['type']: editor.movable[-1].type = Label
        elif 'Button' in m['type']: editor.movable[-1].type = Button
        else: editor.movable[-1].type = Entry

        editor.movable[-1].place(relx=round(relPos[0]+m['relx']*relSize[0], 3), rely=round(relPos[1]+m['rely']*relSize[1], 3),
            relwidth=relSize[0]*m['relwidth'], relheight=relSize[1]*m['relheight'])
        editor.movable[-1].name = m['name']
        editor.movable[-1].my_relpos = [m['relx'], m['rely']]
        editor.movable[-1].my_relsize = [m['relwidth'], m['rely']]
        make_draggable(editor.movable[-1])
        editor.movable[-1].bind('<Button-3>', showOptions)
def save(*args):
    global file
    if file is None:
        files =[('JSON', '*.json')]
        file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
    if file is None: return
    try: size = (int(widthEntry.get()), int(heightEntry.get()))
    except: size = (0, 0)
    with open(file, 'w') as f:
        data = {'title':titleEntry.get(), "width":size[0], "height":size[1],
        "bg":color, "resizable":state, "editorStarted":editorActive, "widgets":[]}
        for m in editor.movable:
            data['widgets'].append({"name":m.name, "type":str(m.type), "color":m['bg'], "text":m['text'], "fg":m['fg'],
            "relx":m.my_relpos[0], "rely":m.my_relpos[1], "relwidth":m.my_relsize[0], "relheight":m.my_relsize[1]})
        f.write(json.dumps(data, indent=2))
    headerLabel['text'] = f'{file} - Tkinter App Generator'

#toolbar widgets
menuLabel = Label(bg='#808080'); menuLabel.place(relx=0, rely=0, relwidth=1, relheight=0.035)
headerLabel = Label(text='Tkinter App Generator', bg='#808080', fg='#e6e6e6')
headerLabel.place(relx=0, rely=0, relwidth=1, relheight=0.035)
exitImage = PhotoImage(file='exit.png')
minimizeImage = PhotoImage(file='minimize.png')
logoImage = PhotoImage(file='logo.png')
logoLabel = Label(image=logoImage, bg='#808080')
logoLabel.place(relx=0, rely=0, relheight=0.035, relwidth=0.035)
exitButton = Button(bd=0,image=exitImage, command=exit, bg='#808080')
exitButton.place(relx=0.965, rely=0, relwidth=0.035, relheight=0.035)
minimizeButton = Button(bd=0, image=minimizeImage, bg='#808080', command=hide_screen)
minimizeButton.place(relx=0.93, rely=0, relwidth=0.035, relheight=0.035)

#file Menu
fileMenu = Button(text='File', fg='#e6e6e6',bd=0, bg='#808080', command=lambda:showFileMenu(generateFileButton))
fileMenu.place(relx=0.035, rely=0, relwidth=0.025, relheight=0.035)
generateFileButton = Button(text='Generate Python file (Ctrl+g)', bg='#5a5a5a', fg='#e6e6e6', bd=0, command=generate)
saveProjectButton = Button(text='Save As New Project', bg='#5a5a5a',fg='#e6e6e6',bd=0,command=saveNew)
openProjectButton = Button(text='Open Project', bg='#5a5a5a', fg='#e6e6e6', bd=0, command=openProject)
saveButton = Button(text='Save Project (ctrl+s)', bg='#5a5a5a', fg='#e6e6e6', bd=0, command=save)

#editor Menu
editorMenu = Button(text='Editor', fg='#e6e6e6',bd=0, bg='#808080', command=lambda:showEditorMenu(startEditorButton))
editorMenu.place(relx=0.06, rely=0, relwidth=0.03, relheight=0.035)
startEditorButton = Button(text='Start Editor (Ctrl+e)', bg='#5a5a5a', fg='#e6e6e6', bd=0, command=create)
addLabelEditor = Button(text='Add Label (Ctrl+l)', bg='#5a5a5a', fg='#e6e6e6', bd=0, command=lambda:widget_to_frame(addLabelEditor))
addButtonEditor = Button(text='Add Button (Ctrl+b)', bg='#5a5a5a', fg='#e6e6e6', bd=0, command=lambda:widget_to_frame(addButtonEditor))
addEntryEditor = Button(text='Add Entry (Ctrl+n)', bg='#5a5a5a', fg='#e6e6e6', bd=0, command=lambda:widget_to_frame(addEntryEditor))

exitButton.bind('<Enter>', exit_enter); exitButton.bind('<Leave>', exit_leave)
menuLabel.bind('<Button-3>', show_screen)
menuLabel.bind('<Map>', appear)

#topBarSection
topBarSection = Label(text='Top Bar', font=('Arial', 15, 'bold'), bg='#3e3c3c', fg='#e6e6e6')
topBarSection.place(relx=0.035, relwidth=0.15, rely=0.04, relheight=0.05)
widthLabel = Label(text='Width:',bg='#3e3c3c', fg='#e6e6e6'); widthLabel.place(relx=0, rely=0.09, relwidth=0.1, relheight=0.05)
heightLabel = Label(text='Height:',bg='#3e3c3c', fg='#e6e6e6'); heightLabel.place(relx=0, rely=0.14, relwidth=0.1, relheight=0.05)
widthEntry = Entry(bd=0, justify='center', bg='#e6e6e6'); widthEntry.place(relx=0.1, rely=0.091, relwidth=0.1, relheight=0.048)
heightEntry = Entry(bd=0, justify='center', bg='#e6e6e6'); heightEntry.place(relx=0.1, rely=0.141, relwidth=0.1, relheight=0.048)
titleLabel = Label(text='Title:', bg='#3e3c3c', fg='#e6e6e6'); titleLabel.place(relx=0, rely=0.19, relwidth=0.1, relheight=0.05)
titleEntry = Entry(bd=0, justify='center'); titleEntry.place(relx=0.1, rely=0.191, relwidth=0.1, relheight=0.048)

#bodySection
bodySection = Label(text='Body', font=('Arial', 15, 'bold'), bg='#3e3c3c', fg='#e6e6e6')
bodySection.place(relx=0.035, rely=0.27, relwidth=0.15, relheight=0.05)
rLabel = Label(bg='#e6e6e6'); rLabel.place(relx=0.032, rely=0.345, relwidth=0.16, relheight=0.005)
rSlider = Label(bg='#909090'); rSlider.place(relx=0.102, rely=0.3375, relwidth=0.02, relheight=0.02)
draggable_slider(rSlider)
gLabel = Label(bg='#e6e6e6'); gLabel.place(relx=0.032, rely=0.37, relwidth=0.16, relheight=0.005)
gSlider = Label(bg='#909090'); gSlider.place(relx=0.102, rely=0.3625, relwidth=0.02, relheight=0.02)
draggable_slider(gSlider)
bLabel = Label(bg='#e6e6e6'); bLabel.place(relx=0.032, rely=0.395, relwidth=0.16, relheight=0.005)
bSlider = Label(bg='#909090'); bSlider.place(relx=0.102, rely=0.3875, relwidth=0.02, relheight=0.02)
draggable_slider(bSlider)
colorLabel = Label(bg=color)
colorLabel.place(relx=0.032, rely=0.42, relwidth=0.1, relheight=0.03)
colorLabel2 = Label(text='#7e7e7e', bg='#3e3c3c', fg='#e6e6e6')
colorLabel2.place(relx=0.132, rely=0.42, relwidth=0.06, relheight=0.03)
state = True; checkmark = PhotoImage(file='chekmark.png')
resizableLabel = Label(text='Resizable:', bg='#3e3c3c', fg='#e6e6e6')
resizableLabel.place(relx=0.015, rely=0.47, relwidth=0.1, relheight=0.05)
myCheckMark = Button(bg='#e6e6e6', image=checkmark, bd=0, command=lambda:changeState(myCheckMark))
myCheckMark.place(relx=0.145, rely=0.486, relwidth=0.01, relheight=0.02)

errorLabel = Label(text='', bg='#3e3c3c', fg='#e6e6e6', font=('arial', 15, 'bold'))
errorLabel.place(relx=0.0125, rely=0.93, relwidth=0.2, relheight=0.05)

def make_draggable(widget):
    widget.bind("<B1-Motion>", on_drag_motion)
def on_drag_motion(event):
    global relPos, relSize
    if editorActive:
        widget = event.widget
        x = event.x_root
        y = event.y_root
        if x/1280 > relPos[0] and x/1280 < relPos[0]+relSize[0]-widget.winfo_width()/1280 \
            and y/720 > relPos[1] and y/720 < relPos[1]+relSize[1]-widget.winfo_height()/720:
            widget.place(relx=x/1280, rely=y/720)

            relx = round(((x-320-(960-relSize[0]*1280)/2))/(relSize[0]*1280), 3)
            rely = round((y-25.2-(694.8-relSize[1]*720)/2)/(relSize[1]*720), 3)
            widget.my_relpos = [relx, rely]

            relX['text']=f'relx:  {relx}'; relY['text']=f'rely: {rely}'
def showOptions(event):
    global editedWidget, editedBind
    widget = event.widget
    relwidth, relheight = round(widget.winfo_width()/(relSize[0]*1280),3), round(widget.winfo_height()/(relSize[1]*720),3)
    widget.my_relsize = (relwidth, relheight)
    infoLabel.place_forget()
    widgetType.place(relx=0.016, rely=0.58, relwidth=0.2, relheight=0.05)
    varName.place(relx=0.01, rely=0.63, relwidth=0.1, relheight=0.05)
    varEntry.place(relx=0.11, rely=0.63, relwidth=0.1, relheight=0.048)
    textLabel.place(relx=0.01, rely=0.68, relwidth=0.1, relheight=0.05)
    textEntry.place(relx=0.11, rely=0.68, relwidth=0.1, relheight=0.048)
    bgColor.place(relx=0.01, rely=0.73, relwidth=0.1, relheight=0.05)
    bgEntry.place(relx=0.11,rely=0.73, relwidth=0.1, relheight=0.048)
    fgColor.place(relx=0.01, rely=0.78, relwidth=0.1, relheight=0.05)
    fgColor.place(relx=0.01, rely=0.78, relwidth=0.1, relheight=0.05)
    fgEntry.place(relx=0.11, rely=0.78, relwidth=0.1, relheight=0.048)
    sizeLabel.place(relx=0.01, rely=0.83, relwidth=0.1, relheight=0.05)
    widgetWidth.place(relx=0.11, rely=0.83, relwidth=0.049, relheight=0.048)
    widgetHeight.place(relx=0.161, rely=0.83, relwidth=0.049, relheight=0.048)
    sumbitInfo.place(relx=0.01, rely=0.88, relheight=0.025, relwidth=0.2)
    varEntry.delete(0, END); varEntry.insert(0, widget.name)
    widgetWidth.delete(0, END); widgetHeight.delete(0, END)
    widgetWidth.insert(0, relwidth); widgetHeight.insert(0, relheight)
    bgEntry.delete(0, END); fgEntry.delete(0, END)
    bgEntry.insert(0, widget['bg']); fgEntry.insert(0, widget['fg'])
    textEntry.delete(0, END); textEntry.insert(0, widget['text'])
    widgetType['text'] = f'Widget type:    {widget.type}'
    editedWidget = widget
    editedBind = root.bind('<Return>', submit)
def submit(event):
    global editedWidget, editedBind
    if not bgEntry.get():
        bgEntry.insert(0, '#7e7e7e')
    if not fgEntry.get():
        fgEntry.insert(0, '#7e7e7e')
    editedWidget.config(text=textEntry.get(), bg=bgEntry.get(), fg=fgEntry.get())
    editedWidget.name = varEntry.get()
    if (float(widgetWidth.get()),float(widgetHeight.get())) != editedWidget.my_relsize:
        if float(widgetWidth.get()) > 0.99:
            widgetWidth.delete(0, END); widgetWidth.insert(0, 'too big'); return
        if float(widgetHeight.get()) > 0.99:
            widgetHeight.delete(0, END); widgetHeight.insert(0, 'too big'); return
        editedWidget.my_relsize = (float(widgetWidth.get()),float(widgetHeight.get()))
        editedWidget.place(relwidth=float(widgetWidth.get())*relSize[0], relheight=float(widgetHeight.get())*relSize[1])
        if editedWidget.winfo_rootx()+editedWidget.my_relsize[0]*relSize[0]*1280 >= (relPos[0]+relSize[0])*1280:
            editedWidget.place(relx=relPos[0]+relSize[0]-editedWidget.my_relsize[0]*relSize[0])
        if editedWidget.winfo_rooty()+editedWidget.my_relsize[1]*relSize[1]*720 > (relPos[1]+relSize[1]+0.035)*720:
            editedWidget.place(rely=0.965-editedWidget.my_relsize[1]*relSize[1])
def add_widget_to_frame(event):
    if event.keycode == 76:
        editor.movable.append(Label(text='Label', bg='#5a5a5a', fg='#e6e6e6'))
        editor.movable[-1].type = Label
    elif event.keycode == 66:
        editor.movable.append(Label(text='Button', bg='#5a5a5a', fg='#e6e6e6'))
        editor.movable[-1].type = Button
    else:
        editor.movable.append(Label(text='Entry', bg='#5a5a5a', fg='#e6e6e6'))
        editor.movable[-1].type = Entry
    if editorActive:
        editor.movable[-1].place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.1)
        make_draggable(editor.movable[-1])
    editor.movable[-1].bind('<Button-3>', showOptions)
    editor.movable[-1].name = ''
    for _ in range(5):
        editor.movable[-1].name += chr(randint(97, 122))

#editorSection
widgetSection = Label(text='Widget Settings', font=('Arial', 15, 'bold'), bg='#3e3c3c', fg='#e6e6e6')
widgetSection.place(relx=0.037, rely=0.53, relwidth=0.15, relheight=0.05)
infoLabel = Label(text='You first need to click widget in editor', bg='#3e3c3c', fg='#e6e6e6')
infoLabel.place(relx=0.011, rely=0.58, relwidth=0.2, relheight=0.05)
widgetType = Label(text='', bg='#3e3c3c', fg='#e6e6e6')
varName = Label(text='Widget name:', bg="#3e3c3c", fg='#e6e6e6')
varEntry = Entry(justify='center', bd=0)
textLabel = Label(text='Widget text:',bd=0, bg='#3e3c3c', fg='#e6e6e6')
textEntry = Entry(justify='center', bd=0)
bgColor = Label(text='Background color:', bg='#3e3c3c', fg='#e6e6e6')
bgEntry = Entry(justify='center', bd=0)
fgColor = Label(text='Foreground color:', bg='#3e3c3c', fg='#e6e6e6')
fgEntry = Entry(justify='center', bd=0)
sizeLabel = Label(text='Width and height:', bg='#3e3c3c', fg='#e6e6e6')
widgetWidth = Entry(justify='center', bd=0); widgetHeight = Entry(justify='center', bd=0)
relX = Label(text='relx:', bg='#3e3c3c', fg='#e6e6e6', font=('arial',8,'bold')); relY = Label(text='rely:',bg='#3e3c3c',fg='#e6e6e6',font=('arial',8,'bold'))
relX.place(relx=0.01,rely=0.915, relwidth=0.1, relheight=0.025)
relY.place(relx=0.11,rely=0.915,relwidth=0.1, relheight=0.025)
sumbitInfo = Label(text='Click Enter to submit', bg='#3e3c3c', fg='#e6e6e6')

root.bind('<Control-n>', add_widget_to_frame)
root.bind('<Control-b>', add_widget_to_frame)
root.bind('<Control-l>', add_widget_to_frame)
root.bind('<Control-g>', generate)
root.bind('<Control-e>', create)
root.bind('<Control-s>', save)
root.mainloop()