import os
os.environ['SDL_VIDEODRIVER'] = 'fbcon'
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

import pygame
import time
import random

class pyscope :
    screen = None;

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
        pygame.init()
            break

        if not found:
            raise Exception('No suitable video driver found!')

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."


    def drawGraticule(self):
        "Renders an empty graticule"
        # The graticule is divided into 10 columns x 8 rows
        # Each cell is 50x40 pixels large, with 5 subdivisions per
        # cell, meaning 10x8 pixels each.  Subdivision lines are
        # displayed on the central X and Y axis
        # Active area = 10,30 to 510,350 (500x320 pixels)
        borderColor = (255, 255, 255)
        lineColor = (64, 64, 64)
        subDividerColor = (128, 128, 128)
        # Outer border: 2 pixels wide
        pygame.draw.rect(self.screen, borderColor, (8,28,504,324), 2)
        # Horizontal lines (40 pixels apart)
        for i in range(0, 7):
            y = 70+i*40
            pygame.draw.line(self.screen, lineColor, (10, y), (510, y))
        # Vertical lines (50 pixels apart)
        for i in range(0, 9):
            x = 60+i*50
            pygame.draw.line(self.screen, lineColor, (x, 30), (x, 350))
        # Vertical sub-divisions (8 pixels apart)
        for i in range(1, 40):
            y = 30+i*8
            pygame.draw.line(self.screen, subDividerColor, (258, y), (262, y))
        # Horizontal sub-divisions (10 pixels apart)
        for i in range(1, 50):
            x = 10+i*10
            pygame.draw.line(self.screen, subDividerColor, (x, 188), (x, 192))

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
    # Add  the graticule
    scope.drawGraticule()

        # Get a refernce to the system font, size 30
        font = pygame.font.Font(None, 30)
        # Render some white text (pyScope 0.1) onto text_surface
        text_surface = font.render('pyScope (%s)' % "0.1", True, (255, 255, 255))  # White text
    # Blit the text at 10, 0
    scope.screen.blit(text_surface, (10, 0))

        # Update the display
        pygame.display.update()

# Create an instance of the PyScope class
scope = pyscope()
scope.test()

for event in pygame.event.get():
    print "event:", event
    if event.type == pygame.MOUSEBUTTONDOWN:
        sys.exit()

time.sleep(10)

