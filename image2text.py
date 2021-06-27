import os
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import IntVar
from tkinter import SOLID
from tkinter import Entry
from tkinter import Radiobutton
from tkinter import Button
from tkinter import DISABLED
from tkinter import HORIZONTAL
from tkinter import END
from tkinter import W
import json
import webbrowser
import pytesseract
import time

import re
import uuid

class MenuBar(Menu):
    def __init__(self, ws):
        Menu.__init__(self, ws)

        file = Menu(self, tearoff=False)
        file.add_command(label="Open Config",command=self.openConfig)    
        file.add_separator()
        file.add_command(label="Exit", underline=1, command=self.quit)
        self.add_cascade(label="File",underline=0, menu=file)

        help = Menu(self, tearoff=0)  
        help.add_command(label="About", command=self.about)  
        help.add_command(label="Release Notes", command=self.release)  
        help.add_command(label="Instructions", command=self.instruction)  

        self.add_cascade(label="Help", menu=help)  

    def openConfig(self):
        curr_directory = os.getcwd()
        try:
            os.system("notepad config.json")
        except Exception as e:
            messagebox.showerror('Error', str(e)+'\nCannot locate config.json at ' + curr_directory)

    def exit(self):
        self.exit
    def release(self):
        webbrowser.open('https://github.com/jinlee487/image2text')
    def instruction(self):
        curr_directory = os.getcwd()
        try:
            os.system("notepad instruction.txt")
        except Exception as e:
            messagebox.showerror('Error', str(e)+'\nCannot locate instruction.txt at ' + curr_directory)
    def about(self):
        messagebox.showinfo('About', 'This is an open source image transcriber made by me, Jinlee487.' 
                    +' I will not assume any responsibility of others using this resource in any fashion.')

class GUI(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.style = ttk.Style()
        self.style.theme_use("winnative")
        self.videoOrAudio = IntVar()
        self.title('image2text')
        self.geometry('580x300')
        frame = Frame(self,bd=2, relief=SOLID, padx=10, pady=10)

        Label(frame, text="File Path", font=('Times', 14)).grid(row=0, column=0, sticky=W, pady=10)
        Label(frame, text="Download Path", font=('Times', 14)).grid(row=4, column=0, sticky=W, pady=10)
        Label(frame, text="Progress", font=('Times', 14)).grid(row=5, column=0, sticky=W, pady=10)
        self.reg_url = Entry(frame, font=('Times', 14), width=28,state=DISABLED)
        file_path_btn = Button(frame, width=4, text='new', font=('Times', 14), command=self.changeFilePath)
        self.downloadPath = Entry(frame, font=('Times', 14), width=28,state=DISABLED)
        path_btn = Button(frame, width=4, text='new', font=('Times', 14), command=self.changeDownloadPath)
        download_btn = Button(frame, width=10, text='Download', font=('Times', 14), command=self.downloadStream)
        cancel_btn = Button(frame, width=10, text='Cancel', font=('Times', 14), command=self.destroy)

        self.downloadText = scrolledtext.ScrolledText(frame,font=('Times', 14), height=3, width=38)

        self.reg_url.grid(row=0, column=1, columnspan=3, pady=2, padx=2)
        file_path_btn.grid(row=0, column=4)
        self.downloadPath.grid(row=4, column=1, columnspan=3, pady=2, padx=2)
        path_btn.grid(row=4, column=4)

        self.downloadText.grid(row=5, column=1, columnspan=10, pady=3, padx=2)

        download_btn.grid(row=7, column=4, pady=2, padx=2)
        cancel_btn.grid(row=7, column=3, pady=2, padx=2)
        frame.place(x=50, y=50)

        menubar = MenuBar(self)  
        self.config(menu=menubar)
        self.readConfig()

    def start_pb(self):
        # not used
        self.pb1.start(100)   
        
    def end_pb(self):
        # not used
        self.pb1.stop()

    def downloadStream(self):
        
        try: 
            if not self.downloadPath.get():
                raise ValueError()
            destination = os.path.normpath(self.downloadPath.get())
            self.downloadText.delete(1.0, END)
            self.downloadText.insert("end","")
        except ValueError as e:
            messagebox.showwarning("Warning", str(e) + "\nDownload directory is empty")
            return
        except Exception as e:
            messagebox.showwarning("Warning", str(e) + "\nPlease select the file you would like to download")
            return
        try: 
            image_path = self.reg_url.get()
            print(image_path)
            if os.path.isfile(image_path)!=True:
                raise ValueError()
        except ValueError as e:
            messagebox.showwarning("Warning", str(e) + "\nFile is empty")
            return
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        except Exception as e:
            messagebox.showwarning("Warning", str(e) + "\nFailed to locate pytesseract ")
            return
        try:
            new_file = os.path.join(destination.strip(),self.temporaryFileNameGenerator()+".txt")

            file = open(new_file, "w") 
            file.write(pytesseract.image_to_string(image_path)) 
            file.close()         
        except Exception as e:
            messagebox.showwarning("Warning", str(e) + "\nFailed to write text file")
            return
        try:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            new_file_name = os.path.join(destination.strip(),timestr+".txt")

            os.rename(new_file ,new_file_name)
            self.downloadText.insert(1.0,"Succefully saved file at location \n" + destination + "\n")
        except Exception as e:
            messagebox.showwarning("Warning", str(e) + "\nfailed to convert file name")
            return

    def temporaryFileNameGenerator(self):
        return str(uuid.uuid4())
         
    def readConfig(self):
        curr_directory = os.getcwd()
        try:
            f = open('config.json')
            data = json.load(f)
            if 'directory' not in data:
                raise ValueError()
            path = data['directory']
            self.downloadPath.configure(state='normal')
            self.downloadPath.delete("0", "end")
            self.downloadPath.insert("end",path)
            self.downloadPath.configure(state=DISABLED)
        except ValueError as e:
            messagebox.showerror('Error', str(e)+'\nCannot find directory key in config.json. Check if config.json has been modified.')
        except Exception as e: 
            messagebox.showerror('Error', str(e)+'\nCannot locate config.json at ' + curr_directory)

    def changeDownloadPath(self):
        dir_name = filedialog.askdirectory()  
        if(dir_name == ""):
            return
        with open("config.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["directory"] = dir_name

        with open("config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        self.readConfig()

    def changeFilePath(self):
        file_path = filedialog.askopenfilename(filetypes=(("All files", "*.*"),("jpg file", "*.jpg"), ("png file ",'*.png')))
        self.reg_url.configure(state='normal')
        self.reg_url.delete("0", "end")
        self.reg_url.insert("end",file_path)
        self.reg_url.configure(state=DISABLED)

if __name__ == "__main__":
    
    ws=GUI()
    ws.mainloop()




