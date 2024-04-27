import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import os



# Function to mask the colors of the image
def mask_colors(pixel_color):
    global output
    # Transform the pixel color from RGB to BGR
    pixel_color = pixel_color[::-1]
    # Create cv2 image to work with from PIL image
    image_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Create the boundaries for the search
    print("Tolerance: ", tolerance)
    lower=np.clip(np.array(pixel_color, dtype=np.int16) - tolerance/2, 0, 255)
    upper=np.clip(np.array(pixel_color, dtype=np.int16) + tolerance/2, 0, 255)
    
    #Create the mask with the findings of the search
    mask = cv2.inRange(image_cv2, lower, upper)
    print("lower: ", lower)
    print("upper: ", upper)
    print("Number of pixels with that color found: ",np.count_nonzero(mask!=0))
    if np.count_nonzero(mask!=0) == 0:
        print("There was an error")

    # Invert the mask and apply bitwise AND with the original image
    inverted_mask = cv2.bitwise_not(mask)  # Invert the mask
    output = cv2.bitwise_and(image_cv2, image_cv2, mask=inverted_mask)

    # Convert the image back to PIL format
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    output = Image.fromarray(output)

    # Show the output in the right label
    resize_image(resized_img.size)



# Get the position and color of the clicked pixel
def on_image_click(event):
    print("Image clicked at position", event.x, event.y)

    # Get the color of the pixel at the clicked position
    color = resized_img.getpixel((event.x, event.y))
    color = color[:3]
    print("Color of clicked pixel:", color)
    mask_colors(color)


#  Resize both images to the selected size
def resize_image(size):
    global img, output, label, blank_label, resized_img

    # Resize the image
    resized_img = img.resize(size)
    resized_output = output.resize(size)


    # Convert the resized image to a Tkinter-compatible photo image
    resized_photo = ImageTk.PhotoImage(resized_img)
    resized_photo_output = ImageTk.PhotoImage(resized_output)

    # Update the label with the resized image
    label.config(image=resized_photo)
    label.image = resized_photo  # Keep a reference to the image to prevent it from being garbage collected

    # Update the blank label with the blank image
    blank_label.config(image=resized_photo_output)
    blank_label.image = resized_photo_output  # Keep a reference to the image to prevent it from being garbage collected




# Select the file and prepare the white clone    
def on_file_selection(filename):
    global img, label, blank_label, tolerance, output, resized_img

    tolerance = 30 # Default tolerance value

    print(f"Image selected: {filename}")

    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Open the image and convert it to a Tkinter-compatible photo image
    img = Image.open(filename)
    photo = ImageTk.PhotoImage(img)

    resized_img = img

    # Create a label and add the image to it
    label = tk.Label(frame, image=photo)
    label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
    label.grid(row=0, column=0)  # Place the label in the left column of the grid

    # Bind the mouse click event to the callback function
    label.bind("<Button-1>", on_image_click)

    # Create a blank image of the same size as the original image
    output = Image.new('RGB', img.size, 'white')  # 'white' indicates the color of the image
    blank_photo = ImageTk.PhotoImage(output)
    
    # Create a label and place the blank image in it
    blank_label = tk.Label(frame, image=blank_photo)
    blank_label.grid(row=0, column=1)


# Select the view size
def on_view_selection(view):

    # Check if 'img' is defined
    if 'img' not in globals():
        print("No image selected yet.")
        return
    else:

        # Define the sizes for each view
        sizes = {
        0: img.size,  # Original size
        1: (400, 350),  # Small size (half the original size)
        2: (600, 500),  # Medium size (same as the original size)
        3: (900, 650),  # Large size (double the original size)
        4: (int((root.winfo_screenwidth()/2)-15), int(root.winfo_screenheight()-100)),  # Full screen size
        5: 'personalized'  # Personalized size
        }
        # If the view is 'personalized', ask the user for the new size
        if sizes[view] == 'personalized':
            while True:
                try:
                    width = simpledialog.askinteger("Input", "Enter the width of the image (as reference large size is 900):")
                    height = simpledialog.askinteger("Input", "Enter the height of the image (as reference large size is 650):")
                    sizes[view] = (width, height)
                    break
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid integer.")

        print(f"View selected: {sizes[view]}")

        resize_image(sizes[view])


# Change the tolerance value
def on_tolerance_selection():
    global tolerance
    while True:
        try:
            tolerance = simpledialog.askinteger("Input", "Enter the new tolerance value (by defect it is 30):")
            break
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid float.")


# Main program

root = tk.Tk()

menubar = tk.Menu(root)

# Create the File menu
filemenu = tk.Menu(menubar, tearoff=0)

# List all files in the current directory
for filename in os.listdir('.'):
    # If the file is an image, add it to the menu
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        filemenu.add_command(label=filename, command=lambda f=filename: on_file_selection(f))

# Create the View menu
viewmenu = tk.Menu(menubar, tearoff=0)

# Dictionary of sizes
sizes = {
    "Original": 0,
    "Small": 1,
    "Medium": 2,
    "Large": 3,
    "Full Screen": 4,
    "Personalized": 5
}

# Add commands to the View menu
for size, value in sizes.items():
    viewmenu.add_command(label=size, command=lambda v=value: on_view_selection(v))

# Create the Tolerance menu
tolerancemenu = tk.Menu(menubar, tearoff=0)

# Add a command to the Tolerance menu
tolerancemenu.add_command(label="Set Tolerance", command=on_tolerance_selection)

# Add the File, View and Tolerance menus to the menubar
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="View", menu=viewmenu)
menubar.add_cascade(label="Tolerance", menu=tolerancemenu)

root.config(menu=menubar)

# Create a frame to hold the image and blank space
frame = tk.Frame(root)
frame.pack()

root.mainloop()


