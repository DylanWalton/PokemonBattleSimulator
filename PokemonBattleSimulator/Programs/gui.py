from tkinter import *
import customtkinter
from PIL import Image
import client
from _ServerName import *

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
username = ""
with open("PokemonBattleSimulator\\username.txt", "r") as file :
    username = file.read()

with open("PokemonBattleSimulator\\presets.txt", "r") as file :
    m_savePresets = file.readlines()
for i, ligne in enumerate(m_savePresets) :
    m_savePresets[i] = m_savePresets[i][:-1]
for i, ligne in enumerate(m_savePresets) :
    m_savePresets[i] = m_savePresets[i].split(",")
displaySavePresets = []
for i in range(len(m_savePresets)) :
    displaySavePresets.append(m_savePresets[i][0])

#region Commands(Functions)
def set_username() :
    global username

    if len(entry_Username.get()) <= 20 :
        username = entry_Username.get()
        with open ("PokemonBattleSimulator\\username.txt", "w") as file :
            file.write(username)
        print(entry_Username.get())
    else :
        entry_Username.delete(0, len(entry_Username.get()))
        entry_Username.configure(placeholder_text="Limit Exceeded!", placeholder_text_color="red")

def set_PortIP() :
    global ip, port, m_savePresets

    ip = entry_IP.get()
    port = entry_Port.get()

    if shouldSavePresets and (ip != "" and port != "") :
        _ServerName.startDemandWindow()
        #name = input("What name would you like to save this preset under ?")
        data = ["name", ip, port]
        with open("PokemonBattleSimulator\\presets.txt", "a") as file :
            file.write("Name"+","+ip+","+port+"\n")
        m_savePresets.append(data)
        displaySavePresets.append(data[0])
        optionMenu_LoadPresets.configure(values=displaySavePresets)

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
    
def activatePreset(value) :
    global ip, port
    
    i = 0
    while displaySavePresets[i] != value :
        i+=1
    if i != 0 :
        entry_IP.delete(0, len(entry_IP.get()))
        entry_Port.delete(0, len(entry_Port.get()))
        entry_IP.insert(0, m_savePresets[i][1])
        entry_Port.insert(0, m_savePresets[i][2])
        entry_IP.configure(text_color="#42f58a")
        entry_Port.configure(text_color="#42f58a")
        ip, port = m_savePresets[i][1], m_savePresets[i][2]
    else :
        entry_IP.delete(0, len(entry_IP.get()))
        entry_Port.delete(0, len(entry_Port.get()))
        entry_IP.configure(placeholder_text="Enter the server IP address (i.e 127.0.0.1)", placeholder_text_color="grey")
        entry_Port.configure(placeholder_text="Enter the server port to connect to (i.e 1234)", placeholder_text_color="grey")
        ip, port = "", 0

def set_ServerName(name : str) :
    print(name)
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
if username != "" :
    entry_Username.configure(placeholder_text=username)                                        
entry_Username.place(relx=.1, rely=.13, anchor=W)
button_Username = customtkinter.CTkButton(master=m_masterSettingsTab,
                                          text="Set username",
                                          width=50,
                                          height=30,
                                          font=(None, 14),
                                          command=set_username)
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
                                                     values=displaySavePresets,
                                                     command=activatePreset)                                                     
optionMenu_LoadPresets.place(relx=.3, rely=.4, anchor=W)
#endregion

window.mainloop()
