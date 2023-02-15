# Just a quick pomodoro timer with plyer

from plyer import notification
import time
import sqlite3

dbms = sqlite3.connect("pomodoro.db")
cursor = dbms.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS pomodoro (id INTEGER PRIMARY KEY, date TEXT, name TEXT, duration INTEGER)")
dbms.commit()


def timer(x, timer_name):
    # Add a session to the database with repeat and date
    dur = x / 60
    cursor.execute("INSERT INTO pomodoro (date, name, duration) VALUES (?, ?, ?)",
                   (time.strftime("%d/%m/%Y"), timer_name, dur))
    dbms.commit()
    notification.notify(
        title="Timer Started",
        message=f"Starting your {timer_name} timer",
        timeout=5
    )
    time.sleep(x)
    # Get the number of pomodoro completed in total
    cursor.execute("SELECT COUNT(*) FROM pomodoro")
    count = cursor.fetchone()[0]

    notification.notify(
        title="Timer Finished",
        message="You have completed {} pomodoro(s) to date. Open the app to set your next timer".format(count),
        timeout=5
    )


if __name__ == "__main__":
    while True:
        menu = input("Would you like to start a timer? (y/n): ")
        if menu == "n":
            print("Thanks for using the timer. Hope you got everything done!")
            break
        else:
            called = input("What would you like to call your timer: ")
            duration = int(
                input("How long would you like to set the timer for (in minutes): "))  # User will enter minutes
            duration = duration * 60  # Convert the value to actual seconds
            timer(duration, called)
