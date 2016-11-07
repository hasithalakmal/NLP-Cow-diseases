import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.resizable(width=False, height=False)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        s = ttk.Style()
        s.theme_use('clam')

        #chat history label
        self.chat_label = tk.Label(self, text="")
        self.chat_label.grid(row=0, column=0, columnspan=3)
        self.chat_label.config(font=("Calibri", 12))

        #initializing scrollbar
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.grid(row=1, column=4,rowspan=3, sticky=tk.N+tk.S)

        #chat box
        self.chat_box = tk.Listbox(self, width=120, yscrollcommand=self.scrollbar.set)
        self.chat_box.grid(row=1,column=0, rowspan=3,columnspan=3)
        self.chat_box.config(font=("Calibri", 10))

        #setting scrollbar to the chat box
        self.scrollbar.config( command = self.chat_box.yview )

        empty_label3 = tk.Label(self)
        empty_label3.grid(row=5)

        #initializing an access variable and question label
        self.var01 = tk.StringVar()
        self.doc_label = ttk.Label(self, textvariable=self.var01, justify=tk.LEFT, )
        self.doc_label.grid(row=6, column=0, columnspan=3)

        self.doc_label.config(font=("Calibri", 12))
        self.var01.set("")

        #initializing result label
        self.var02 = tk.StringVar()
        self.answer_label = tk.Label(self, textvariable=self.var02, justify=tk.LEFT, )
        self.answer_label.grid(row=7, column=0, columnspan=3)

        self.answer_label.config(font=("Courier", 11))
        self.var02.set("")

        #user input field
        self.chat_entry = ttk.Entry(self, width=100)
        self.chat_entry.grid(row=8, column=0,columnspan=3)


        empty_label2 = tk.Label(self)
        empty_label2.grid(row=9)

        #submit button
        self.button = ttk.Button(self, text="Submit")
        self.button.grid(row=10, column=1)

        empty_label = tk.Label(self)
        empty_label.grid(row=11)

    #for getting user input value
    def get_entry_value(self):
        return self.chat_entry.get()

    #set access variable of the label 01
    def set_var01(self, question):
        self.var01.set(question)

    #set access variable of the label 02
    def set_var02(self, result):
        self.var01.set(result)

    def set_chat_box(self,reply):
        self.chat_box.insert(tk.END, reply)

    def clear_entry(self):
        self.chat_entry.delete(0, 'end')


