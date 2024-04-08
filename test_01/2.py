import pygame

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("버튼 예제")

# 버튼 크기와 위치 설정
button_width = 200
button_height = 100
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2

# 버튼 상태 추적 변수
button_hovered = False

# 버튼 색상
button_color_default = (255, 255, 255)  # 기본 상태 색상 (흰색)
button_color_hover = (0, 255, 0)  # 마우스를 올렸을 때 색상 (녹색)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # 마우스 움직임 이벤트 처리
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                button_hovered = True
            else:
                button_hovered = False

    # 화면 배경 색상 설정
    screen.fill((0, 0, 0))  # 검은색 (0, 0, 0)

    # 버튼 색상 설정
    if button_hovered:
        button_color = button_color_hover
    else:
        button_color = button_color_default

    # 버튼 그리기
    pygame.draw.rect(screen, button_color, pygame.Rect(button_x, button_y, button_width, button_height))

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
