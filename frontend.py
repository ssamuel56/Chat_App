import customtkinter
import tkinter
from networking import *

customtkinter.set_appearance_mode("dark")

# TODO Need to add function here to keep track of conversations. 
# Possibly keep connection info in JSON file and use SQLlite for message storage
# Class to create the conversation_selection_frames
class ConversationFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        self.conversation_name_label = customtkinter.CTkLabel(master=self, fg_color="transparent", font=("Monospace",20))
        self.conversation_name_label.grid(column=1, columnspan=1, row=2, sticky="")


# Class to create the message selection frame
# Possibly call function in here that creates all the current messages
class ConversationSelectionContainer(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # self.pack(fill = BOTH, expand = True)
        # add widgets onto the frame, for example:
        # self.label = customtkinter.CTkLabel(self)
        # self.label.grid(row=0, column=1, padx=20)
        for x in range(2):
            self.conversation_frame = ConversationFrame(master=self)
            self.conversation_frame.pack(fill ="x", expand = False, pady=(0, 10))
            self.conversation_frame.configure(border_width=5, border_color="#3C375C", fg_color="#3c375c")


# Class to create the Message content/main area of the app
class MessagingFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=0)
        #self.grid_rowconfigure(3, weight=3)
        self.grid_columnconfigure(0,weight=1)
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)
        #self.grid_columnconfigure(3, weight=1)

        self.message_title_label = customtkinter.CTkLabel(master=self, text="Hello", font=("Source Code Pro", 20))
        self.message_title_label.grid(row=0, column = 0, padx=5, pady=5, sticky="new")

        self.message_boxes_frame = customtkinter.CTkFrame(master=self, 
                                                          # fg_color="transparent"
                                                          )
        self.message_boxes_frame.grid(row=1, column=0, pady=0, sticky="nsew")

        self.typed_message_textbox = customtkinter.CTkTextbox(master=self, height=60)
        self.typed_message_textbox.grid(row=2, column=0, padx=5, pady=5, sticky="sew")

    # Used to load in new chat bubbles as new messages appear
    def load_new_message(self, msg):
        self.new_message_bubble = customtkinter.CTkLabel(master=self.message_boxes_frame, text=msg)
        self.new_message_bubble.pack(fill="x", expand=False, pady=5)


class App(customtkinter.CTk):
    def __init__(self, websocket):
        super().__init__()
        self.geometry("900x600")
        self.title("Geek Chat")
        self.websocket = websocket

        # Configure a grid structure for the application 
        # Goin to use grid for setting all content except for the actual messages and the selection frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=3)
        # self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=3)

        #Add message selection to app
        self.conversation_selection = ConversationSelectionContainer(master=self)
        self.conversation_selection.grid(row=0, rowspan=2, column=0, padx=(20,0), pady=20, sticky="nsew")

        # Add messages/ main content to app
        self.messaging_frame = MessagingFrame(master=self)
        self.messaging_frame.grid(row=0, rowspan=2, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

        # add widgets to app
        # self.button = customtkinter.CTkButton(self, command=self.button_click)
        # self.button.grid(row=0, column=4, padx=20, pady=10)

    # This method checks the message queue every second to see if any new messages have arrived.
    # At that point it creates new chat messages for each one.
    # TODO This will need to be expanded into another method to allow for multiple conversations.
    def message_checker(self):
        while not self.websocket.message_queue.empty():
            print('You Hit Condition')
            self.messaging_frame.load_new_message(self.websocket.message_queue.get())
        self.after(1000, self.message_checker)


# Run main logic of app and also call our message update function.
# Must have the first call of .after here or will not run recurssively
server = WebSocketConnection()
server.start_as_thread()
app = App(server)
app.after(1000, app.message_checker())
app.mainloop()
