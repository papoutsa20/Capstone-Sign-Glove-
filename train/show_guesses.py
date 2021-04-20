import pygame
import serial
import keyboard
#ser = serial.Serial('COM4', 9600, timeout=2)


ser = serial.Serial('/dev/cu.usbmodem142301', 9600, timeout=2)

#
# Code below was taken from https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
#

pygame.init()


# assigning values to X and Y variable
X = 400
Y = 400

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Show Text')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

white = (255,255,255)
black = (0,0,0)
ser.reset_input_buffer()
word = ''
while True:
    letter = ser.readline()
    letter = letter.decode("utf-8")
    print(letter)
    # completely fill the surface object
    # with white color
    if keyboard.is_pressed('space'):
        word = word + letter

    # get text
    #
    #
    if(letter):
        display_surface.fill(white)
        text = font.render(word+letter, True,black, white)

    # create a rectangular object for the
    # text surface object
        textRect = text.get_rect()

    # set the center of the rectangular object.
        textRect.center = (X // 2, Y // 2)

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
        display_surface.blit(text, textRect)
        pygame.display.update()
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:

            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen.
