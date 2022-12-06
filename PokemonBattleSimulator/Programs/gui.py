from tkinter import *
import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

window = customtkinter.CTk()
window.geometry("700x500")
window.title("Pokemon Battle Simulator")
icon = PhotoImage(file='PokemonBattleSimulator\\Assets\\icon3.png')
window.iconphoto(True, icon)
window.resizable(False, False)

frame = customtkinter.CTkFrame(master=window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

#region Images 
background = customtkinter.CTkImage(light_image=Image.open("PokemonBattleSimulator\\Assets\\MainBackground.png"),
                                    size=(450,170))
bg = customtkinter.CTkButton(master=frame, 
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
    print("Play!")

def options() :
    print("Options!")

def quit() :
    exit()
#endregion

#region Labels
label_Title = customtkinter.CTkLabel(master=frame, 
                                     text="Pokemon Battle Simulator", 
                                     text_color="white", 
                                     font=("Roboto", 24))
label_Title.pack(pady=40, padx=10)
#endregion

#region Buttons
m_height = 34
m_width = 174
m_fontSize = 17

button_Play = customtkinter.CTkButton(master=frame, 
                                      text="Play",
                                      command=play,
                                      width=m_width,
                                      height=m_height,
                                      font=(None, m_fontSize))

button_Settings = customtkinter.CTkButton(master=frame, 
                                         text="Settings",
                                         command=options,
                                         width=m_width,
                                         height=m_height,
                                         font=(None, m_fontSize))

button_Quit = customtkinter.CTkButton(master=frame, 
                                      text="Quit",
                                      command=quit,
                                      width=m_width,
                                      height=m_height,
                                      font=(None, m_fontSize))

button_Play.place(relx=.5, rely=.65, anchor=CENTER)
button_Settings.place(relx=.5, rely=.73, anchor=CENTER)
button_Quit.place(relx=.5, rely=.81, anchor=CENTER)
#endregion

#region Tabs
#endregion

#region Frames

#endregion

window.mainloop()
