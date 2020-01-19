import sys

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

from program_data import LOCALFILE
from program_data import BACKUPPATH
from program_data import TOKEN

#initializing dropbox instance to none
dbx = None

# Upload Config
def backup():

    with open(LOCALFILE, 'rb') as f:

        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")

        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))

        except ApiError as err:
            # Dropbox space availability?

            if (err.error.is_path() and err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")

            elif err.user_message_text:
                print(err.user_message_text)

                sys.exit()

            else:
                print(err)
                sys.exit()

# file details

def checkFileDetails():

    print("Checking file details")

    for entry in dbx.files_list_folder('').entries:
        print("File list is : ")
        print(entry.name)


def beginTransfer():
    # Check for  access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")

    # Create instance of a Dropbox class.
    print("Creating a Dropbox object...")
    global dbx
    dbx = dropbox.Dropbox(TOKEN)

    # access token validity
    try: 
        dbx.users_get_current_account()

    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    '''
    '''
    try:
        checkFileDetails()

    except:
        sys.exit("Error while checking file details")
    

    print("Creating backup...")
    # Create a backup of the current settings file
    backup()

    print("Backup Successful!")