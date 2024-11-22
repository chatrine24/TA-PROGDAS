import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import json
from PIL import Image, ImageTk


class MoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moodiary")
        self.root.geometry("800x700")

        # Memuat gambar latar belakang
        self.bg_image = Image.open("background.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Membuat label dengan gambar sebagai background
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Warna mood
        self.mood_colors = {
            "happy": "#FFD700",
            "good": "#FFC1CC",
            "neutral": "#F2DDDC",
            "sad": "#B3E5FC",
            "depressed": "#E3D8F1"
        }

        # Header
        tk.Label(
            root,
            text="MOODIARY",
            font=("Aptos", 24, "bold"),
            bg="#F04770"
        ).pack(pady=10)

        # Kalender
        self.calendar = Calendar(
            root,
            selectmode="day",
            date_pattern="yyyy-MM-dd",
            background="black",
            foreground="white",
            showweeknumbers=False
        )
        self.calendar.pack(pady=20)
        self.calendar.bind("<<CalendarSelected>>", self.display_note)

        # Pilihan Mood
        tk.Label(
            root,
            text="How are you feeling",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF"
        ).pack(pady=15)

        self.mood_var = tk.StringVar()
        self.mood_var.set("")

        # Tombol mood
        self.mood_buttons = {}
        mood_frame = tk.Frame(root, bg="#FFC1CC")
        mood_frame.pack(pady=0)
        for mood, color in self.mood_colors.items():
            btn = tk.Radiobutton(
                mood_frame,
                text=mood.capitalize(),
                variable=self.mood_var,
                value=mood,
                indicatoron=0,
                width=10,
                font=("Baloo 2", 15, "bold"),
                bg=color,
                fg="black",
                activebackground=color,
                command=self.update_button_colors
            )
            btn.pack(side="left", padx=5)
            self.mood_buttons[mood] = btn
            self.add_hover_effect(btn, color)

        # Notes
        tk.Label(
            root,
            text="Write about it",
            font=("Nunito", 14, "bold"),
            bg="#FFFFFF"
        ).pack(pady=5)

        self.note_entry = tk.Entry(
            root,
            font=("Arial", 12),
            width=50
        )
        self.note_entry.pack(pady=5)

        # Tombol Simpan
        save_button = tk.Button(
            root,
            text="Save",
            command=self.save_mood,
            bg="#FFFFFF",
            fg="Black",
            font=("Nunito", 12, "bold"),
            width=20
        )
        save_button.pack(pady=10)
        self.add_hover_effect(save_button, "#FFFFFF")

        # Label untuk menampilkan note
        tk.Label(
            root,
            text="Notes:",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF"
        ).pack(pady=5)

        self.saved_note_label = tk.Label(
            root,
            text="",
            font=("Arial", 12),
            bg="#FFFFFF",
            fg="black",
            wraplength=700
        )
        self.saved_note_label.pack(pady=5)

        # Data untuk menyimpan mood dan notes
        self.data = {}
        self.load_data()
        self.update_calendar_colors()

    def add_hover_effect(self, widget, original_color):
        def on_enter(event):
            widget.config(bg="#FFB6C1")

        def on_leave(event):
            widget.config(bg=original_color)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def update_button_colors(self):
        for mood, button in self.mood_buttons.items():
            color = self.mood_colors[mood]
            if self.mood_var.get() == mood:
                button.config(bg=color)
            else:
                button.config(bg=color)

    def save_mood(self):
        selected_date = self.calendar.get_date()
        selected_mood = self.mood_var.get()
        note_text = self.note_entry.get()

        if not selected_mood:
            messagebox.showwarning("Warning", "Please select a mood!")
            return

        self.data[selected_date] = {"mood": selected_mood, "note": note_text}
        self.update_calendar_colors()
        self.save_data()
        messagebox.showinfo("Success", f"Mood for {selected_date} saved with your note!")

        self.note_entry.delete(0, tk.END)
        self.mood_var.set("")
        self.update_button_colors()

    def update_calendar_colors(self):
        self.calendar.calevent_remove("all")
        for date_str, entry in self.data.items():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                color = self.mood_colors.get(entry["mood"], "#FFFFFF")
                tag_name = f"mood_{date_str}"
                self.calendar.calevent_create(date_obj, entry["mood"].capitalize(), tag_name)
                self.calendar.tag_config(tag_name, background=color, foreground="black")
            except Exception as e:
                print(f"Error processing date {date_str}: {e}")

    def display_note(self, event=None):
        selected_date = self.calendar.get_date()
        if selected_date in self.data:
            saved_note = self.data[selected_date].get("note", "")
            mood = self.data[selected_date].get("mood", "No Mood")
            self.saved_note_label.config(
                text=f"Mood: {mood.capitalize()}\nNote: {saved_note}"
            )
        else:
            self.saved_note_label.config(text="No data saved for this date.")

    def save_data(self, filename="mood_data.json"):
        with open(filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def load_data(self, filename="mood_data.json"):
        try:
            with open(filename, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

class LoginPage:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Login")
        self.root.geometry("400x300")

        tk.Label(
            root,
            text="Login to Moodiary",
            font=("Arial", 18, "bold")
        ).pack(pady=0)
        
        tk.Label(
            root,
            text="Ini rahasia, login dulu!",
            font=("Arial", 10 )
        ).pack(pady=20)

        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(
            root,
            text="Login",
            command=self.validate_login,
            bg="pink",
            fg="black"
        ).pack(pady=20)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Dummy login credentials
        if username == "Chatrine" and password == "nailong":
            self.root.destroy()  # Close login window
            self.on_success()
        else:
            messagebox.showerror("Error", "Invalid")


if __name__ == "__main__":
    def open_mood_tracker():
        root = tk.Tk()
        app = MoodTrackerApp(root)
        root.mainloop()

    login_root = tk.Tk()
    login_page = LoginPage(login_root, on_success=open_mood_tracker)
    login_root.mainloop()
    