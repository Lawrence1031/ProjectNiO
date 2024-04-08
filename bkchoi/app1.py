import pygame

pygame.init()

background = pygame.display.set_mode((480, 360))
pygame.display.set_caption("SONOL")

fps = pygame.time.Clock()

x_pos = background.get_size()[0]//2 #240
y_pos = background.get_size()[1]//2 #180

play = True

to_x = 0
to_y = 0

while play:

	deltaTime = fps.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			play = False 
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_UP:
				print("K_UP")
				# y_pos = y_pos - 10
				to_y = -1
			if event.key==pygame.K_DOWN:
				print("K_DOWN")
				# y_pos = y_pos + 10
				to_y = 1
			if event.key==pygame.K_RIGHT:
				print("K_RIGHT")
				# x_pos = x_pos + 10
				to_x = 1
			if event.key==pygame.K_LEFT:
				print("K_LEFT")
				# x_pos = x_pos - 10
				to_x = -1
		elif event.type == pygame.KEYUP:
			if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
				to_y = 0
			if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
				to_x = 0




	y_pos = y_pos + to_y
	x_pos = x_pos + to_x	

	if y_pos < 0 : y_pos = 0
	if background.get_size()[1] < y_pos : 
		y_pos = background.get_size()[1];

	if x_pos < 0 : x_pos = 0
	if background.get_size()[0] < x_pos : 
		x_pos = background.get_size()[0];


	background.fill((255,0,0))
	pygame.draw.circle(background, (0,0,255), (x_pos, y_pos), 20)
	pygame.display.update()


pygame.quit()

