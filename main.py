import os
import shutil

username = "Luobo"
directory = "D:/Downloads/files"

# directory can be selected using the thing in tkinter
# directory = 'files'

# also set by user, if None will prompt user to assign, otherwise saves to a file and reloads on launch
destination_directory = directory+'/files'

def create_directory():
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

def mkdirs(newdir,mode=0o777):
    try:
        os.makedirs(newdir, mode)
    except OSError as err:
        return err

for filename in os.listdir(directory):

    # create_directory()

    if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(".pdf"):
        file_path = os.path.join(directory, filename)  # Get the full file path
        os.startfile(file_path)
        # files can be randomly selected for 'fun'
        # these 3 can be 5 stars you click on, with a submit button at the bottom
        print('Current file:', filename)
        rating = input(f'Enjoyability out of 5 stars: ')
        difficulty = input(f'Difficulty out of 5 stars: ')
        mastery = input(f'How well can you play the piece?: ')

        inputs = {'rating':rating, 'difficulty':difficulty, 'mastery':mastery}
        for category, stars in inputs.items():
            final_destination = destination_directory+'/'+category+'/'+stars
            print(f'{destination_directory}/{category}/{stars}')
            final_destination_file = os.path.join(final_destination, filename)
            final_destination_file = final_destination_file.replace('\\', '/')
            print(final_destination_file)

            if not os.path.exists(final_destination):
                try:
                    os.makedirs(final_destination, 0o777)
                except OSError as err:
                    print(err)
            # belongs up-top eventually

            if os.access(file_path, os.R_OK):
                shutil.copy(file_path, final_destination_file)

        os.remove(file_path)
        