from tkinter import *
from datetime import datetime, timedelta
import time
from threading import Thread
import pygame

snooze_button = None  # Global reference

def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play()

def alarm_thread(alarm_time):
    global snooze_button
    triggered = False

    while not triggered:
        now = datetime.now().strftime("%H:%M:%S")
        print("Current:", now, "| Alarm:", alarm_time)
        if now >= alarm_time:
            play_alarm()
            show_snooze_button()
            triggered = True
        time.sleep(1)

def set_alarm():
    alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    print("Alarm set for:", alarm_time)
    status_label.config(text=f"Alarm set for {alarm_time}")
    Thread(target=alarm_thread, args=(alarm_time,), daemon=True).start()

def snooze_alarm():
    pygame.mixer.music.stop()  # Stop current sound

    # Add 5-minute snooze time
    snooze_time = datetime.now() + timedelta(minutes=5)
    new_alarm_time = snooze_time.strftime("%H:%M:%S")
    status_label.config(text=f"Snoozed for 5 minutes (New alarm: {new_alarm_time})")
    
    hide_snooze_button()

    # Start new alarm thread
    Thread(target=alarm_thread, args=(new_alarm_time,), daemon=True).start()

def show_snooze_button():
    global snooze_button
    snooze_button = Button(root, text="Snooze 5 min", font=("Arial", 12), command=snooze_alarm, bg="orange")
    snooze_button.pack(pady=10)

def hide_snooze_button():
    global snooze_button
    if snooze_button:
        snooze_button.destroy()
        snooze_button = None

# GUI setup
root = Tk()
root.title("Alarm Clock with Snooze")
root.geometry("350x300")
root.resizable(False, False)

Label(root, text="Set Time (24-hour format)", font=("Arial", 14)).pack(pady=10)

frame = Frame(root)
frame.pack()

hour = StringVar(value="00")
minute = StringVar(value="00")
second = StringVar(value="00")

Entry(frame, textvariable=hour, width=3, font=("Arial", 18)).pack(side=LEFT)
Label(frame, text=":", font=("Arial", 18)).pack(side=LEFT)
Entry(frame, textvariable=minute, width=3, font=("Arial", 18)).pack(side=LEFT)
Label(frame, text=":", font=("Arial", 18)).pack(side=LEFT)
Entry(frame, textvariable=second, width=3, font=("Arial", 18)).pack(side=LEFT)

Button(root, text="Set Alarm", font=("Arial", 14), command=set_alarm).pack(pady=20)

status_label = Label(root, text="", font=("Arial", 12))
status_label.pack()

root.mainloop()
