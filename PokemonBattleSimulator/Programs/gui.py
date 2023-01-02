from tkinter import *
import customtkinter
from PIL import Image
import socket
import threading
from random import randint
import c_pokemon
import c_dresseur

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

assetsLoc = "..\\PokemonBattleSimulator\\Assets\\"
dataLoc = "..\\PokemonBattleSimulator\\Data\\"
pokImagesLoc = "..\\PokemonBattleSimulator\\PokemonData\\Images\\"
pokMetaLoc = "..\\PokemonBattleSimulator\\PokemonData\\Meta\\"

window = customtkinter.CTk()
window.geometry("700x500")
window.title("Pokemon Battle Simulator")
icon = PhotoImage(file=f"{assetsLoc}icon3.png")
window.iconphoto(True, icon)
window.resizable(False, False)

tabView = customtkinter.CTkTabview(master=window, width=window._current_width-20, height=window._current_height-15)
tabView.pack(padx=1, pady=1)
tab_Game = tabView.add("Game")
tab_Settings = tabView.add("Settings")

m_masterGameTab = tab_Game
m_masterSettingsTab = tab_Settings
                                                                            
#region MainTab
#region Images 
background = customtkinter.CTkImage(light_image=Image.open(f"{assetsLoc}MainBackground.png"),
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
    #load()

    try :
        client_connect(str(ip), int(port))
        receive_Process.start()
    except ValueError as v :
        errorPopUp("Double check the IP and Port")
        #loadFailed()
    except ConnectionRefusedError as c :
        if c.winerror != 1 :
            errorPopUp("The attempted server is likely down")
            #loadFailed()
    except OSError as e:
        if e.winerror != 1 :
            errorPopUp("Double check the IP and Port")
            #loadFailed()

def settings() :
    tabView.set("Settings")

def quit() :
    try :
        client.close()
    except :
        exit()
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
with open(f"{dataLoc}username.txt", "r") as file :
    username = file.read()

with open(f"{dataLoc}presets.txt", "r") as file :
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
        with open (f"{dataLoc}username.txt", "w") as file :
            file.write(username)
    else :
        entry_Username.delete(0, len(entry_Username.get()))
        entry_Username.configure(placeholder_text="Limit Exceeded!", placeholder_text_color="red")

def set_PortIP() :
    global ip, port, m_savePresets

    ip = entry_IP.get()
    port = entry_Port.get()

    if shouldSavePresets and (ip != "" and port != "") :
        m_name = entry_ServerName.get()
        data = [m_name, ip, port]
        with open(f"{dataLoc}presets.txt", "a") as file :
            file.write(m_name+","+ip+","+port+"\n")
        m_savePresets.append(data)
        displaySavePresets.append(data[0])
        optionMenu_LoadPresets.configure(values=displaySavePresets)

def save_Presets() :
    global savePresetsToggleValue, shouldSavePresets

    if savePresetsToggleValue == 1 :
        radioButton_SavePresets.deselect()
        savePresetsToggleValue = 0
        shouldSavePresets = False
        entry_ServerName.place(relx=.1, rely=4, anchor=W)
    else : 
        radioButton_SavePresets.select()
        savePresetsToggleValue = 1
        shouldSavePresets = True
        entry_ServerName.place(relx=.1, rely=.86, anchor=W)
    
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
entry_ServerName = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                          placeholder_text="Server Name",
                                          width=240)
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

#region LoadingFrame
#frame_LoadingFrame = customtkinter.CTkFrame(master=window,
#                                            width=window._current_width-20, 
#                                            height=window._current_height-20)
#progressBar_LoadingBar = customtkinter.CTkProgressBar(master=frame_LoadingFrame,
#                                                        width=300,
#                                                        height=15,
#                                                        progress_color="yellow",
#                                                        mode="indeterminate",
#                                                        indeterminate_speed=1)

#def load() :
#    tabView.place(relx=10)
#    frame_LoadingFrame.place(relx=.5, rely=.5, anchor=CENTER)   
#
#    label_Loading = customtkinter.CTkLabel(master=frame_LoadingFrame,
#                                        text="Loading",
#                                        text_color="white",
#                                        font=(None, 31))
#    label_Loading.place(relx=.5, rely=.4, anchor=CENTER)
#    progressBar_LoadingBar.place(relx=.5, rely=.5, anchor=CENTER)
#    progressBar_LoadingBar.start()

#def loadFailed() :
#    tabView.place(relx=.5, rely=.488, anchor=CENTER)
#    frame_LoadingFrame.place(relx=20)
#    progressBar_LoadingBar.stop()
#endregion

#region Error Notifier
label_ErrorNotifier = customtkinter.CTkLabel(master=window,
                                             text_color="red",
                                             font=(None, 17))

image_IgnoreError = customtkinter.CTkImage(light_image=Image.open(f"{assetsLoc}YellowDot.png"),
                                    size=(20,20))

def ignorePopUp() :
    label_ErrorNotifier.place(relx=.17, rely=5, anchor=S)
    button_IgnoreError.place(relx=.353, rely=5, anchor=S)

button_IgnoreError = customtkinter.CTkButton(master=window,
                                             image=image_IgnoreError,
                                             width=28,
                                             height=28,
                                             command=ignorePopUp,
                                             text="",
                                             fg_color="#1A1A1A")

def errorPopUp(error : str) :
    label_ErrorNotifier.configure(text=error)
    if len(error) < 31 :
        label_ErrorNotifier.place(relx=.17, rely=.99, anchor=S)
        button_IgnoreError.place(relx=.353, rely=.99, anchor=S)
    else :
        label_ErrorNotifier.place(relx=.2, rely=.99, anchor=S)
        button_IgnoreError.place(relx=.415, rely=.99, anchor=S)
