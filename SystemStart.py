import time
import os
import random
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk


class FlashingImageApp:
    def __init__(self, root, image_folder):
        self.root = root
        self.root.title("Flashing Image Game")

        # Set background color and window size
        self.root.configure(bg='#2C3E50')  # Dark Blue background
        self.root.geometry('600x600')  # Window size

        self.image_folder = image_folder

        # List all image files in the folder
        self.image_files = [f for f in os.listdir(self.image_folder) if
                            f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        if not self.image_files:
            raise ValueError("No images found in the provided folder!")

        self.image = None
        self.image_label = Label(root, bg='#2C3E50')
        self.image_label.pack(pady=20)

        # Set up the UI components with improved font and color
        self.label = Label(root, text="Is the image alive?", font=('Arial', 18, 'bold'), fg='#ECF0F1', bg='#2C3E50')
        self.label.pack(pady=20)

        # Styled buttons
        self.yes_button = Button(root, text="Yes", font=('Arial', 14), bg='#27AE60', fg='white', relief='raised', bd=5,
                                 command=self.yes_button_clicked)
        self.yes_button.pack(side='left', padx=40, pady=20)

        self.no_button = Button(root, text="No", font=('Arial', 14), bg='#E74C3C', fg='white', relief='raised', bd=5,
                                command=self.no_button_clicked)
        self.no_button.pack(side='right', padx=40, pady=20)

        self.image_count = 0
        self.timer_id = None  # To hold the timer reference
        self.flash_image()  # Start flashing images

    def get_random_image(self):
        """Selects a random image from the folder."""
        random_image_file = random.choice(self.image_files)
        image_path = os.path.join(self.image_folder, random_image_file)
        return Image.open(image_path)

    def flash_image(self):
        """Flashes a random image and resets the 5-second timer."""
        if self.image_count >= 100:
            # After 100 images, display the congratulations message and stop
            self.label.config(text="Congratulations! Test complete.")
            self.yes_button.config(state='disabled')
            self.no_button.config(state='disabled')
            return

        # Get a random image and convert it to a format suitable for tkinter
        self.image = self.get_random_image()
        self.image = ImageTk.PhotoImage(self.image)

        # Show the image
        self.image_label.config(image=self.image)

        # Show prompt and buttons only when the image is displayed
        self.label.pack(pady=20)
        self.yes_button.pack(side='left', padx=40, pady=20)
        self.no_button.pack(side='right', padx=40, pady=20)

        # Increment the image count
        self.image_count += 1

        # Cancel the previous timer and set a new 5-second timer for hiding the image
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        # Set a new timer to hide the image after 5 seconds
        self.timer_id = self.root.after(3000, self.hide_image)  # Hide the image after 5 seconds

    def hide_image(self):
        """Hides the current image and the prompt and buttons after 5 seconds."""
        self.image_label.config(image='')

        # Hide prompt and buttons when image is hidden
        self.label.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()

        # Show the next image after 5 seconds (after hiding the current one)
        self.flash_image()

    def yes_button_clicked(self):
        """Handles the 'Yes' button click."""
        print("You clicked 'Yes'")
        self.hide_image()  # Hide current image immediately
        self.flash_image()  # Show the next image

    def no_button_clicked(self):
        """Handles the 'No' button click."""
        print("You clicked 'No'")
        self.hide_image()  # Hide current image immediately
        self.flash_image()  # Show the next image

#Start script Here
if __name__ == "__main__":
    image_folder = r"C:\Users\thegr\PycharmProjects\Newphython\ImageFolder"  # Replace with the path to your image folder
    root = tk.Tk()
    app = FlashingImageApp(root, image_folder)
    root.mainloop()