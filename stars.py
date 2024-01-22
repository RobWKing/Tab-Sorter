import tkinter as tk

# callback sends the identifier to the handle_star_clicks function in MainApplication upon button click

class StarGroup(tk.Frame):
    def __init__(self, parent, category, callback, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.callback = callback

        # sprites for buttons
        self.checked_button = tk.PhotoImage(file='images/star_checked.png')
        self.unchecked_button = tk.PhotoImage(file='images/star_unchecked.png')

        # create the list of unique ids for button names in the form {category{number}}, e.g. Difficulty5
        self.number_of_stars = 5
        self.button_identifiers = self.generate_button_ids(category)
        self.buttons = []




        for i, identifier in enumerate(self.button_identifiers):
            button = tk.Button(self, image=self.unchecked_button, relief='flat', command=lambda idx=i: self.button_click(idx))
            button.pack(side=tk.LEFT, padx=5)
            self.buttons.append(button)

    # Creates a unique id for each of the buttons - e.g. Rating1, Rating2, Rating3...
    def generate_button_ids(self, category):
        button_id_list = []
        for i in range(self.number_of_stars):
            item = f'{category}{i + 1}'
            button_id_list.append(item)
        return button_id_list


    def button_click(self, idx):
        # set all buttons back to 'unchecked', then use the idx of the clicked to iterate backwards through the list,
        # setting all buttons before it to be 'checked'.

        # actual logic including sending callback to main class
        self.reset_stars(idx)
        identifier = self.button_identifiers[idx]
        # print(f"Button {idx+1} ({identifier}) clicked!")
        self.callback(identifier)

        # changing appearance of buttons
        for i in range(idx+1):
            self.buttons[i].configure(image=self.checked_button)
            i -= 1



    def reset_stars(self, idx):
        # reset stars by setting all stars back to the appearance of unchecked button.
        for i in range(len(self.button_identifiers)):
            self.buttons[i].configure(image=self.unchecked_button)
            i += 1
