import tkinter as tk
from tkinter import *
from tkinter import ttk
from ApplicationUI import View
from DiseaseFinder import DiseaseFinder

class Controller:
    owner = ""
    cow = ""
    type = ""
    age = 0
    program_counter = int(0)
    disease_finder = None
    master = None
    list_counter = 1

    def __init__(self, root):
        self.master = root

        self.view1 = View(root)
        self.view1.chat_entry.bind('<Return>', self.get_user_input)
        #self.view1.set_var01("")
        self.start_app()


    #receives user input from view
    def get_user_input(self, event=None):
        user_input = self.view1.get_entry_value()

        self.view1.set_chat_box("   You: {}".format(user_input))

        if self.list_counter % 2 == 1:
            self.view1.chat_box.itemconfig(self.list_counter, foreground="orange")

        self.list_counter = (self.list_counter + 2)
        self.view1.clear_entry()
        self.perform_action(user_input)


    # perform the actions according to the program counter
    #0 - get owner name
    #1 - get cow name
    #2 - get cow type
    #3 - get age
    #4 - find disease
    def perform_action(self, user_input):

        if len(user_input) > 0:

            if self.program_counter == 0:
                self.owner = user_input
                self.view1.set_chat_box("   Doctor: Hello {}, What's your cow's name?".format(self.owner))
                self.view1.set_var02("Hello {}, What's your cow's name?".format(self.owner))
                self.program_counter += 1

            elif self.program_counter == 1:
                self.cow = user_input
                self.view1.set_chat_box("   Doctor: Is {} an adult cow or a calf? ".format(self.cow))
                self.view1.set_var02("Is {} an adult cow or a calf? ".format(self.cow))
                self.program_counter += 1

            elif self.program_counter == 2:
                reply = self.check_type(user_input.lower())
                self.view1.set_chat_box("   Doctor: {}".format(reply))
                self.view1.set_var02(reply)

            elif self.program_counter == 3:
                reply = self.check_age(user_input)
                self.view1.set_chat_box("   Doctor: {}".format(reply))
                self.view1.set_var02(reply)

            elif self.program_counter == 4:
                # preprocess user response
                value, reply = self.disease_finder.find_hit_diseases(user_input)
                self.check_hit(value, reply)

            self.view1.chat_box.see(END)

    def check_hit(self,value,reply):
        if value == 1:
            self.view1.set_chat_box("   Doctor: According to your description we think your cow has  {}".format(reply))
            self.view1.set_var02("According to your description we think your cow has {}".format(reply))
            self.create_restart()

            # self.messagebox.showinfo("Say Hello", "Hello World")

        elif value == 2:

            self.view1.set_chat_box(
                "   Doctor: Sorry we are unable to arrive at exact decision. But your cow may have \n{}".format(
                    str(reply)))
            self.view1.set_var02(
                "Sorry we are unable to arrive at exact decision. But your cow may have \n{} ".format(str(reply)))
            self.create_restart()

        elif value == 3:
            value,question = self.disease_finder.make_question()
            self.view1.set_chat_box("   Doctor: {}".format(question))
            self.view1.set_var02(question)

        elif value == 4:
            self.view1.set_chat_box("   Doctor: Sorry your reply is not clear. Does it have this symptom? {} ?".format(str(reply)))
            self.view1.set_var02("Sorry your reply is not clear. Does it have this symptom? {} ?".format(str(reply)))


    #check cow type
    def check_type(self,user_input):

        if "calf" in user_input:
            self.program_counter += 1
            self.type = "calf"
            return "Can you tell the age of {} in exact months: ".format(self.cow)

        elif "adult cow" in user_input:
            self.program_counter += 1
            self.type = "adult cow"
            return "Can you tell the age of {} in exact months: ".format(self.cow)

        else:
            return "We need to clearly know ,is {} an adult cow or a calf? ".format(self.cow)

    #check cow's age
    def check_age(self,user_input):
        try:
            self.age = int(user_input)

            #initialize DiseaseFinder
            self.disease_finder = DiseaseFinder(self.age,self.type)
            value, question = self.disease_finder.make_question()

            if value:
                self.program_counter += 1
                return "Can you say, what are the symptoms does {} have? {} ".format(self.cow, question)

            else:
                self.create_restart()
                return question

        except ValueError:
            return "Please specify the age in exact months"

    def create_restart(self):
        self.view1.chat_entry.config(state="disabled")
        self.view1.button.config(text="Restart", command=self.restart_app)

    def restart_app(self):
        self.owner = ""
        self.cow = ""
        self.type = ""
        self.age = 0
        self.program_counter = 0
        self.disease_finder = None
        self.start_app()

    def start_app(self):
        self.view1.set_var02("What is your name?")
        self.view1.set_chat_box("   Doctor: What is your name?")
        self.view1.chat_entry.config(state='normal')
        self.view1.button.configure(text="Submit", command=self.get_user_input)


    # def restart(self):
    #     self.master.destroy()
    #     root = tk.Tk()
    #     root.wm_title("Chat Application")
    #     root.withdraw()
    #     Controller(root)
    #     root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Chat Application")
    root.withdraw()
    app = Controller(root)
    root.mainloop()

