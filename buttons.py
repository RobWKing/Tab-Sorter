import tkinter as tk
from tkinter import messagebox
class SubmitButton(tk.Button):
    def __init__(self, parent, submit_file, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.config(text="Submit", command=self.button_click, font=("Verdana", 18), fg='black', bg='#C5C5C5')
        self.submit_choices = submit_file

    def button_click(self):
        self.submit_choices()


class FetchButton(tk.Button):
    def __init__(self, parent, request_new_file, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.config(text="Fetch", command=self.button_click, font=("Verdana", 12), fg='black', relief='groove', bg='#B4B4F5')
        self.request_new_file = request_new_file

    def button_click(self):
        self.request_new_file()


class DeleteButton(tk.Button):
    def __init__(self, parent, delete_current_file, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.config(text="Delete", command=self.button_click, font=("Verdana", 12), fg='black', relief='groove', bg='#EC4C2B')
        self.delete_file = delete_current_file

    def button_click(self):
        self.delete_file()
        # response = messagebox.askyesno("Caution", "Are you sure you wish to delete this file?")
        #
        # if response:
        #     print("Proceeding...")
        #     self.delete_file()
        # else:
        #     print("Operation cancelled.")



    def delete_file(self):
        pass
