from tkinter import *
import customtkinter
import gui

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

presetServerNameWindow = customtkinter.CTk()
presetServerNameWindow.geometry("240x160")
presetServerNameWindow.title("Server Name")
presetServerNameWindow.resizable(False, False)
def acceptServerName() :
    gui.set_ServerName(entry_ServerName.get())
    presetServerNameWindow.quit()

label_AskServerName = customtkinter.CTkLabel(master=presetServerNameWindow,
                                             text="What would you like to\nname the server ?",
                                             font=(None, 16))
label_AskServerName.place(relx=.5, rely=.2, anchor=CENTER)  
entry_ServerName = customtkinter.CTkEntry(master=presetServerNameWindow,
                                          placeholder_text="20 characters maximum",
                                          width=170)
entry_ServerName.place(relx=.5, rely=.45, anchor=CENTER)  
button_ServerNameAccept = customtkinter.CTkButton(master=presetServerNameWindow,
                                                  text="Continue",
                                                  width=40,
                                                  height=30,
                                                  font=(None, 15),
                                                  command=acceptServerName)       
button_ServerNameAccept.place(relx=.5, rely=.7, anchor=CENTER)

def startDemandWindow() :
    presetServerNameWindow.mainloop()