#endregion

#region Client
client = None
connected = False
FORMAT = "utf-8"
players = []

def client_connect(ip : str, port : int) :
    global client
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    lobby()

def client_receive() :
    while True :
        try :
            global client
            message = client.recv(1024).decode(FORMAT)
            if message == "alias?" :
                client.send(username.encode(FORMAT))
            elif "!" in message :
                if "!players:" in message :
                    global players
                    client.send(" ".encode(FORMAT))
                    message = message.replace("!players:", "")
                    message = message.replace("[", "")
                    message = message.replace("]", "")
                    message = message.replace("b'", "")
                    message = message[:-1]
                    message = message.split(",")
                    players = message
                    i = 0
                    for player in players :
                        player = player.replace(" ", "")
                        player = player.replace("'", "")
                        players[i] = player
                        i += 1
                    players.remove(username)
                    displayPlayers()
                elif "!invite:" in message :
                    message = message.replace("!invite:", "")
                    message = message.split(",")
                    if message[0] == username :
                        recvInvite(message[1])
                elif "!inviteaccepted:" in message :
                    message = message.replace("!inviteaccepted:", "")
                    #message = message.split(",")
                    if message == chosenPlayer :
                        battle()
                elif "!left:" in message :
                    message = message.replace("!left:", "")
                    message = message.replace("b'", "")
                    message = message[:-1]
                    global poppedPlayer
                    poppedPlayer = players.index(message)
                    players.remove(message)
                    displayPlayers()
                elif "!ready:" in message :
                    message = message.replace("!ready:", "")
                    message = message.replace("b'", "")
                    message = message.split(",")
                    if message[1] == chosenPlayer :
                        global opponentPokemon, opponentLvl, opponentHP
                        opponentPokemon = message[0]
                        opponentLvl = int(message[2])
                        opponentHP = int(message[3])
                        if tamer == None :
                            global opponentIsReady
                            opponentIsReady = True
                        else : goToBattle()
                else :
                    textbox_Chat.insert("0.0", message+"\n\n")
            elif "$" in message :
                if "$attack:" in message :
                    message = message.replace("b'", "")
                    message = message.replace("$attack:", "")
                    message = message.split(",")
                    if message[0] == chosenPlayer :
                        if message[2] != "n" :
                            takeDamage(message, True)
                        else :
                            takeDamage(message, False)
                elif "$health:" in message :
                    message = message.replace("b'", "")
                    message = message.replace("$health:", "")
                    message = message.split(",")
                    if message[1] == chosenPlayer :
                        oppHealthVis(message[0])
                if "$death:" in message :
                    message = message.replace("b'", "")
                    message = message.replace("$death:", "")
                    if message == chosenPlayer :
                        winFrame()
            else :
                textbox_Chat.insert("0.0", message+"\n\n")
        except :
            print("Error!")
            client.close()
            break

roundsForEffectLeft = []
damagePerRound = []
effectNames = []

def client_send() :
    if entry_Chat.get() != "" :
        message = f"{username}  >>  {entry_Chat.get()}"
        client.send(message.encode(FORMAT))
        entry_Chat.delete(0, len(entry_Chat.get()))
#endregion

#region Lobby
frame_LobbyFrame = customtkinter.CTkFrame(master=window,
                                              width=window._current_width-20, 
                                              height=window._current_height-20)
entry_Chat = customtkinter.CTkEntry(master=frame_LobbyFrame, placeholder_text="Message everyone", width=593, height=30)
textbox_Chat = customtkinter.CTkTextbox(master=frame_LobbyFrame, width=290, height=370, border_color="black", border_width=1, text_color="orange")
frame_Players = customtkinter.CTkFrame(master=frame_LobbyFrame, width=210, height=370, fg_color="#1A1A1A", border_color="black", border_width=1)

def lobby() :
    tabView.place(relx=10)
    frame_LobbyFrame.place(relx=.5, rely=.5, anchor=CENTER)

    label_ServerTitle = customtkinter.CTkLabel(master=frame_LobbyFrame,
                                               text=optionMenu_LoadPresets.get(),
                                               font=(None, 27),
                                               text_color="#229fe7")
    label_ServerTitle.place(relx=.42, rely=0.05, anchor=CENTER)

    label_Players = customtkinter.CTkLabel(master=frame_LobbyFrame, text="Players", font=(None, 20))
    label_Players.place(relx=.545, rely=.126, anchor=W)
    frame_Players.place(relx=.436, rely=.54, anchor=W)
    button_Battle = customtkinter.CTkButton(master=frame_LobbyFrame, text="Battle", font=(None, 18), fg_color="green", width=160, height=30, text_color="white", command=requestBattle)
    button_Battle.place(relx=.873, rely=.27, anchor=CENTER)
    button_Back = customtkinter.CTkButton(master=frame_LobbyFrame, text="Back", font=(None, 18), fg_color="#ef9c06", width=160, height=30, text_color="white", command=backToMain)
    button_Back.place(relx=.873, rely=.34, anchor=CENTER)
    button_QuitLobby = customtkinter.CTkButton(master=frame_LobbyFrame, text="Quit", font=(None, 18), fg_color="#af0400", width=160, height=30, text_color="white", command=quit)
    button_QuitLobby.place(relx=.873, rely=.41, anchor=CENTER)

    entry_Chat.place(relx=0, rely=.97, anchor=W)
    image_SendArrow = customtkinter.CTkImage(light_image=Image.open(f"{assetsLoc}SendArrow2.png"),
                                    size=(34,23))
    button_SendChat = customtkinter.CTkButton(master=frame_LobbyFrame, fg_color="#229fe7", image=image_SendArrow, width=85, height=30, text="", command=client_send)
    button_SendChat.place(relx=.875, rely=.97, anchor=W)

    label_Chat = customtkinter.CTkLabel(master=frame_LobbyFrame, text="Chat", font=(None, 20))
    label_Chat.place(relx=.18, rely=.126, anchor=W)
    textbox_Chat.place(relx=0, rely=.54, anchor=W)

