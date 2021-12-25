# import pygame module in this program 
import pygame, sys

from win32api import GetSystemMetrics


# activate the pygame library . 
# initiate pygame and give permission 
# to use pygame's functionality. 
pygame.init() 

# define the RGB value 
# for white colour 
white = (255, 255, 255) 


if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    # PyScreeze and Pillow needs to account for this to make accurate screenshots.
    # TODO - How does macOS and Linux handle monitor scaling?
    import ctypes
    try:
       ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.
    width =  GetSystemMetrics(0)
    height = GetSystemMetrics(1)
else:
    #If you want a fancy costum method to read out the screensize you should do it here!
    width = 1920
    height = 1080





# create the display surface object 
# of specific dimension..e(X, Y). 
display_surface = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN) 

# set the pygame window name 
pygame.display.set_caption('Image') 

# create a surface object, image is drawn on it. 
tag1 = pygame.image.load(r'AprilTags\tag16h5_0.png') 
tag2 = pygame.image.load(r'AprilTags\tag16h5_1.png') 
tag3 = pygame.image.load(r'AprilTags\tag16h5_2.png') 

tag_size = height // 2

tag1 = pygame.transform.scale(tag1, (tag_size,tag_size))
tag2 = pygame.transform.scale(tag2, (tag_size,tag_size))
tag3 = pygame.transform.scale(tag3, (tag_size,tag_size))



total_time_steps = 1000
x0, y0 = (tag_size,tag_size)

# infinite loop 
for t in range(total_time_steps):

	# completely fill the surface object 
	# with white colour 
    display_surface.fill(white) 

	# copying the image surface object 
	# to the display surface object at 
	# (0, 0) coordinate.
    if t < 10:
        display_surface.blit(tag1, (0, 0))
        display_surface.blit(tag2, (width - tag_size, 0))
        display_surface.blit(tag3, (0, height - tag_size))


    if t >= 10:
        radius = height // 10
        #location = (x0 + (width - x0) * t // total_time_steps, y0 + (height - y0) * t // total_time_steps)
        location = (width //2 , height // 2)

        pygame.draw.circle(display_surface, (0,0, 0), location,radius)


    if t >= 500 and t < 550:
        radius = height // 10 + 100
        location = (width //2 + 300 , height // 2 - 700)
        pygame.draw.circle(display_surface, (0,0, 0), location, radius)



    pygame.time.wait(33)

	# iterate over the list of Event objects 
	# that was returned by pygame.event.get() method. 
    for event in pygame.event.get() : 

		# if event object type is QUIT 
		# then quitting the pygame 
		# and program both. 
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) : 

			# deactivates the pygame library 
            pygame.quit() 

			# quit the program. 
            quit() 

	# Draws the surface object to the screen. 
    pygame.display.update() 
			
