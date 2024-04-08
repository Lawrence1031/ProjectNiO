import pygame
import math

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("카드 흔들기 예제")

# 카드 이미지 로드
card_image = pygame.image.load("img/card.jpg")
card_width = card_image.get_width()
card_height = card_image.get_height()

# 카드 초기 위치 설정
card_x = (screen_width - card_width) // 2
card_y = (screen_height - card_height) // 2

# 애니메이션 변수 설정
angle = 0  # 회전 각도
amplitude = 20  # 흔들림 크기
frequency = 0.1  # 흔들림 속도

clock = pygame.time.Clock()

# 게임 루프
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 배경 색상 설정
    screen.fill((0, 0, 0))  # 검은색(0, 0, 0)

    # 카드 위치 업데이트
    angle += frequency
    card_offset = math.sin(angle) * amplitude
    card_y = (screen_height - card_height) // 2 + card_offset

    # 카드 그리기
    screen.blit(card_image, (card_x, card_y))

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
