import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from plyer import notification
import time
import sqlite3

dbms = sqlite3.connect("pomodoro.db")
cursor = dbms.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS pomodoro (id INTEGER PRIMARY KEY, date TEXT, name TEXT, duration INTEGER)")
dbms.commit()

root = ctk.CTk()
ctk.set_appearance_mode("Dark")
root.title("Pomodoro Timer")
root.geometry("350x200")
root.maxsize(350, 200)


def timer(x, timer_name):
    dur = x / 60
    cursor.execute("INSERT INTO pomodoro (date, name, duration) VALUES (?, ?, ?)",
                   (time.strftime("%d/%m/%Y"), timer_name, dur))
    dbms.commit()
    notification.notify(
        title="Timer Started",
        message=f"Starting your {timer_name} timer",
        timeout=5
    )
    root.withdraw()
    time.sleep(x)
    # Get the number of pomodoro completed in total
    cursor.execute("SELECT COUNT(*) FROM pomodoro")
    count = cursor.fetchone()[0]
    notification.notify(
        title="Timer Finished",
        message="You have completed {} pomodoro(s) to date. Open the app to set your next timer".format(count),
        timeout=5
    )
    root.deiconify()


def start():
    try:
        name = timer_name.get()
        try:
            entered_duration = int(tduration.get())
            duration = entered_duration * 60
            timer(duration, name)
        except:
            tk.messagebox.showerror("Error", "Please enter a valid number for duration")
    except:
        tk.messagebox.showerror("Error", "Encountered an error. Please try again")


def exit_timer():
    root.destroy()
    exit()


# Timer name
ctk.CTkLabel(root, text="Timer Name:").grid(row=0, column=0, padx=10, pady=20)
timer_name = tk.StringVar()
box = ctk.CTkEntry(root, textvariable=timer_name, justify="center", width=150)
box.insert(0, "Focus")
box.grid(row=0, column=1, padx=20)
# Duration
ctk.CTkLabel(root, text="Duration (in minutes): ").grid(row=1, column=0, padx=20, pady=10)
tduration = tk.IntVar()
tk.Spinbox(root, from_=1, to_=60, textvariable=tduration, width=10, justify="center").grid(row=1, column=1, padx=20)
# Functions
ctk.CTkButton(root, text="Start", command=start).grid(row=2, column=0, padx=10, pady=10)
ctk.CTkButton(root, text="Quit", command=exit_timer).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
