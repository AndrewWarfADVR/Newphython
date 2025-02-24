import os
import random
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk


class FlashingImageApp:
    def __init__(self, root, alive_folder, not_alive_folder):
        self.root = root
        self.root.title("Flashing Image Game")
        self.root.configure(bg='#2C3E50')  # Dark Blue background
        self.root.geometry('600x600')  # Window size

        self.alive_folder = alive_folder
        self.not_alive_folder = not_alive_folder

        # Load images
        self.alive_images = [f for f in os.listdir(self.alive_folder) if
                             f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        self.not_alive_images = [f for f in os.listdir(self.not_alive_folder) if
                                 f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

        if not self.alive_images and not self.not_alive_images:
            raise ValueError("No images found in the provided folders!")

        self.image_label = Label(root, bg='#2C3E50')
        self.image_label.pack(pady=20)

        self.label = Label(root, text="Is the image alive?", font=('Arial', 18, 'bold'), fg='#ECF0F1', bg='#2C3E50')
        self.label.pack(pady=20)

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

        self.image_count = 0
        self.score = 0
        self.total_images = 500   #<----____THIS WILL CHANGE THE LENGTH OF THE APPLICATION RUN TIME BY ADDING A HIGHER NUMBER WILL EXTEND THE RUN TIME..-----
        self.timer_id = None
        self.flash_image()  # Start flashing images
        # Keyboard function  ---
        # Bind keyboard buttons (4 for Yes, 6 for No)
        self.root.bind('4', self.yes_button_clicked_from_key)
        self.root.bind('6', self.no_button_clicked_from_key)

    def get_random_image(self, folder):
        """Selects a random image from the folder."""
        random_image_file = random.choice(folder)
        image_path = os.path.join(self.alive_folder if folder == self.alive_images else self.not_alive_folder,
                                  random_image_file)
        return image_path

    def flash_image(self):
        """Flashes a random image and resets the timer."""
        if self.image_count >= self.total_images:
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

    # Script 4 KEY = ANSWER YES --- 6 Key = NO

    def yes_button_clicked_from_key(self, event=None):
        """Handles 'Yes' key press (key 4)."""
        self.check_answer('Yes')
        self.hide_image()

    def no_button_clicked_from_key(self, event=None):
        """Handles 'No' key press (key 6)."""
        self.check_answer('No')
        self.hide_image()

    def check_answer(self, user_answer):
        """Compares the user's answer to the correct answer and updates the score."""
        if user_answer == self.correct_answer:
            self.score += 1

    def end_game(self):
        """Displays the final score and shows Play Again and End Game buttons."""
        accuracy_percentage = (self.score / self.total_images) * 100  # Calculate percentage
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

        # Hide Play Again and End Game buttons
        self.play_again_button.pack_forget()
        self.end_game_button.pack_forget()

        # Reset label text
        self.label.config(text="Is the image alive?", font=('Arial', 18, 'bold'), fg='#ECF0F1')

        # Restart image flashing
        self.flash_image()


# Start script ---NOTE! FOR USER MAKE SURE TO CHOOSE A FILE PATH FOR ALIVE AND NOT ALIVE FOLDER MAKE SURE THESE FOLDERS are IN PARENT FOLDER EXAMPLE Parent folder in this case is ("ImageFolder") which has CHILD folders which are ("\alive_images") ("\not_alive_images") THE PARENT FOLDER NAME DOES NOT MATTER HOWEVER THE CHILD FOLDER HAS TO BE ("\alive_images") ("\not_alive_images")
if __name__ == "__main__":
    alive_folder = r"C:\Users\kakee\ImageFolder\alive_images"
    not_alive_folder = r"C:\Users\kakee\ImageFolder\not_alive_images"
    root = tk.Tk()
    app = FlashingImageApp(root, alive_folder, not_alive_folder)
    root.mainloop()