playerLabels = []
chosenPlayer = None
optionMenu_Players = None
poppedPlayer = None

def displayPlayers() :
    global players, playerLabels, optionMenu_Players
    values = ["Players"]
    j = 0
    for label in playerLabels :
        label.destroy()
        playerLabels.pop(j)
        j += 1

    i = 0
    n = .04
    distanceBetweenButtons = .07

    for player in players :      
        values.append(player)
        playerLabels.append(None)
        playerLabels[i] = customtkinter.CTkLabel(master=frame_Players, text=player, width=180, height=25, font=(None, 17))
        #, corner_radius=0, fg_color="#121212"
        playerLabels[i].place(relx=.5, rely=n, anchor=CENTER)
        i += 1
        n += distanceBetweenButtons

    optionMenu_Players = customtkinter.CTkOptionMenu(master=frame_LobbyFrame, values=values, command=playerChosen, width=160)
    optionMenu_Players.place(relx=.873, rely=.19, anchor=CENTER)

def playerChosen(text) :
    global chosenPlayer
    chosenPlayer = text

inviteDenied = True
inviterName = None

def requestBattle() :
    # send invite to chosen player
    if inviteDenied :
        client.send(f"!invite:{chosenPlayer},{username}".encode(FORMAT))
        textbox_Chat.insert("0.0", f"Invite sent to {chosenPlayer}\n")
    elif optionMenu_Players.get() == inviterName :
        client.send(f"!inviteaccepted:{username}".encode(FORMAT))
        battle()

def backToMain() :
    global client
    client.close()
    frame_LobbyFrame.place(relx=10)
    tabView.place(relx=.5, rely=.488, anchor=CENTER)

def recvInvite(inviter : str) :
    global inviterName, inviteDenied
    for label in playerLabels :
        if label.cget("text") == inviter :
            label.configure(text=label.cget("text")+" wants to battle!", text_color="yellow")
            inviterName = inviter
            inviteDenied = False
            break
#endregion

#region Battle

#region Pokemon
with open(f"{pokMetaLoc}pokemonMetaData.txt", "r") as file :
    pokemon = file.readlines()
for i in range(len(pokemon)) :
    pokemon[i] = pokemon[i].replace("\n", "")
for i in range(len(pokemon)) :
    pokemon[i] = pokemon[i].split(",")


pikachu = c_pokemon.Pokemon(pokemon[0][0], int(pokemon[0][1]), int(pokemon[0][2]), int(pokemon[0][3]), int(pokemon[0][4]))
charizard = c_pokemon.Pokemon(pokemon[1][0], int(pokemon[1][1]), int(pokemon[1][2]), int(pokemon[1][3]), int(pokemon[1][4]))
lucario = c_pokemon.Pokemon(pokemon[2][0], int(pokemon[2][1]), int(pokemon[2][2]), int(pokemon[2][3]), int(pokemon[2][4]))
mewtwo = c_pokemon.Pokemon(pokemon[3][0], int(pokemon[3][1]), int(pokemon[3][2]), int(pokemon[3][3]), int(pokemon[3][4]))
suicune = c_pokemon.Pokemon(pokemon[4][0], int(pokemon[4][1]), int(pokemon[4][2]), int(pokemon[4][3]), int(pokemon[4][4]))
rayquaza = c_pokemon.Pokemon(pokemon[5][0], int(pokemon[5][1]), int(pokemon[5][2]), int(pokemon[5][3]), int(pokemon[5][4]))

frame_PokemonChoice = customtkinter.CTkFrame(master=window, width=window._current_width-20, height=window._current_height-20)

image_Pikachu = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Pikachu.png"), size=(270,250))
image_Charizard = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Charizard.png"), size=(300,230))
image_Lucario = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Lucario.png"), size=(160, 280))
image_Mewtwo = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Mewtwo.png"), size=(250, 280))
image_Suicune = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Suicune.png"), size=(290, 260))
image_Rayquaza = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Rayquaza.png"), size=(250, 280))

button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, text="", image=image_Pikachu, width=430, height=400, fg_color="#222222", hover=False)
label_Name = customtkinter.CTkLabel(master=frame_PokemonChoice, text=pikachu.get_nom(), font=(None, 25))
label_Pv = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Pv : "+str(pikachu.get_pv()), font=(None, 23))
label_Attaque = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Attaque : "+str(pikachu.get_attaque()), font=(None, 23))
label_Defense = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Defense : "+str(pikachu.get_defense()), font=(None, 23))
label_Level = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Level : "+str(pikachu.get_niveau())+" / 100", font=(None, 23))
#endregion

def battle() :

    frame_LobbyFrame.place(relx=10)

    frame_PokemonChoice.place(relx=.5, rely=.5, anchor=CENTER)
    label_PokemonChoice = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Choose a Pokemon", font=(None, 28))
    label_PokemonChoice.place(relx=.5, rely=.1, anchor=CENTER)

    optionMenu_Pokemon.place(relx=.5, rely=.18, anchor=CENTER)

    button_PokemonImage1.place(relx=.3, rely=.5, anchor=CENTER)
    label_Name.place(relx=.6, rely=.37, anchor=CENTER)
    label_Pv.place(relx=.6, rely=.44, anchor=CENTER)
    label_Attaque.place(relx=.6, rely=.51, anchor=CENTER)
    label_Defense.place(relx=.6, rely=.58, anchor=CENTER)
    label_Level.place(relx=.6, rely=.65, anchor=CENTER)

    button_Choose = customtkinter.CTkButton(master=frame_PokemonChoice, text="Play", font=(None, 23), height=30, width=100, command=waitForOpponent)
    button_Choose.place(relx=.5, rely=.9, anchor=CENTER)
    # choose your pokemon

