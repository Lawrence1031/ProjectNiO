import pygame

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("카드 겹치기 예제")

# 카드 이미지 로드
card_images = [
    pygame.image.load("img/card.jpg"),
    pygame.image.load("img/card.jpg"),
    pygame.image.load("img/card.jpg")
]

# 카드 초기 위치 설정
card_width = card_images[0].get_width()
card_height = card_images[0].get_height()

card_x = (screen_width - card_width * 3) // 2
card_y = (screen_height - card_height) // 2

# 겹치는 카드 간격
overlap = 30

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 배경 색상 설정
    screen.fill((0, 0, 0))  # 검은색(0, 0, 0)

    # 카드 그리기
    for i in range(len(card_images)):
        card_rect = card_images[i].get_rect()
        card_rect.topleft = (card_x + i * overlap, card_y)
        screen.blit(card_images[i], card_rect)

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
