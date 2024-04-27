# Color-cheker-for-daltonism
This repository was created to help people with daltonism to find repeated colors on images, especifically colour-coded maps.

# Usage
Execute the code and select the image that you wnat to use on the File menu. It will load any image of phormat .png, .jpg, .jpeg, .gif or .bmp saved on the same folder as the code. Once selected the window will show both the image selected on the left and a blank space of the same size as the image on the right. By clicking on any pixel of the image on the left the same image but with color masked by black will appear on the right. Please, don't click on the right as that will give an error to the program

The size of the window can be changed on View between four different sizes, including full screen. There is also the option of personalized size where the user can input the size manually. Changing the size of the window manually will just modify the dimensions of the window, but not the images.

The tolerance for the color found can be adjusted on the Tolerance menu, where it is set on 30 by deffect. Every time the user clicks on a pixel it will extract the colors on RGB and search for other pixels with all three channels inside the stablished range. There may be some errors due to the perception of two colors being very different from a human perspective, but close from the machine. This can generally be solved by adjusting the tolerance. The same can happen with transparent colors, since the computer will regard them in most cases as different colors.

# Improvements
I created this code to help up a familiar with daltonism in a very specific task, so there is a lot of possible improvements that can be done in this code. Feel free to modify it as much as necessary.