chosenPokemon = pikachu

def choosePokemon(pokName) :
    # Display the appropriate pokemon info
    global button_PokemonImage1, chosenPokemon
    if pokName == "Pikachu" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=270, height=250, image=image_Pikachu, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.3, rely=.5, anchor=CENTER)
        label_Name.configure(text=pikachu.get_nom())
        label_Pv.configure(text="Pv : "+str(pikachu.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(pikachu.get_attaque()))
        label_Defense.configure(text="Defense : "+str(pikachu.get_defense()))
        label_Level.configure(text="Level : "+str(pikachu.get_niveau())+" / 100")
        chosenPokemon = pikachu
    elif pokName == "Charizard" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=300, height=230, image=image_Charizard, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.26, rely=.5, anchor=CENTER)
        label_Name.configure(text=charizard.get_nom())
        label_Pv.configure(text="Pv : "+str(charizard.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(charizard.get_attaque()))
        label_Defense.configure(text="Defense : "+str(charizard.get_defense()))
        label_Level.configure(text="Level : "+str(charizard.get_niveau())+" / 100")
        chosenPokemon = charizard
    elif pokName == "Lucario" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=150, height=280, image=image_Lucario, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.3, rely=.55, anchor=CENTER)
        label_Name.configure(text=lucario.get_nom())
        label_Pv.configure(text="Pv : "+str(lucario.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(lucario.get_attaque()))
        label_Defense.configure(text="Defense : "+str(lucario.get_defense()))
        label_Level.configure(text="Level : "+str(lucario.get_niveau())+" / 100")
        chosenPokemon = lucario
    elif pokName == "Mewtwo" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=260, height=280, image=image_Mewtwo, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.27, rely=.55, anchor=CENTER)
        label_Name.configure(text=mewtwo.get_nom())
        label_Pv.configure(text="Pv : "+str(mewtwo.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(mewtwo.get_attaque()))
        label_Defense.configure(text="Defense : "+str(mewtwo.get_defense()))
        label_Level.configure(text="Level : "+str(mewtwo.get_niveau())+" / 100")
        chosenPokemon = mewtwo
    elif pokName == "Suicune" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=290, height=260, image=image_Suicune, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.26, rely=.5, anchor=CENTER)
        label_Name.configure(text=suicune.get_nom())
        label_Pv.configure(text="Pv : "+str(suicune.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(suicune.get_attaque()))
        label_Defense.configure(text="Defense : "+str(suicune.get_defense()))
        label_Level.configure(text="Level : "+str(suicune.get_niveau())+" / 100")
        chosenPokemon = suicune
    elif pokName == "Rayquaza" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=250, height=280, image=image_Rayquaza, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.27, rely=.55, anchor=CENTER)
        label_Name.configure(text=rayquaza.get_nom())
        label_Pv.configure(text="Pv : "+str(rayquaza.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(rayquaza.get_attaque()))
        label_Defense.configure(text="Defense : "+str(rayquaza.get_defense()))
        label_Level.configure(text="Level : "+str(rayquaza.get_niveau())+" / 100")
        chosenPokemon = rayquaza

#region Battle for real


opponentLvl = None
opponentHP = None

def goToBattle() :
    label_Loading.destroy()
    progressBar.destroy()

    button_MyPokemon = customtkinter.CTkButton(master=frame_Battle, image=button_PokemonImage1.cget("image"), width=button_PokemonImage1._current_width-20, height=button_PokemonImage1._current_height-20, text="", hover=False, fg_color="#222222")
    button_MyPokemon.place(relx=.24, rely=.72, anchor=CENTER)

    global progressBar_HP, label_HP, progressBar_OppHP, label_OppHP, attack1Info, attack2Info, attack3Info, attack4Info, button_Attack1, button_Attack2, button_Attack3, button_Attack4, numAtt1, numAtt2, numAtt3, numAtt4, maxHp, textbox_Effects
    

    maxHp = tamer.get_pokemon().get_pv()

    frame_OppInfo = customtkinter.CTkFrame(master=frame_Battle, width=220, height=76, border_width=1, border_color="#483d41", fg_color="#2e3030")
    label_OppName = customtkinter.CTkLabel(master=frame_OppInfo, text=opponentPokemon, font=(None, 23), text_color="#fa1b2d")
    progressBar_OppHP = customtkinter.CTkProgressBar(master=frame_OppInfo, width=200, height=13, progress_color="green")
    label_OppHP = customtkinter.CTkLabel(master=frame_OppInfo, text=f"{opponentHP}/{opponentHP}", font=(None, 13), text_color="green")
    label_OppLvl = customtkinter.CTkLabel(master=frame_OppInfo, text=f"Level:{opponentLvl}", font=(None, 13), text_color="#f62681")
    progressBar_OppHP.set(1)
    frame_OppInfo.place(relx=.74, rely=.7, anchor=CENTER)
    label_OppName.place(relx=.27, rely=.2, anchor=CENTER)
    progressBar_OppHP.place(relx=.5, rely=.5, anchor=CENTER)
    label_OppHP.place(relx=.14, rely=.8, anchor=CENTER)
    label_OppLvl.place(relx=.6, rely=.8, anchor=CENTER)

    if opponentPokemon == "Pikachu" :
        button_OtherPokemon = customtkinter.CTkButton(master=frame_Battle, image=image_Pikachu, width=220, height=200, hover=False, fg_color="#222222", text="")
        button_OtherPokemon.place(relx=.8, rely=.3, anchor=CENTER)
    elif opponentPokemon == "Charizard" :
        button_OtherPokemon = customtkinter.CTkButton(master=frame_Battle, image=image_Charizard, width=250, height=180, hover=False, fg_color="#222222", text="")
        button_OtherPokemon.place(relx=.8, rely=.3, anchor=CENTER)
    elif opponentPokemon == "Lucario" :
        button_OtherPokemon = customtkinter.CTkButton(master=frame_Battle, image=image_Lucario, width=110, height=230, hover=False, fg_color="#222222", text="")
        button_OtherPokemon.place(relx=.85, rely=.3, anchor=CENTER)
    elif opponentPokemon == "Mewtwo" :
        button_OtherPokemon = customtkinter.CTkButton(master=frame_Battle, image=image_Mewtwo, width=200, height=230, hover=False, fg_color="#222222", text="")
        button_OtherPokemon.place(relx=.8, rely=.3, anchor=CENTER)
    elif opponentPokemon == "Suicune" :
        button_OtherPokemon = customtkinter.CTkButton(master=frame_Battle, image=image_Suicune, width=240, height=210, hover=False, fg_color="#222222", text="")
        button_OtherPokemon.place(relx=.75, rely=.3, anchor=CENTER)
    elif opponentPokemon == "Rayquaza" :
        button_OtherPokemon = customtkinter.CTkButton(master=frame_Battle, image=image_Rayquaza, width=200, height=230, hover=False, fg_color="#222222", text="")
        button_OtherPokemon.place(relx=.8, rely=.3, anchor=CENTER)

    allAtt = None
    attack1Info = None
    attack2Info = None
    attack3Info = None
    attack4Info = None

    with open(f"{pokMetaLoc}SpecialAtt.txt", "r") as file :
        allAtt = file.readlines()

    for line_Num in range(len(allAtt)) :
        if tamer.get_nom_pokemon() in allAtt[line_Num] :
            attack1Info = allAtt[line_Num+1]
            attack1Info = attack1Info.replace("\n", "")
            attack1Info = attack1Info.split(",")
            attack2Info = allAtt[line_Num+2]
            attack2Info = attack2Info.replace("\n", "")
            attack2Info = attack2Info.split(",")
            attack3Info = allAtt[line_Num+3]
            attack3Info = attack3Info.replace("\n", "")
            attack3Info = attack3Info.split(",")
            attack4Info = allAtt[randint(1, 3)]
            attack4Info = attack4Info.replace("\n", "")
            attack4Info = attack4Info.split(",")
            break

    numAtt1 = int(attack1Info[2])
    numAtt2 = int(attack2Info[2])
    numAtt3 = int(attack3Info[2])
    numAtt4 = int(attack4Info[2])

    frame_Info = customtkinter.CTkFrame(master=frame_Battle, width=220, height=76, border_width=1, border_color="#483d41", fg_color="#2e3030")
    label_Name = customtkinter.CTkLabel(master=frame_Info, text=tamer.get_nom_pokemon(), font=(None, 23), text_color="white")
    progressBar_HP = customtkinter.CTkProgressBar(master=frame_Info, width=200, height=13, progress_color="green")
    label_HP = customtkinter.CTkLabel(master=frame_Info, text=f"{str(tamer.get_pokemon().get_pv())}/{str(tamer.get_pokemon().get_pv())}", font=(None, 13), text_color="green")
    label_Lvl = customtkinter.CTkLabel(master=frame_Info, text=f"Level:{str(tamer.get_pokemon().get_niveau())}", font=(None, 13), text_color="#f62681")
    progressBar_HP.set(1)
    frame_Info.place(relx=.2, rely=.3, anchor=CENTER)
    label_Name.place(relx=.27, rely=.2, anchor=CENTER)
    progressBar_HP.place(relx=.5, rely=.5, anchor=CENTER)
    label_HP.place(relx=.14, rely=.8, anchor=CENTER)
    label_Lvl.place(relx=.6, rely=.8, anchor=CENTER)

    frame_Attacks = customtkinter.CTkFrame(master=frame_Battle, width=300, height=80, border_width=1, border_color="#00b3e5", fg_color="#282d3f")
    button_Attack1 = customtkinter.CTkButton(master=frame_Attacks, command=attack1, text=f"{attack1Info[0]} {attack1Info[2]}/{attack1Info[2]}", border_width=1, border_color="black", height=35, font=(None,15))
    button_Attack2 = customtkinter.CTkButton(master=frame_Attacks, command=attack2, text=f"{attack2Info[0]} {attack2Info[2]}/{attack2Info[2]}", border_width=1, border_color="black", height=35, font=(None,15))
    button_Attack3 = customtkinter.CTkButton(master=frame_Attacks, command=attack3, text=f"{attack3Info[0]} {attack3Info[2]}/{attack3Info[2]}", border_width=1, border_color="black", height=35, font=(None,15))
    button_Attack4 = customtkinter.CTkButton(master=frame_Attacks, command=attack4, text_color="yellow", text=f"{attack4Info[0]} {attack4Info[2]}/{attack4Info[2]}", border_width=1, border_color="black", height=35, font=(None,15))
    frame_Attacks.place(relx=.7, rely=.9, anchor=CENTER)
    button_Attack1.place(relx=.25, rely=.26, anchor=CENTER)
    button_Attack2.place(relx=.75, rely=.26, anchor=CENTER)
    button_Attack3.place(relx=.25, rely=.74, anchor=CENTER)
    button_Attack4.place(relx=.75, rely=.74, anchor=CENTER)
    
    textbox_Effects = customtkinter.CTkTextbox(master=frame_Battle, width=230, height=70, border_color="black", border_width=1, text_color="white")
    textbox_Effects.place(relx=.2, rely=.1, anchor=CENTER)

damageModifier = 0
damageLess = 0

def attack1() :
    button_Attack1.configure(state="disabled")
    button_Attack2.configure(state="disabled")
    button_Attack3.configure(state="disabled")
    button_Attack4.configure(state="disabled")
    global numAtt1, damageLess, damageModifier
    numAtt1 -= 1
    button_Attack1.configure(text=f"{attack1Info[0]} {numAtt1}/{attack1Info[2]}")

    damage = int(attack1Info[1]) * (tamer.get_pokemon().get_attaque() * .01)/3

    if damageModifier > 0 :
        damage -= damageLess
        damageModifier -= 1

    if attack1Info[3] != "n" and attack1Info[5] != "n" :
        effectOnOther = attack1Info[3]
        effectOnOther = effectOnOther.split(":")
        effectOnOther[1] = int(effectOnOther[1])
        effectOnOther[1] *= (tamer.get_pokemon().get_attaque() * .01)
        effectOnOther[1] -= .5
        roundsForEffect = attack1Info[5]
        client.send(f"$attack:{username},{damage},{effectOnOther[0]}:{effectOnOther[1]},{roundsForEffect},{attack1Info[0]}".encode(FORMAT))
    else :
        client.send(f"$attack:{username},{damage},n,n,{attack1Info[0]}".encode(FORMAT))

    textbox_Effects.insert("0.0", f"{tamer.get_nom_pokemon()}(you) used {attack1Info[0]} for {int(damage)} damage!\n")

    if attack1Info[0] == "Future Sight" :
        dmgName = attack1Info[4].split(":")
        tamer.get_pokemon().set_degats(int(int(dmgName[1]) * (tamer.get_pokemon().get_attaque() * .01)/3)+1)
        label_HP.configure(text=f"{str(tamer.get_pokemon().get_pv())}/{maxHp}")
        progressBar_HP.set(tamer.get_pokemon().get_pv() / maxHp)
        client.send(f"$health:{tamer.get_pokemon().get_pv()},{username}".encode(FORMAT))
        textbox_Effects.insert("0.0", f"{dmgName[0]} -> {int(int(dmgName[1]) * (tamer.get_pokemon().get_attaque() * .01)/3)}\n")
        checkForDeath()
    checkForWin()

def attack2() :
    button_Attack1.configure(state="disabled")
    button_Attack2.configure(state="disabled")
    button_Attack3.configure(state="disabled")
    button_Attack4.configure(state="disabled")
    global numAtt2, damageLess, damageModifier
    numAtt2 -= 1
    button_Attack2.configure(text=f"{attack2Info[0]} {numAtt2}/{attack2Info[2]}")
    damage = int(attack2Info[1]) * (tamer.get_pokemon().get_attaque() * .01)/3

    if damageModifier > 0 :
        damage -= damageLess
        damageModifier -= 1
    
    if attack2Info[3] != "n" and attack2Info[5] != "n" :
        effectOnOther = attack2Info[3]
        effectOnOther = effectOnOther.split(":")
        effectOnOther[1] = int(effectOnOther[1])
        effectOnOther[1] *= (tamer.get_pokemon().get_attaque() * .01)
        effectOnOther[1] -= .5
        roundsForEffect = attack2Info[5]
        client.send(f"$attack:{username},{damage},{effectOnOther[0]}:{effectOnOther[1]},{roundsForEffect},{attack2Info[0]}".encode(FORMAT))
    else :
        client.send(f"$attack:{username},{damage},n,n,{attack2Info[0]}".encode(FORMAT))

    textbox_Effects.insert("0.0", f"{tamer.get_nom_pokemon()}(you) used {attack2Info[0]} for {int(damage)} damage!\n")

    if attack2Info[0] == "Outrage" :
        damageLess = attack2Info[4].split(":")
        damageLess = int(damageLess[1])
        damageModifier = int(attack2Info[5])
        damageLess *= int((tamer.get_pokemon().get_attaque() * .01)/5)
        damageLess += 2
        textbox_Effects.insert("0.0", f"{tamer.get_nom_pokemon()} will deal {damageLess} less damage for the next {damageModifier} rounds\n")
    checkForWin()

def attack3() :
    button_Attack1.configure(state="disabled")
    button_Attack2.configure(state="disabled")
    button_Attack3.configure(state="disabled")
    button_Attack4.configure(state="disabled")
    global numAtt3, damageLess, damageModifier
    numAtt3 -= 1
    button_Attack3.configure(text=f"{attack3Info[0]} {numAtt3}/{attack3Info[2]}")

    damage = int(attack3Info[1]) * (tamer.get_pokemon().get_attaque() * .01)/3

    if damageModifier > 0 :
        damage -= damageLess
        damageModifier -= 1

    if attack3Info[3] != "n" and attack3Info[5] != "n" :
        effectOnOther = attack3Info[3]
        effectOnOther = effectOnOther.split(":")
        effectOnOther[1] = int(effectOnOther[1])
        effectOnOther[1] *= (tamer.get_pokemon().get_attaque() * .01)
        effectOnOther[1] -= .5
        roundsForEffect = attack3Info[5]
        client.send(f"$attack:{username},{damage},{effectOnOther[0]}:{effectOnOther[1]},{roundsForEffect},{attack3Info[0]}".encode(FORMAT))
    else :
        client.send(f"$attack:{username},{damage},n,n,{attack3Info[0]}".encode(FORMAT))

    textbox_Effects.insert("0.0", f"{tamer.get_nom_pokemon()}(you) used {attack3Info[0]} for {int(damage)} damage!\n")
    checkForWin()

def attack4() :
    button_Attack1.configure(state="disabled")
    button_Attack2.configure(state="disabled")
    button_Attack3.configure(state="disabled")
    button_Attack4.configure(state="disabled")
    global numAtt4, damageLess, damageModifier
    numAtt4 -= 1
    button_Attack4.configure(text=f"{attack4Info[0]} {numAtt4}/{attack4Info[2]}")

    damage = int(attack4Info[1]) * (tamer.get_pokemon().get_attaque() * .01)/3

    if damageModifier > 0 :
        damage -= damageLess
        damageModifier -= 1

    if attack4Info[3] != "n" and attack4Info[5] != "n" :
        effectOnOther = attack4Info[3]
        effectOnOther = effectOnOther.split(":")
        effectOnOther[1] = int(effectOnOther[1])
        effectOnOther[1] *= (tamer.get_pokemon().get_attaque() * .01)
        effectOnOther[1] -= .5
        roundsForEffect = attack4Info[5]
        client.send(f"$attack:{username},{damage},{effectOnOther[0]}:{effectOnOther[1]},{roundsForEffect},{attack4Info[0]}".encode(FORMAT))
    else :
        client.send(f"$attack:{username},{damage},n,n,{attack4Info[0]}".encode(FORMAT))

    textbox_Effects.insert("0.0", f"{tamer.get_nom_pokemon()}(you) used {attack4Info[0]} for {int(damage)} damage!\n")

    if attack4Info[0] == "Extincteur" :
        if "Fire" in effectNames :
            popThisEffect = effectNames.index("Fire")
            effectNames.pop(popThisEffect)
            roundsForEffectLeft.pop(popThisEffect)
            damagePerRound.pop(popThisEffect)
    elif attack4Info[0] == "Lobotomisation" :
        dmgName = attack4Info[4].split(":")
        tamer.get_pokemon().set_degats(int(int(dmgName[1]) * (tamer.get_pokemon().get_attaque() * .01)/3))
        label_HP.configure(text=f"{str(tamer.get_pokemon().get_pv())}/{maxHp}")
        progressBar_HP.set(tamer.get_pokemon().get_pv() / maxHp)
        client.send(f"$health:{tamer.get_pokemon().get_pv()},{username}".encode(FORMAT))
        textbox_Effects.insert("0.0", f"{dmgName[0]} -> {dmgName[1]}\n")
        checkForDeath()
    
    checkForWin()

def takeDamage(message, effect : bool) :
    global numAtt1, numAtt2, numAtt3, numAtt4

    if numAtt1 >= 1 :
        button_Attack1.configure(state="normal")
    if numAtt2 >= 1 :
        button_Attack2.configure(state="normal")
    if numAtt3 >= 1 :
        button_Attack3.configure(state="normal")
    if numAtt4 >= 1 :
        button_Attack4.configure(state="normal")
    damage = int(float(message[1]))
    damage -= int(tamer.get_pokemon().get_defense() * .01)
    tamer.get_pokemon().set_degats(damage)
    label_HP.configure(text=f"{str(tamer.get_pokemon().get_pv())}/{maxHp}")
    progressBar_HP.set(tamer.get_pokemon().get_pv() / maxHp)
    client.send(f"$health:{tamer.get_pokemon().get_pv()},{username}".encode(FORMAT))
    textbox_Effects.insert("0.0", f"{opponentPokemon} used {message[4]} for {damage} damage!\n")

    if effect :
        print(message)
        message[2] = message[2].split(":")
        print(message[2])
        roundsForEffectLeft.append(int(message[3]))
        print(roundsForEffectLeft)
        message[2][1] = int(float(message[2][1]))
        if message[2][1] < 1 :
            message[2][1] = 1
        damagePerRound.append(message[2][1])
        print(damagePerRound)
        effectNames.append(message[2][0])
        print(effectNames)

    for effect in range(len(roundsForEffectLeft)) :
        roundsForEffectLeft[effect] -= 1
        dmg = damagePerRound[effect]
        dmg -= int(tamer.get_pokemon().get_defense() * .01) 
        tamer.get_pokemon().set_degats(dmg)
        progressBar_HP.set(tamer.get_pokemon().get_pv() / maxHp)
        client.send(f"$health:{tamer.get_pokemon().get_pv()},{username}".encode(FORMAT))
        textbox_Effects.insert("0.0", f"{effectNames[effect]} -> {dmg}\n")

        if roundsForEffectLeft[effect] == 0 :
            roundsForEffectLeft.pop(effect)
            damagePerRound.pop(effect)
            effectNames.pop(effect)

    checkForDeath()

def checkForDeath() :
    if tamer.get_pokemon().get_pv() == 0 :
        client.send(f"$death:{username}".encode(FORMAT))
        lossFrame()

def checkForWin() :
    if progressBar_OppHP.get() == 0 :
        winFrame()
        
def lossFrame() :
    frame_Battle.place(relx=30)

    global frame_GameOver
    frame_GameOver = customtkinter.CTkFrame(master=window, width=window._current_width-20, height=window._current_height-20)
    label_GameOver = customtkinter.CTkLabel(master=frame_GameOver, text="Game Over!", font=(None, 30))
    label_Loss = customtkinter.CTkLabel(master=frame_GameOver, text="You Lose", font=(None, 23), text_color="orange")
    label_XP = customtkinter.CTkLabel(master=frame_GameOver, text=f"{tamer.get_nom_pokemon()} earned 0 levels, better luck next time", font=(None, 20))
    button_Continue = customtkinter.CTkButton(master=frame_GameOver, text="Continue", command=backToLobby)
    frame_GameOver.place(relx=.5, rely=.5, anchor=CENTER)
    label_GameOver.place(relx=.5, rely=.2, anchor=CENTER)
    label_Loss.place(relx=.5, rely=.4, anchor=CENTER)
    label_XP.place(relx=.5, rely=.6, anchor=CENTER)
    button_Continue.place(relx=.5, rely=.8, anchor=CENTER)

def winFrame() :
    frame_Battle.place(relx=30)

    global frame_GameOver
    frame_GameOver = customtkinter.CTkFrame(master=window, width=window._current_width-20, height=window._current_height-20)
    label_GameOver = customtkinter.CTkLabel(master=frame_GameOver, text="Game Over!", font=(None, 30))
    label_Win = customtkinter.CTkLabel(master=frame_GameOver, text="You Win!", font=(None, 23), text_color="green")
    if tamer.get_pokemon().get_niveau() != 100 :
        label_XP = customtkinter.CTkLabel(master=frame_GameOver, text=f"{tamer.get_nom_pokemon()} earned 1 level, well done!", font=(None, 20))
    else :
        label_XP = customtkinter.CTkLabel(master=frame_GameOver, text=f"{tamer.get_nom_pokemon()} has already reached the maximum level, but still, well done!", font=(None, 20))

    content = None

    with open(f"{pokMetaLoc}pokemonMetaData.txt", "r") as file :
        content = file.readlines()

    print(content)
    print(tamer.get_nom_pokemon())

    for i in range(len(content)) :
        print(content[i])
        if f"{tamer.get_nom_pokemon()}" in content[i] :
            content[i] = content[i].split(",")
            content[i][-1] = str(int(content[i][-1])+1)
            thingToChange = ""
            for item in content[i] :
                thingToChange += "," + item
            thingToChange = thingToChange[1:]
            thingToChange += "\n"
            content[i] = thingToChange
            break

    with open(f"{pokMetaLoc}pokemonMetaData.txt", "w") as file :
        file.writelines(content)

    button_Continue = customtkinter.CTkButton(master=frame_GameOver, text="Continue", command=backToLobby)
    frame_GameOver.place(relx=.5, rely=.5, anchor=CENTER)
    label_GameOver.place(relx=.5, rely=.2, anchor=CENTER)
    label_Win.place(relx=.5, rely=.4, anchor=CENTER)
    label_XP.place(relx=.5, rely=.6, anchor=CENTER)
    button_Continue.place(relx=.5, rely=.8, anchor=CENTER)

def backToLobby() :
    # set EVERYTHING back to how it was at lobby level
    global chosenPlayer, chosenPokemon, opponentLvl, opponentHP, damageLess, damageModifier, roundsForEffectLeft, damagePerRound,\
           effectNames, playerLabels, optionMenu_Players, poppedPlayer, inviteDenied, inviterName, tamer, opponentIsReady, opponentPokemon
    damageModifier = 0
    damageLess = 0
    opponentLvl = None
    opponentHP = None  
    roundsForEffectLeft = []
    damagePerRound = []
    effectNames = []
    playerLabels = []
    chosenPlayer = None
    optionMenu_Players = None
    poppedPlayer = None
    inviteDenied = True
    inviterName = None
    optionMenu_Pokemon.set("Pikachu")
    opponentPokemon = None
    opponentIsReady = False
    for i in range(len(pokemon)) :
        if f"{tamer.get_nom_pokemon()}" in pokemon[i][0] :
            tamer.get_pokemon().set_pv(pokemon[i][1])
            break
    chosenPokemon = pikachu
    tamer = None
    choosePokemon("Pikachu")
    
    frame_Battle.destroy()
    frame_GameOver.destroy()
    displayPlayers()
    lobby()

def oppHealthVis(health) :
    label_OppHP.configure(text=f"{health}/{opponentHP}")
    progressBar_OppHP.set(int(health) / opponentHP)

opponentPokemon = None
opponentIsReady = False
tamer = None

def waitForOpponent() :
    global tamer, opponentIsReady, frame_Battle, label_Loading, progressBar, frame_Battle
    frame_Battle = customtkinter.CTkFrame(master=window, width=window._current_width-20, height=window._current_height-20)
    label_Loading = customtkinter.CTkLabel(master=frame_Battle, text="Waiting for opponent", text_color="white", font=(None, 31))
    progressBar = customtkinter.CTkProgressBar(master=frame_Battle, width=300, height=15, progress_color="yellow", mode="indeterminate", indeterminate_speed=1)
    tamer = c_dresseur.Dresseur(username, chosenPokemon)
    client.send(f"!ready:{tamer.get_nom_pokemon()},{tamer.get_nom_dresseur()},{tamer.get_pokemon().get_niveau()},{tamer.get_pokemon().get_pv()}".encode(FORMAT))
    frame_PokemonChoice.place(relx=-10)
    frame_Battle.place(relx=.5, rely=.5, anchor=CENTER)
    label_Loading.place(relx=.5, rely=.4, anchor=CENTER)
    progressBar.place(relx=.5, rely=.5, anchor=CENTER)
    progressBar.start()
    
    if opponentIsReady : goToBattle()

#endregion

pokemonNames = []
for i in pokemon :
    pokemonNames.append(i[0])
optionMenu_Pokemon = customtkinter.CTkOptionMenu(master=frame_PokemonChoice, values=pokemonNames, command=choosePokemon)
#endregion

#region Threads
receive_Process = threading.Thread(target=client_receive)
receive_Process.daemon = True
#endregion

window.mainloop()
