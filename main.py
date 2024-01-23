import os
import shutil
import random
import tkinter as tk
from tkinter import messagebox, filedialog

from stars import StarGroup

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.window_width = int(self.parent.winfo_screenwidth() * 0.5)
        self.window_height = int(self.parent.winfo_screenheight() * 0.52)

        x = int((self.parent.winfo_screenwidth() - self.window_width) / 2)
        y = int((self.parent.winfo_screenheight() - self.window_height) / 2)

        self.parent.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.parent.title('Tab Sorter')
        self.parent.iconbitmap("images/guitar.ico")

        self.categories = ['Rating', 'Difficulty', 'Mastery']
        self.star_groups = {}

        self.rating_value = 0
        self.difficulty_value = 0
        self.mastery_value = 0

        self.main_display_label = None

        # logic for actual files
        self.current_file = None
        self.directory = None

        # checks whether there is a directory for first-time users
        self.check_directory()

        # create the interface
        self.create_labels()
        self.create_stars()
        self.create_buttons()


    def update_main_display(self, text_to_display):
        # if other labels created later, take second argument of which label

        # checks the length of the text and adjusts the font size accordingly, max font size of 20
        initial_font_size = 20
        multiplier = 45  # adjust this to get a size you like
        font_size = int(min(initial_font_size/len(text_to_display) * multiplier,20))

        self.main_display_label.config(text=text_to_display, font=("Verdana", font_size))

    def check_directory(self):
        # if the directory file is empty - i.e. there is no saved directory
        no_saved_directory = os.path.getsize('directory.txt') == 0

        # alert the user and run the directory setting function
        if no_saved_directory:
            messagebox.showinfo("Information", "No directory found")
            self.choose_directory()

        # otherwise, set self.directory to be the saved directory
        else:
            with open("directory.txt", "r") as file:
                self.directory = file.read()

    def choose_directory(self):

        # open a pop-up asking user to choose a directory
        new_directory = filedialog.askdirectory()

        # if they do choose one, not click cancel, then set self.directory, and save it to directory.txt
        if new_directory:
            # print("Selected directory:", new_directory)
            self.directory = new_directory
            messagebox.showinfo("Directory saved", "Set as the new default directory.")
            # print("Directory written to directory.txt")
            with open("directory.txt", "w") as file:
                file.write(new_directory)

        # if they do not choose one and there is no self.directory set (so no previous directory), run
        # check_directory() again
        if self.directory is None:
            self.check_directory()

    def create_labels(self):

        # create a frame for the main display, and set it be a fixed size to prevent the lower elements shifting around
        # depending on the font size of the main_display_label's text
        main_display_frame = tk.Frame(self.parent, width=self.window_width, height=30)
        main_display_frame.pack_propagate(False)
        main_display_frame.pack(side=tk.TOP, pady=(50,30))

        # create the text and attach to the display frame
        self.main_display_label = tk.Label(main_display_frame, text='Fetch a file to begin!', font=("Verdana", 20), fg='black')
        self.main_display_label.pack(side=tk.TOP)

    def create_buttons(self):

        # an inner frame to organise buttons into a line
        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=(30,0))

        directory_button = tk.Button(root, text="Set Directory", relief='groove', command=self.choose_directory)
        directory_button.place(relx=0.5, rely=0.07, anchor=tk.S)

        fetch_button = tk.Button(button_frame, text="Fetch", command=self.fetch_new_file,
                                 font=("Verdana", 12), fg='black', relief='groove', bg='#B4B4F5')
        fetch_button.pack(side=tk.LEFT, padx=5)

        submit_button = tk.Button(button_frame, text="Submit", command=self.submit_file,
                                  font=("Verdana", 18), fg='black', bg='#C5C5C5')
        submit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_current_file,
                                  font=("Verdana", 12), fg='black', relief='groove', bg='#EC4C2B')
        delete_button.pack(side=tk.LEFT, padx=5)

    def create_stars(self):

        # the self.categories in the init are the names of the categories that will have stars and the directories that
        # will be created and copied into
        # self.star_groups dictionary is created in order to reset the stars to zero upon button presses from the MainApplication
        for category in self.categories:
            label = tk.Label(self.parent, text=category, font=("Verdana", 14), fg='black')
            label.pack()
            row_of_stars = StarGroup(self.parent,category, self.handle_star_clicks)
            row_of_stars.pack()
            self.star_groups[category] = row_of_stars

    def handle_star_clicks(self, identifier):

        category = str()
        value = int()

        # When a star object is clicked on, its id is sent here from this StarGroup object, e.g. the third star of 'mastery', id = 'Mastery3'
        # Separate category name and star rating from the clicked button's name string
        for i, char in enumerate(identifier):
            if char.isdigit():
                category = identifier[:i]
                value = int(identifier[i])

        # update the MainApplication's values for the given category upon star button press, e.g. Mastery3 -> self.mastery_value = 3
        formatted_category = category.lower()
        setattr(self, f'{formatted_category}_value', value)

    def delete_current_file(self):
        # if there is currently a file loaded
        if self.current_file:
            response = messagebox.askyesno("Caution", "Are you sure you wish to delete this file?")

            if response:
                # messagebox.showinfo("Order 66 executed.", "If file_deleted: print('File deleted successfully)")
                os.remove(self.current_file)
                self.update_main_display('File deleted! Fetch another file to continue!')
                # do you want to actually confirm file was successfully deleted with another function?

                # reset all stars to zero, reset all associated values to zero and reset current_file
                self.reset_stars_values_file()

            else:
                print("Operation cancelled.")

        else:
            messagebox.showinfo("Error", 'No file to handle')

    def fetch_new_file(self):

        # reset all stars to zero, reset all associated values to zero and reset current_file
        self.reset_stars_values_file()

        pdf_files = []

        # Iterate over files in the directory
        for file_name in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file_name)

            # Check if the file is not a directory and ends with ".pdf"
            if os.path.isfile(file_path) and file_name.endswith(".pdf"):
                pdf_files.append(file_path)

        if pdf_files:
            # set current file randomly from the list
            self.current_file = random.choice(pdf_files)

            # fetch just the base filename and send to the main display
            formatted_file_name = os.path.basename(self.current_file)
            self.update_main_display(formatted_file_name)

            # open the current file
            os.startfile(self.current_file)
        else:
            self.update_main_display('No files found in this directory. Change directory and fetch again.')

    def submit_file(self):

        # if there is a file loaded, switched to not for now, same as delete function
        if self.current_file:

            # first check whether all 3 categories have been filled
            if all(value != 0 for value in (self.difficulty_value, self.rating_value, self.mastery_value)):

                self.copy_to_directories()

                # reset all stars to zero, reset all associated values to zero and reset current_file
                self.reset_stars_values_file()

                # finally, resets the main display
                self.update_main_display('Completed! Fetch another file to continue!')

            else:
                messagebox.showinfo("Oops", 'Complete all categories to continue')

        else:
            self.update_main_display('No file selected!')
            self.reset_stars_values_file()

    def copy_to_directories(self):
        inputs = {'Rating': self.rating_value, 'Difficulty': self.difficulty_value, 'Mastery': self.mastery_value}
        current_filename = os.path.basename(self.current_file)
        for category, stars in inputs.items():
            final_destination = self.directory+'/'+category+'/'+str(stars)
            final_destination_file = os.path.join(final_destination, current_filename)
            final_destination_file = final_destination_file.replace('\\', '/')
            print(final_destination_file)

            if not os.path.exists(final_destination):
                try:
                    os.makedirs(final_destination, 0o777)
                except OSError as err:
                    print(err)

            if os.access(self.current_file, os.R_OK):
                shutil.copy(self.current_file, final_destination_file)

        # when copying completed, delete original file
        os.remove(self.current_file)

    def reset_stars_values_file(self):
        # reset all stars to zero
        for star_group in self.star_groups.values():
            star_group.reset_stars(0)
        #  reset all associated values to zero
        for category in self.categories:
            setattr(self, f'{category.lower()}_value', 0)
        # reset current_file
        self.current_file = None

# for analysing
def print_vars():
    print('self.current_file:', mainapp.current_file)
    print('self.directory:', mainapp.directory)
    root.after(1000, print_vars)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    mainapp = MainApplication(root)
    mainapp.pack(side="top", fill="both", expand=True)
    # print_vars()
    root.mainloop()
