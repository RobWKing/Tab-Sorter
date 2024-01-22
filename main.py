import os
# import shutil
import tkinter as tk
from tkinter import messagebox
from buttons import FetchButton, DeleteButton, SubmitButton
from stars import StarGroup
import random
username = "Luobo"
directory = "D:/Downloads/files"

# directory can be selected using the Windows explorer stuff in tkinter
# directory = 'files'

# also set by user, if None will prompt user to assign, otherwise saves to a file and reloads on launch
destination_directory = directory+'/files'

# these 2 are basically the same thing, turn them into one, remove code from main for loop
def create_directory(target_directory, mode=0o777):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory, mode)

def mkdirs(target_directory,mode=0o777):
    try:
        os.makedirs(target_directory, mode)
    except OSError as err:
        return err


# this will be a function that is run when the submit button is pressed
# I guess will first create a list of all filenames, then grab the next item when submit button is pressed...
# so possibly a few functions: initialize function when app opened + move files +  grab next file + UI class/function

# for filename in os.listdir(directory):
#
#     # create_directory()
#
#     if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(".pdf"):
#         file_path = os.path.join(directory, filename)  # Get the full file path
#         os.startfile(file_path)
#         # files can be randomly selected for 'fun'
#         # these 3 can be 5 stars you click on, with a submit button at the bottom
#         print('Current file:', filename)
#         rating = input(f'Enjoyability out of 5 stars: ')
#         difficulty = input(f'Difficulty out of 5 stars: ')
#         mastery = input(f'How well can you play the piece?: ')
#
#         inputs = {'rating':rating, 'difficulty':difficulty, 'mastery':mastery}
#         for category, stars in inputs.items():
#             final_destination = destination_directory+'/'+category+'/'+stars
#             print(f'{destination_directory}/{category}/{stars}')
#             final_destination_file = os.path.join(final_destination, filename)
#             final_destination_file = final_destination_file.replace('\\', '/')
#             print(final_destination_file)
#
#             if not os.path.exists(final_destination):
#                 try:
#                     os.makedirs(final_destination, 0o777)
#                 except OSError as err:
#                     print(err)
#             # belongs up-top eventually
#
#             if os.access(file_path, os.R_OK):
#                 shutil.copy(file_path, final_destination_file)
#
#         os.remove(file_path)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        window_width = int(self.parent.winfo_screenwidth() * 0.5)
        window_height = int(self.parent.winfo_screenheight() * 0.6)

        x = int((self.parent.winfo_screenwidth() - window_width) / 2)
        y = int((self.parent.winfo_screenheight() - window_height) / 2)

        self.parent.geometry(f"{window_width}x{window_height}+{x}+{y}")
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

        # create the interface
        self.create_labels()
        self.create_stars()
        self.create_buttons()


    def update_main_display(self, text_to_display):
        # checks the length of the text and adjusts the font accordingly
        # if other labels created later, take second argument of which label
        initial_font_size = 20
        multiplier = 30
        font_size = int(min(initial_font_size/len(text_to_display) * multiplier,20))
        print(font_size)
        self.main_display_label.config(text=text_to_display, font=("Verdana", font_size))

    def create_labels(self):
        self.main_display_label = tk.Label(self.parent, text='Fetch a file to begin!', font=("Verdana", 20), fg='black')
        self.main_display_label.pack(pady=(50, 30))

    def create_buttons(self):

        # an inner frame to organise buttons into a line
        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=(30,0))

        fetch_button = FetchButton(button_frame, self.fetch_new_file)
        fetch_button.pack(side=tk.LEFT, padx=5)

        submit_button = SubmitButton(button_frame, self.submit_file)
        submit_button.pack(side=tk.LEFT, padx=5)

        delete_button = DeleteButton(button_frame, self.delete_current_file)
        delete_button.pack(side=tk.LEFT, padx=5)

    def create_stars(self):
        categories = ['Rating', 'Difficulty', 'Mastery']
        for category in categories:
            label = tk.Label(self.parent, text=category, font=("Verdana", 14), fg='black')
            label.pack()
            row_of_stars = StarGroup(self.parent,category, self.handle_star_clicks)
            row_of_stars.pack()
            self.star_groups[category] = row_of_stars

    def handle_star_clicks(self, identifier):
        category = str()
        value = int()

        # When a star is clicked on, its id is sent here from StarGroup object, e.g. the third star of 'mastery', id = 'Mastery3'
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
        if not self.current_file:
            response = messagebox.askyesno("Caution", "Are you sure you wish to delete this file?")

            if response:
                # messagebox.showinfo("Order 66 executed.", "If file_deleted: print('File deleted successfully)")
                self.update_main_display('File deleted! Fetch another file to continue!')
                # do you want to actually confirm file was successfully deleted with another function?
            else:
                print("Operation cancelled.")

        else:
            print('no file to handle')

    def fetch_new_file(self):
        print('fetch new file here...')
        tabs = ['guitar_tab.pdf', 'other_tab.pdf', 'tab3.pdf']
        self.update_main_display(random.choices(tabs))

    def submit_file(self):
        # if there is a file loaded, switched to not for now, same as delete function
        if not self.current_file:

            # first check whether all 3 categories have been filled
            if all(value != 0 for value in (self.difficulty_value, self.rating_value, self.mastery_value)):

                self.copy_to_directories()

                # reset all stars to zero
                for star_group in self.star_groups.values():
                    star_group.reset_stars(0)
                #  reset all associated values to zero
                for category in self.categories:
                    setattr(self, f'{category.lower()}_value', 0)
                # reset current_file
                self.current_file = None

                # finally, resets the main display
                if self.check_file():
                    self.update_main_display('Completed! Fetch another file to continue!')
                    # self.update_main_display('Completed! continue!')
                    # self.update_main_display('Completed! Fetch another fi! Fetch another fi! Fetch another fi! Fetch another file to continue!')
                else:
                    self.update_main_display('Encountered an error copying files.')

            else:
                messagebox.showinfo("Oops", 'Complete all categories to continue')

    def check_file(self):
        print('check the 3 target directories for the file, return True if all present (if necessary')
        return True

    def copy_to_directories(self):
        print('copy to directories here')


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
