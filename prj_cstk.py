# an AI/ML based Text summarizer


import tkinter
import tkinter as tk
from tkinter import scrolledtext
from tkinter import StringVar
from tkinter import *
import customtkinter
from customtkinter import *
from PIL import Image, ImageTk
import os
from tkinter import filedialog as fd 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from googletrans import Translator

def trans():
    selected_language = combobox_var.get()
    summary = e2.get("1.0", "end-1c")

    if selected_language != "-select-" and summary.strip() != "":
        translator = Translator()
        translated_summary = translator.translate(summary, dest=selected_language.lower())
        e2.delete("1.0", END)
        e2.insert(END, translated_summary.text)

def new():
    e1.delete(1.0,END)
    e2.delete(1.0,END)
    deltxt()

def About():
    from tkinter import messagebox
    messagebox.showinfo("Owner info. ", "version : 1.05v (beta)\nCreated by : SOLUTION FETCHERS")

def Contact():
    from tkinter import messagebox
    messagebox.showinfo("Contact ", "e-mail: solutionfetchers.team@gmail.com")


def exit_win():
    from tkinter import messagebox
    if messagebox.askokcancel("Exit ", "Do you want to exit?!"):
        app.destroy()

def choosefile():
    file = fd.askopenfile(mode ='r', filetypes =[('All Files', '*.*')])
    if file is not None:
        content = file.read()
        e1.insert(END,content)

def deltxt():
    canvas.delete(text4)
    canvas.delete(text5)
    #text4.config(text=" ")
    #text5.config(text=" ")
    
def summ():
    global s,deltxt,text4,text5
    s = ""
    text = e1.get("1.0", "end-1c")

    
    # Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    # Creating a frequency table to keep the score of each word
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Creating a dictionary to keep the score of each sentence
    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    # Average value of a sentence from the original text
    average = int(sumValues / len(sentenceValue))

    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence

    if 'text4' in globals():
        canvas.delete(text4)
    if 'text5' in globals():
        canvas.delete(text5)

    e2.insert(END,summary)
    text1 = e1.get("1.0", "end-1c")
    summ1 = e2.get("1.0", "end-1c")
    text4=canvas.create_text(1100,400,text="Original Text Length       :  " + str(len(text1)),font=('Arial', 15))
    text5=canvas.create_text(1100,700,text="Summarized Text Length     :  " + str(len(summ1)),font=('Arial', 15))
    




def save():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    summ=e2.get(1.0, "end-1c")
    f = open("summaries.rtf", "a")
    f.write("\ndate and time =")
    f.write(dt_string)
    f.write('\nSummary : ')
    f.write('\n\t\t')
    f.write(summ)
    f.write('\n ------------------------- \n')
    f.close()

    from tkinter import messagebox
    messagebox.showinfo(" ","Summary is successfully saved!")
    return

def clear():
    e1.delete(1.0,END)
    e2.delete(1.0,END)
    
    deltxt()
    
    





customtkinter.set_appearance_mode("light") # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue") # Themes: blue (default), dark-blue, green


app=customtkinter.CTk()
app.title('Text Summarizer')
app.geometry('1370x700')

menubar=Menu(app)
app.iconbitmap(r'D:\SIH\icon.ico') 
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label='New',command=new)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=exit_win)
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About',command=About)
helpmenu.add_separator()
helpmenu.add_command(label='Contact',command=Contact)
app.config(menu=menubar)


bg= ImageTk.PhotoImage(file="static/bg2.jpg")
canvas= Canvas(app,width= 1370, height= 700)
canvas.pack(expand=True, fill= BOTH)
canvas.create_image(0,0,image=bg, anchor="nw")


text1=canvas.create_text(900,50,text='Text summarizer',fill="Blue2",font=('Bell Gothic Std Black',40))
text2=canvas.create_text(150,200,text="Enter text : ",font=('Arial', 15))
text3=canvas.create_text(150,500,text="Summary : ",font=('Arial', 15))

button1=customtkinter.CTkButton(master=app,text='Summarize',fg_color='PaleGreen1',width=230, height=50,corner_radius=10,command=summ)
button1.place(x=600,y=80)
button2=customtkinter.CTkButton(app,text='(choose file)',fg_color='lemon chiffon',command=choosefile,width=50,corner_radius=00).place(x=80,y=175)
button3=customtkinter.CTkButton(app,text='Save',fg_color='CadetBlue1',command=save,width=90).place(x=150,y=600)
button4=customtkinter.CTkButton(app,text='Clear',fg_color='lemon chiffon',command=clear,width=90).place(x=280,y=600)
button5=customtkinter.CTkButton(app,text='Translate',fg_color='green yellow',command=trans,width=90).place(x=80,y=450)

n1 = StringVar()
e1 = tk.scrolledtext.ScrolledText(app)
e1.place(x=280,y=180,width=1000,height=200)

n2 = StringVar()
e2 = tk.scrolledtext.ScrolledText(app)
e2.place(x=280,y=480,width=1000,height=200)


combobox_var = customtkinter.StringVar(value="-select-")
combobox = customtkinter.CTkComboBox(master=app,values=["-select-", "Hindi", "Telugu", "Urdu"],variable=combobox_var).place(x=65,y=415)



canvas.pack()
app.protocol("WM_DELETE_WINDOW", exit_win)
app.mainloop()
