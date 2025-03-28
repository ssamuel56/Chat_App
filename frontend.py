import customtkinter
import tkinter


customtkinter.set_appearance_mode("dark")


# Class to create the message selection frame
# Possibly call function in here that creates all the current messages
class MessageSelectionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # self.pack(fill = BOTH, expand = True)
        # add widgets onto the frame, for example:
        # self.label = customtkinter.CTkLabel(self)
        # self.label.grid(row=0, column=1, padx=20)
        for x in range(200):
            self.message_select_button = customtkinter.CTkButton(master=self, text=f"test message {x}", border_width=5)
            self.message_select_button.pack(fill ="x", expand = True)


# Class to create the Message content/main area of the app
class MessageContentFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=3)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)
        # self.grid_rowconfigure(3, weight=1)
        # self.grid_columnconfigure(3, weight=1)

        self.typed_message_textbox = customtkinter.CTkTextbox(master=self, height=30)
        self.typed_message_textbox.grid(row=2, column=0, columnspan=3, padx=5, pady=(5), sticky="sew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Geek Chat")

        # Configure a grid structure for the application 
        # Goin to use grid for setting all content except for the actual messages and the selection frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=2)
        # self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=2)

        #Add message selection to app
        self.message_selection = MessageSelectionFrame(master=self)
        self.message_selection.grid(row=0, rowspan=2, column=0, padx=(20,0), pady=20, sticky="nsew")

        # Add messages/ main content to app
        self.message_content = MessageContentFrame(master=self)
        self.message_content.grid(row=0, rowspan=2, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

        # add widgets to app
        # self.button = customtkinter.CTkButton(self, command=self.button_click)
        # self.button.grid(row=0, column=4, padx=20, pady=10)

    # add methods to app
    def button_click(self):
        print("button click")


app = App()
app.mainloop()
