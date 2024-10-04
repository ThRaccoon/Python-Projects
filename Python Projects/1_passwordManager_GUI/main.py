import tkinter
from tkinter import messagebox
import json
import random


# Global variables------------------------------------------------------------------------------------------------------
size = 1

KEY1 = 11
KEY2 = 5
# ----------------------------------------------------------------------------------------------------------------------

# The exception is checking if "lastUsedEmail.txt" exist
try:
    with open("lastUsedEmail.txt", 'r') as email_file:
        common_email = email_file.read()
except FileNotFoundError:
    email_file = open("lastUsedEmail.txt", 'x')
finally:
    email_file.close()


# Encrypt password------------------------------------------------------------------------------------------------------
def encrypt(password, key1, key2):
    for i in range(len(password)):
        password[i] = ord(password[i]) + key1
        if password[i] > 126:
            password[i] = chr((password[i] % 126) + 32)
        else:
            password[i] = chr(password[i])

    for j in range(len(password)):
        password[j] = ord(password[j]) + key2
        if password[j] > 126:
            password[j] = chr((password[j] % 126) + 32)
        else:
            password[j] = chr(password[j])

    return password


# Decrypt password------------------------------------------------------------------------------------------------------
def decrypt(password, key1, key2):
    for i in range(len(password)):
        password[i] = ord(password[i]) - key2
        if password[i] < 33:
            password[i] = chr(126 - abs(password[i] - 32))
        else:
            password[i] = chr(password[i])

    for j in range(len(password)):
        password[j] = ord(password[j]) - key1
        if password[j] < 33:
            password[j] = chr(126 - abs(password[j] - 32))
        else:
            password[j] = chr(password[j])

    return password


def search_by_app():
    app = app_text.get()

    # The exception is checking if the file is empty (if it is "json.load" and "app in data.keys" will crash)
    try:
        with open("myInfo.json", "r") as info_file:
            data = json.load(info_file)

            if app in data.keys():
                password = list(data[app]["password"])
                password = ''.join(decrypt(password, KEY1, KEY2))

                messagebox.askokcancel(title="Found", message=f"App: {app}\n"
                                                              f"Email: {data[app]["email"]}\n"
                                                              f"Password: {password}")
            else:
                messagebox.askokcancel(title="Not found", message="App is not found!")
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.askokcancel(title="Error", message="Your database is empty!")


def password_length(selected):
    if type(selected) is int:
        gen_button.config(state="normal")

    global size
    length = selected
    size = length / 2


def generate_password():
    global size
    password = []

    # Generating random letters and numbers
    for i in range(int(size)):
        # ------------------------------------------------------
        # Lower case
        password.append(chr(random.randint(97, 122)))
        # ------------------------------------------------------
        # Upper case
        # password.append(chr(random.randint(65, 90)))
        # ------------------------------------------------------
        # Random char
        # password.append(chr(random.randint(33, 47)))
        # ------------------------------------------------------
        # Int 0 - 9
        password.append(str(random.randint(0, 9)))
        # ------------------------------------------------------

    password[0] = (chr(random.randint(65, 90)))
    random.shuffle(password)

    # The middle of the password
    mid = int(len(password) / 2)

    if password[mid].isupper():
        password[mid + 1] = '-'
    else:
        password[mid] = '-'

    result = ''.join(password)
    password_text.delete(0, "end")
    password_text.insert(0, result)


def save_info():
    global email_file

    app = app_text.get()

    # The exception is checking if the file is empty (if it is "json.load" and "app in data.keys" will crash)
    try:
        with open("myInfo.json", "r") as file:
            json_data = json.load(file).keys()
            if app in json_data:
                messagebox.showerror(title="Error", message=f"{app} is already used!")
                return
    except (FileNotFoundError, json.JSONDecodeError):
        print("myInfo.json not found!")

    email = email_text.get()

    password = list(password_text.get())
    password = ''.join(encrypt(password, KEY1, KEY2))

    new_data = {
            app: {
                "email": email,
                "password": password,
            }
        }

    if len(app) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message=f"Don't leave empty boxes!")
    else:
        if messagebox.askokcancel(title="Is it ok to save?",
                                  message=f"App: {app} \nEmail: {email} \nPassword: {password}\n"
                                          f"The password above is already encrypted!\n"
                                          f"To see your password you have to enter correct app name in the app text box"
                                          f" and press search!"):

            # ------------------------------------------
            with open("lastUsedEmail.txt", "w") as email_file:
                email_file.write(email)
            # -------------------------------------------

            # -------------------------------------------
            try:
                with open("myInfo.json", "r") as file2:
                    # Reading old database
                    old_data = json.load(file2)
            # The excepting is checking 1.If the file doesn't exist 2.If the file is empty ("json.load" will crash).
            except (FileNotFoundError, json.JSONDecodeError):
                with open("myInfo.json", "w") as file2:
                    json.dump(new_data, file2, indent=3)
            else:
                # Updating old date
                old_data.update(new_data)
            # ------------------------------------------
                with open("myInfo.json", "w") as file2:
                    # Writing the updated data back to the file
                    json.dump(old_data, file2, indent=3)
            # ------------------------------------------
            finally:
                app_text.delete(0, "end")
                password_text.delete(0, "end")


# Creating the main window----------------------------------------------------------------------------------------------
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg="white")
window.resizable(False, False)

# Creating the main canvas----------------------------------------------------------------------------------------------
canvas = tkinter.Canvas(width=320, height=350, bg="white", highlightbackground="white")
myimg = tkinter.PhotoImage(file="png_1.png")
canvas.create_image(160, 175, image=myimg)
canvas.grid(row=0, column=1)

# App label-------------------------------------------------------------------------------------------------------------
app_label = tkinter.Label(text="App:", bg="white")
app_label.grid(row=1, column=0)
# App text box
app_text = tkinter.Entry(width=55, highlightthickness=1, highlightbackground="black")
app_text.focus()
app_text.grid(row=1, column=1)
# App search button
search_button = tkinter.Button(width=7, text="search", bg="white", command=search_by_app)
search_button.grid(row=1, column=2)

# Email label-----------------------------------------------------------------------------------------------------------
email_label = tkinter.Label(text="Email:", bg="white")
email_label.grid(row=2, column=0)
# Email text box
email_text = tkinter.Entry(width=65, highlightthickness=1, highlightbackground="black")

# The exception is catching if common_email is empty
try:
    email_text.insert(0, common_email)
except NameError:
    common_email = " "

email_text.grid(row=2, column=1, columnspan=2)

# Password label--------------------------------------------------------------------------------------------------------
password_label = tkinter.Label(text="Password:", bg="white")
password_label.grid(row=3, column=0)
# Password text box
password_text = tkinter.Entry(width=55, highlightthickness=1, highlightbackground="black")
password_text.grid(row=3, column=1)
# Generate password button
gen_button = tkinter.Button(text="generate", bg="white", command=generate_password, state="disabled")
gen_button.grid(row=3, column=2)

# Add button------------------------------------------------------------------------------------------------------------
add_button = tkinter.Button(text="add", width=55, height=1, bg="white", command=save_info)
add_button.grid(row=4, column=1, columnspan=2)

# Option menu-----------------------------------------------------------------------------------------------------------
value_inside = tkinter.StringVar(window)
value_inside.set("size")
options = (4, 8, 12, 16, 20)
question_menu = tkinter.OptionMenu(window, value_inside, *options, command=password_length)
question_menu.config(width=1, bg="white", highlightcolor="white", highlightthickness=1)
question_menu.grid(row=3, column=5)


window.mainloop()
