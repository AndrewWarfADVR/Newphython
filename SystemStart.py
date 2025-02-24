import os
import random
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import time


class FlashingImageApp:
    def __init__(self, root, alive_folder, not_alive_folder):
        self.root = root
        self.root.title("Flashing Image Game")
        self.root.configure(bg='#2C3E50')  # Dark Blue background
        self.root.geometry('600x650')  # Window size

        self.alive_folder = alive_folder
        self.not_alive_folder = not_alive_folder

        # Load images
        self.alive_images = [f for f in os.listdir(self.alive_folder) if
                             f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        self.not_alive_images = [f for f in os.listdir(self.not_alive_folder) if
                                 f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

        if not self.alive_images and not self.not_alive_images:
            raise ValueError("No images found in the provided folders!")

        # Timer variables
        self.game_duration = 600  # 10 minutes (600 seconds)
        self.start_time = time.time()

        # Timer display
        self.timer_label = Label(root, text="Time Left: 10:00", font=('Arial', 16, 'bold'), fg='#F1C40F', bg='#2C3E50')
        self.timer_label.pack(pady=10)

        # Image display
        self.image_label = Label(root, bg='#2C3E50')
        self.image_label.pack(pady=20)

        # Question Label
        self.label = Label(root, text="Is the image alive?", font=('Arial', 18, 'bold'), fg='#ECF0F1', bg='#2C3E50')
        self.label.pack(pady=20)

        # Yes & No Buttons
        self.yes_button = Button(root, text="Yes", font=('Arial', 14), bg='#27AE60', fg='white', relief='raised', bd=5,
                                 command=self.yes_button_clicked)
        self.yes_button.pack(side='left', padx=40, pady=20)

        self.no_button = Button(root, text="No", font=('Arial', 14), bg='#E74C3C', fg='white', relief='raised', bd=5,
                                command=self.no_button_clicked)
        self.no_button.pack(side='right', padx=40, pady=20)

        # Play Again and End Game buttons (Initially hidden)
        self.play_again_button = Button(root, text="Play Again", font=('Arial', 14), bg='#3498DB', fg='white',
                                        relief='raised', bd=5, command=self.restart_game)
        self.end_game_button = Button(root, text="End Game", font=('Arial', 14), bg='#E74C3C', fg='white',
                                      relief='raised', bd=5, command=self.root.quit)

        # Game variables
        self.image_count = 0
        self.score = 0
        self.timer_id = None

        self.update_timer()  # Start countdown timer
        self.flash_image()  # Start flashing images

    def update_timer(self):
        """Updates the countdown timer every second."""
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.game_duration - elapsed_time

        if remaining_time <= 0:
            self.end_game()
        else:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)  # Update timer every second

    def get_random_image(self, folder):
        """Selects a random image from the folder."""
        random_image_file = random.choice(folder)
        image_path = os.path.join(self.alive_folder if folder == self.alive_images else self.not_alive_folder,
                                  random_image_file)
        return image_path

    def flash_image(self):
        """Flashes a random image and resets the timer."""
        if time.time() - self.start_time >= self.game_duration:
            self.end_game()
            return

        folder_choice = random.choice([self.alive_images, self.not_alive_images])
        image_path = self.get_random_image(folder_choice)

        self.image = Image.open(image_path)
        self.image = self.image.resize((300, 300))  # Resize image for better display
        self.image = ImageTk.PhotoImage(self.image)

        self.image_label.config(image=self.image)
        self.correct_answer = 'Yes' if folder_choice == self.alive_images else 'No'
        self.image_count += 1

        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.timer_id = self.root.after(3000, self.hide_image)  # Hide the image after 3 seconds

    def hide_image(self):
        """Hides the current image and continues to the next one."""
        self.image_label.config(image='')
        self.flash_image()

    def yes_button_clicked(self):
        """Handles 'Yes' button click."""
        self.check_answer('Yes')
        self.hide_image()

    def no_button_clicked(self):
        """Handles 'No' button click."""
        self.check_answer('No')
        self.hide_image()

    def check_answer(self, user_answer):
        """Compares the user's answer to the correct answer and updates the score."""
        if user_answer == self.correct_answer:
            self.score += 1

    def end_game(self):
        """Displays the final score and shows Play Again and End Game buttons."""
        accuracy_percentage = (self.score / max(1, self.image_count)) * 100  # Avoid division by zero
        final_score_text = f"🎉 Congratulations! 🎉\nYour final score: {accuracy_percentage:.2f}%"

        # Display final score
        self.label.config(text=final_score_text, font=('Arial', 16, 'bold'), fg='#F39C12')

        # Hide the image and disable Yes/No buttons
        self.image_label.config(image='')
        self.yes_button.pack_forget()
        self.no_button.pack_forget()

        # Show Play Again and End Game buttons together
        self.play_again_button.pack(pady=10)
        self.end_game_button.pack(pady=10)

    def restart_game(self):
        """Resets the game and starts over."""
        self.image_count = 0
        self.score = 0
        self.start_time = time.time()  # Reset timer

        # Hide Play Again and End Game buttons
        self.play_again_button.pack_forget()
        self.end_game_button.pack_forget()

        # Reset label text
        self.label.config(text="Is the image alive?", font=('Arial', 18, 'bold'), fg='#ECF0F1')

        # Restart timer and image flashing
        self.update_timer()
        self.flash_image()


# Start script---- NOTE-- THE PARENT FOLDER NAME DOES NOT MATTER HOWEVER THE CHILD FOLDER HAS TO BE ("\alive_images") ("\not_alive_images") -------
#
#     Line 153 EXAMPLE: alive_folder = r"C:\YOUR\FILEPATH\ImageFolder\alive_images"
#     -Line 154 EXAMPLE: not_alive_folder = r"C:\YOUR\FILEPATH\ImageFolder\not_alive_images"

if __name__ == "__main__":
    alive_folder = r"C:\Users\thegr\PycharmProjects\Newphython\ImageFolder\alive_images"
    not_alive_folder = r"C:\Users\thegr\PycharmProjects\Newphython\ImageFolder\not_alive_images"
    root = tk.Tk()
    app = FlashingImageApp(root, alive_folder, not_alive_folder)
    root.mainloop()
