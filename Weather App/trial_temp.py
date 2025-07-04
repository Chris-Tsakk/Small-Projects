from tkinter import *
from tkinter import ttk
import json
import reguest

def update_weather_labels():

    with open("weather_data.json", "r") as file:
        weather_data = json.load(file)

    # Ενημέρωση των labels με τα δεδομένα του καιρού
    w_label1.config(text=weather_data["condition"])  # Καιρός
    temp_label1.config(text=weather_data["temperature"])  # Θερμοκρασία
    pr_label1.config(text=weather_data["pressure"])  # Πίεση
    wb_label1.config(text=weather_data["wind"])

selected_value = ""


def get_selected_value(com):
    global selected_value  # Χρησιμοποιούμε την παγκόσμια μεταβλητή
    selected_value = com.get()  # Παίρνουμε την τιμή από το Combobox
    reguest.get_full_weather(selected_value)

    # Ενημερώνουμε τα labels μετά τη λήψη των δεδομένων
    update_weather_labels()



win= Tk()
win.title("Weather")
win.config(bg="green")
win.geometry("500x400")



name_label= Label(win,text="Weather App",font=("Helvetica",30,"bold"))
name_label.place(x=27, y=49, height=40 , width= 430)
list_name=["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

com1 = ttk.Combobox(win,values=list_name , font=("Helvetica",15,"bold"))
com1.place(x=27,y=100,height=40,width=430)

button = Button(win,text="Done", command=lambda: get_selected_value(com1), font=("Comic Sans MS",30,"bold"))
button.place(x=190,y=150,height=50,width=99)


w_label=Label(win,text="Climate",font=("Comic Sans MS",15,"bold"))
w_label.place(x=26,y=200,height=50,width=100)
w_label1=Label(win,text="",font=("Comic Sans MS",15,"bold"))
w_label1.place(x=200,y=200,height=50,width=100)

wb_label=Label(win,text="Wind",font=("Comic Sans MS",15,"bold"))
wb_label.place(x=26,y=255,height=50,width=100)
wb_label1=Label(win,text="",font=("Comic Sans MS",15,"bold"))
wb_label1.place(x=200,y=255,height=50,width=100)

temp_label=Label(win,text="Temp",font=("Comic Sans MS",15,"bold"))
temp_label.place(x=26,y=310,height=50,width=100)
temp_label1=Label(win,text="",font=("Comic Sans MS",15,"bold"))
temp_label1.place(x=200,y=310,height=50,width=100)

pr_label=Label(win,text="Presure",font=("Comic Sans MS",15,"bold"))
pr_label.place(x=26,y=365,height=50,width=100)
pr_label1=Label(win,text="",font=("Comic Sans MS",15,"bold"))
pr_label1.place(x=200,y=365,height=50,width=100)

win.mainloop()