import pygame 

pygame.init()

background = pygame.display.set_mode((480, 360))
pygame.display.set_caption("니하오")


play = True
while play:
	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			play = False

	background.fill((255, 255, 255))

	pygame.draw.rect(background, (0,255, 0), (240, 180, 100, 50))

	pygame.draw.ellipse(background, (0,0,255), (240, 180, 100, 50), 5)
	pygame.draw.polygon(background, (255,255,0), [[100,100],[0,200],[200,200]])
	# pygame.draw.line(background, (0,0,0), (240, 0), (240, 360))
	# pygame.draw.line(background, (0,0,0), (0, 0), (480, 360), 5)
	# pygame.draw.line(background, (0,0,0), (0, 360), (480, 0), 5)

	# for i in range(0,480, 30):
	# 	pygame.draw.line(background, (0,0,0), (i,0), (i,360))

	# for i in range(0,360, 30):
	# 	pygame.draw.line(background, (0,0,0), (0,i), (480, i))

	pygame.display.update()

pygame.quit()



