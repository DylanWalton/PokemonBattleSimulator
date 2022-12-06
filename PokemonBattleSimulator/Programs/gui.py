from tkinter import *
import customtkinter
from PIL import Image
import client
import csv

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

window = customtkinter.CTk()
window.geometry("700x500")
window.title("Pokemon Battle Simulator")
icon = PhotoImage(file='PokemonBattleSimulator\\Assets\\icon3.png')
window.iconphoto(True, icon)
window.resizable(False, False)

tabView = customtkinter.CTkTabview(master=window, width=window._current_width-20, height=window._current_height-15)
tabView.pack(padx=1, pady=1)
tab_Game = tabView.add("Game")
tab_Settings = tabView.add("Settings")

m_masterGameTab = tab_Game
m_masterSettingsTab = tab_Settings

#region GameTab
#region Images 
background = customtkinter.CTkImage(light_image=Image.open("PokemonBattleSimulator\\Assets\\MainBackground.png"),
                                    size=(450,170))
bg = customtkinter.CTkButton(master=m_masterGameTab, 
                             text="",
                             image=background,
                             width=500,
                             height=200,
                             fg_color="#222222",
                             hover=False)
bg.place(relx=.5, rely=.4, anchor=CENTER)
#endregion

#region Commands(Functions)
def play() :
    client.client_connect(str(ip), int(port))

def settings() :
    tabView.set("Settings")

def quit() :
    exit()
#endregion

#region Labels
label_Title = customtkinter.CTkLabel(master=m_masterGameTab, 
                                     text="Pokemon Battle Simulator", 
                                     text_color="white", 
                                     font=("Roboto", 24))
label_Title.place(relx=.5, rely=.1, anchor=CENTER)
#endregion

#region Buttons
m_height = 34
m_width = 174
m_fontSize = 17

button_Play = customtkinter.CTkButton(master=m_masterGameTab, 
                                      text="Play",
                                      command=play,
                                      width=m_width,
                                      height=m_height,
                                      font=(None, m_fontSize))

button_Settings = customtkinter.CTkButton(master=m_masterGameTab, 
                                         text="Settings",
                                         command=settings,
                                         width=m_width,
                                         height=m_height,
                                         font=(None, m_fontSize))

button_Quit = customtkinter.CTkButton(master=m_masterGameTab, 
                                      text="Quit",
                                      command=quit,
                                      width=m_width,
                                      height=m_height,
                                      font=(None, m_fontSize))

button_Play.place(relx=.5, rely=.65, anchor=CENTER)
button_Settings.place(relx=.5, rely=.74, anchor=CENTER)
button_Quit.place(relx=.5, rely=.83, anchor=CENTER)
#endregion
#endregion

#region SettingsTab

shouldSavePresets = False
savePresetsToggleValue = 0
ip, port = "", 0
with open("PokemonBattleSimulator\\presets.csv", "r") as file :
    save_Presets = file.readlines() 

#region Commands(Functions)
def set_username(username : customtkinter.CTkEntry) :
    if len(username.get()) <= 20 :
        #username.configure(text=username.get())
        print(username.get())
    else :
        username.configure(text="Limit Exceeded!", text_color="red")

def set_PortIP() :
    global ip, port

    ip = entry_IP.get()
    port = entry_Port.get()

    if shouldSavePresets :
        #name = input("What name would you like to save this preset under ?")
        data = ["name", ip, port]
        with open("PokemonBattleSimulator\\presets.csv", "a") as file :
            writer = csv.writer(file)
            writer.writerow(data)

def save_Presets() :
    global savePresetsToggleValue, shouldSavePresets

    if savePresetsToggleValue == 1 :
        radioButton_SavePresets.deselect()
        savePresetsToggleValue = 0
        shouldSavePresets = False
    else : 
        radioButton_SavePresets.select()
        savePresetsToggleValue = 1
        shouldSavePresets = True
    
#endregion

# Username Stuff
label_Username = customtkinter.CTkLabel(master=m_masterSettingsTab,
                                        text="Username",
                                        text_color="white",
                                        font=(None, 21))
label_Username.place(relx=.1, rely=.05, anchor=W)
entry_Username = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                        placeholder_text="Enter your username, 20 characters at the maximum",
                                        width=330)
entry_Username.place(relx=.1, rely=.13, anchor=W)
button_Username = customtkinter.CTkButton(master=m_masterSettingsTab,
                                          text="Set username",
                                          width=50,
                                          height=30,
                                          font=(None, 14),
                                          command=set_username(entry_Username))
button_Username.place(relx=.1, rely=.22, anchor=W)                

# IP and Port Stuff
label_Port = customtkinter.CTkLabel(master=m_masterSettingsTab,
                                    text="Server Port",
                                    font=(None, 21))
label_Port.place(relx=.1, rely=.4, anchor=W)
entry_Port = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                    placeholder_text="Enter the server port to connect to (i.e 1234)",
                                    width=330)
entry_Port.place(relx=.1, rely=.48, anchor=W)

label_IP = customtkinter.CTkLabel(master=m_masterSettingsTab,
                                    text="Server IP Address",
                                    font=(None, 21))
label_IP.place(relx=.1, rely=.59, anchor=W)
entry_IP = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                    placeholder_text="Enter the server IP address (i.e 127.0.0.1)",
                                    width=330)
entry_IP.place(relx=.1, rely=.67, anchor=W)
button_setPortIP = customtkinter.CTkButton(master=m_masterSettingsTab,
                                           text="Set IP and Port",
                                           width=90,
                                           height=30,
                                           font=(None, 14),
                                           command=set_PortIP)
button_setPortIP.place(relx=.1, rely=.76, anchor=W)
            
# Save Presets Stuff
radioButton_SavePresets = customtkinter.CTkRadioButton(master=m_masterSettingsTab,
                                                       text="Save Presets",
                                                       font=(None, 14), 
                                                       value=savePresetsToggleValue,
                                                       command=save_Presets)
radioButton_SavePresets.place(relx=.3, rely=.76, anchor=W)

optionMenu_LoadPresets = customtkinter.CTkOptionMenu(master=m_masterSettingsTab,
                                                     values=[])
#endregion

window.mainloop()
