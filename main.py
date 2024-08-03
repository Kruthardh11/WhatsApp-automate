import customtkinter as ctk
import pywhatkit
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WhatsAppSenderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WhatsApp Message Scheduler")
        self.geometry(f"{600}x{450}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="WhatsApp\nScheduler", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Main content
        self.entry_recipient = ctk.CTkEntry(self, placeholder_text="Phone number or Group ID")
        self.entry_recipient.grid(row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.entry_hour = ctk.CTkEntry(self, placeholder_text="Hour (24-hour format)")
        self.entry_hour.grid(row=1, column=1, padx=(20, 10), pady=(0, 20), sticky="nsew")

        self.entry_minute = ctk.CTkEntry(self, placeholder_text="Minute")
        self.entry_minute.grid(row=1, column=2, padx=(10, 20), pady=(0, 20), sticky="nsew")

        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")

        self.main_button = ctk.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Schedule Message", command=self.schedule_message)
        self.main_button.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def schedule_message(self):
        recipient = self.entry_recipient.get()
        message = self.textbox.get("1.0", "end-1c").strip()
        hour = self.entry_hour.get()
        minute = self.entry_minute.get()
        
        if not recipient or not message or not hour or not minute:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            hour = int(hour)
            minute = int(minute)
            
            if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                raise ValueError("Invalid time format")

            if recipient.startswith("+"):
                # Send to phone number
                pywhatkit.sendwhatmsg(recipient, message, hour, minute, 15, True, 8)
            else:
                # Send to group
                pywhatkit.sendwhatmsg_to_group(recipient, message, hour, minute, 15, True, 8)
            
            messagebox.showinfo("Success", f"Message scheduled for {hour:02d}:{minute:02d}")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use 24-hour format for hour (0-23) and minutes (0-59).")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = WhatsAppSenderApp()
    app.mainloop()