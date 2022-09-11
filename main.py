import random
import string
from tkinter import *
from tkinter import messagebox
import pyperclip
import json
characters = [c for c in string.ascii_letters]
digits = [c for c in string.digits]
symbols = ["!", "$", "#", "%", "&"]
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    generated_characters = [random.choice(characters) for _ in range(5)]
    generated_digits = [random.choice(digits) for _ in range(2)]
    generated_symbols = [random.choice(symbols) for _ in range(2)]
    generated_password = generated_characters + generated_digits + generated_symbols
    random.shuffle(generated_password)
    generated_password_str = "".join(generated_password)
    password_entry.insert(index=0, string=generated_password_str)
    pyperclip.copy(generated_password_str)
    generated_password.clear()
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    if len(password_entry.get()) == 0 or len(website_entry.get()) == 0:
        messagebox.showerror(title='Validation', message='Fields cannot be blank!')
    else:
        new_data = {website_entry.get(): {
            'email': email_entry.get(),
            'password': password_entry.get()
        }}
        is_ok = messagebox.askokcancel(title=website_entry.get(),
                                       message='Are you OK to go ahead with these details?')
        if is_ok:
            try:
                with open('password.json', mode='r') as file:
                    data = json.load(file)
                    data.update(new_data)
            except FileNotFoundError:
                pass
            else:
                new_data = data
            finally:
                with open('password.json', mode='w') as file:
                    json.dump(new_data, file, indent=4)
                    website_entry.delete(first=0, last=END)
                    password_entry.delete(first=0, last=END)
                    messagebox.showinfo(title="Confirmation", message='Details added to file')


# -------------------


def search():
    with open(file='password.json') as file:
        website = website_entry.get()
        result_data = json.load(fp=file)
        try:
            messagebox.showinfo(message=f'email: {result_data[website]["email"]}\npassword: {result_data[website]["password"]}')
        except KeyError:
            messagebox.showerror(message='Password has not been for this site yet.')
# --------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(pady=40, padx=40)
canvas = Canvas(width=200, height=200)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)
password_label = Label(text='Password:')
password_label.grid(row=3, column=0)
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(row=1, column=1, sticky='EW')
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky='EW')
email_entry.insert(index=0, string='demoemail@gmail.com')
password_entry = Entry()
password_entry.grid(row=3, column=1, sticky='EW')
search = Button(text='Search', width=10, command=search)
search.grid(row=1, column=2, sticky='EW')
generate = Button(text='Generate Password', command=generate_password)
generate.grid(row=3, column=2)
add = Button(text='Add', width=37, command=save_password)
add.grid(row=5, column=1, columnspan=2)
window.mainloop()
