from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()

    new_data = {
        website_data.lower(): {
            "email": email_data,
            "password": password_data,
        }
    }

    if len(website_data) > 0 and len(email_data) > 0 and len(password_data) > 0:
        is_ok = messagebox.askokcancel(
            title=website_data,
            message=f"There are the details entered:\nUsername: {email_data}"
                    f"\nPassword: {password_data} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    # reading old data
                    json_data = json.load(f)
            except FileNotFoundError:
                # create a data.json file
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(new_data, f, indent=4)
            else:
                json_data.update(new_data)
                with open("data.json", "w", encoding="utf-8") as f:
                    # saved new data
                    json.dump(json_data, f, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
    else:
        messagebox.showerror(title="Oppss", message="Please dont leave any fields empty!")


def find_password():
    website = website_entry.get().lower()
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found")
    else:
        if website in json_data:
            email = json_data[website]["email"]
            password = json_data[website]["password"]
            messagebox.showinfo(
                title=website,
                message=f"Username: {email}\nPassword: {password}\nPassword copied to clipboard")
            pyperclip.copy(password)
            website_entry.delete(0, END)
        else:
            messagebox.showerror(title="No data found", message="No details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=0, row=0, columnspan=3)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=23)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=42)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "ing.davidfuentes@gmail.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=23)
password_entry.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
