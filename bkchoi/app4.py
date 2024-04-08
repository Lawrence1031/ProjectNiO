import pygame 

pygame.init()

background = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("니하오")


image_bg = pygame.image.load("image/sky.png")
image_bg = pygame.transform.scale(image_bg, (1280, 800))

image_banana = pygame.image.load("image/banana.png")
image_banana = pygame.transform.scale(image_banana, (150, 150))

image_monkey = pygame.image.load("image/monkey.png")
image_monkey = pygame.transform.scale(image_monkey, (400, 400))

size_bg_width, size_bg_height = background.get_size()

size_banana_width, size_banana_height = image_banana.get_rect().size

x_pos_banana = size_bg_width/2 - size_banana_width/2
y_pos_banana = 0


size_monkey_width, size_monkey_height = image_monkey.get_rect().size

x_pos_monkey = size_bg_width/2 - size_monkey_width/2
y_pos_monkey = size_bg_height - size_monkey_height


to_y = 30
to_x = 0


fps = pygame.time.Clock()


play = True

while play:

	deltaTime = fps.tick(60)

	y_pos_monkey = y_pos_monkey + to_y

	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			play = False
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_UP:
				y_pos_monkey = 150 #원숭이를 위로 보냄
			if event.key==pygame.K_RIGHT:
				to_x = 10
			if event.key==pygame.K_LEFT:
				to_x = -10
		elif event.type == pygame.KEYUP:
			if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
				to_x = 0


	background.blit(image_bg, (0,0))


	x_pos_monkey = x_pos_monkey + to_x

	if size_bg_height - size_monkey_height < y_pos_monkey : 
		y_pos_monkey = size_bg_height - size_monkey_height

	if x_pos_monkey < 0 : x_pos_monkey = 0
	if size_bg_width - size_monkey_width < x_pos_monkey : x_pos_monkey = size_bg_width - size_monkey_width

	background.blit(image_monkey, (x_pos_monkey, y_pos_monkey))
	background.blit(image_banana, (x_pos_banana, y_pos_banana))
	pygame.display.update()

pygame.quit()