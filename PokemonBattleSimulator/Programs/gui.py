from tkinter import PhotoImage
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

window = customtkinter.CTk()
window.geometry("700x500")
window.title("Pokemon Battle Simulator")
icon = PhotoImage(file='PokemonBattleSimulator\\Assets\\icon3.png')
window.iconphoto(True, icon)
window.resizable(False, False)

frame = customtkinter.CTkFrame(master=window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

#region Commands(Functions)
def play() :
    print("Play!")

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
button_Play = customtkinter.CTkButton(master=frame, 
                                      text="Play",
                                      command=play)
button_Play.pack(pady=150, padx=10)

button_Quit = customtkinter.CTkButton(master=frame, 
                                      text="Quit",
                                      command=quit)
button_Quit.pack(pady=0, padx=10)
#endregion

window.mainloop()