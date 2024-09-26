import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600  # Увеличено поле
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поиск клубники")

# Загрузка изображений
koala_image = pygame.image.load('koala.png')
strawberry_image = pygame.image.load('strawberry.png')

# Изменение размера изображений
koala_image = pygame.transform.scale(koala_image, (40, 40))
strawberry_image = pygame.transform.scale(strawberry_image, (40, 40))

# Цвета
DARK_COLOR = (20, 20, 20)
RETRO_COLOR = (255, 128, 0)
WHITE = (255, 255, 255)
SHIELD_COLOR = (0, 0, 255)  # Цвет щита
PROTECT_COLOR = (255, 255, 255)  # Цвет защитного круга

# Шрифты
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Переменные игры
koala_pos = [WIDTH // 2, HEIGHT // 2]
koala_speed = 0.3  # Установлена скорость коалы на 0.3

# Начальные клубники
strawberries = []
for _ in range(5):  # Изначально 5 клубник
    pos = [random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
    speed = [random.choice([-0.3, 0.3]), random.choice([-0.3, 0.3])]  # Установлена скорость клубники на 0.3
    strawberries.append({'pos': pos, 'speed': speed})

shield_pos = [-100, -100]  # Убираем щит в начале
game_over = False
has_shield = False
show_instructions = True  # Инициализируем переменную для инструкций
last_strawberry_time = 0  # Время последнего появления клубники
shield_collected_time = 0  # Время, когда был собран щит

# Таймер игры
clock = pygame.time.Clock()

# Функция для отображения текста на экране
def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

# Основной игровой цикл
def game_loop():
    global koala_pos, strawberries, shield_pos, game_over
    global has_shield, show_instructions, last_strawberry_time, shield_collected_time  # Добавляем shield_collected_time
    running = True
    start_ticks = pygame.time.get_ticks()

    while running:
        screen.fill(DARK_COLOR)

        if show_instructions:
            draw_text("Цель: Собрать клубнику!", font, RETRO_COLOR, 50, HEIGHT // 2 - 50)
            draw_text("Используйте стрелки или WASD для перемещения коалы.", font, RETRO_COLOR, 50, HEIGHT // 2)
            draw_text("Нажмите Enter, чтобы начать.", font, RETRO_COLOR, 50, HEIGHT // 2 + 50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    show_instructions = False
                    start_ticks = pygame.time.get_ticks()
            continue
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Движение коалы
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and koala_pos[0] > 0:
            koala_pos[0] -= koala_speed
        if keys[pygame.K_d] and koala_pos[0] < WIDTH - 40:
            koala_pos[0] += koala_speed
        if keys[pygame.K_w] and koala_pos[1] > 0:
            koala_pos[1] -= koala_speed
        if keys[pygame.K_s] and koala_pos[1] < HEIGHT - 40:
            koala_pos[1] += koala_speed

        # Движение клубники
        for strawberry in strawberries:
            strawberry['pos'][0] += strawberry['speed'][0]
            strawberry['pos'][1] += strawberry['speed'][1]
            
            # Отражение клубники от стен
            if strawberry['pos'][0] <= 0 or strawberry['pos'][0] >= WIDTH - 40:
                strawberry['speed'][0] = -strawberry['speed'][0]
            if strawberry['pos'][1] <= 0 or strawberry['pos'][1] >= HEIGHT - 40:
                strawberry['speed'][1] = -strawberry['speed'][1]

            # Проверка на столкновение с клубникой
            if pygame.Rect(koala_pos[0], koala_pos[1], 40, 40).colliderect(strawberry['pos'][0], strawberry['pos'][1], 40, 40):
                if has_shield:
                    strawberries.remove(strawberry)  # Удалить клубнику
                    has_shield = False  # Если есть щит, он исчезает
                else:
                    game_over = True

        # Появление клубники каждые 5 секунд
        current_time = pygame.time.get_ticks()
        if current_time - last_strawberry_time >= 5000:  # 5000 миллисекунд = 5 секунд
            last_strawberry_time = current_time
            pos = [random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
            speed = [random.choice([-0.3, 0.3]), random.choice([-0.3, 0.3])]  # Установлена скорость клубники на 0.3
            strawberries.append({'pos': pos, 'speed': speed})

        # Проверка на появление щита
        if has_shield:
            shield_pos = [-100, -100]  # Убираем щит после сбора
        else:
            if shield_collected_time == 0 or (current_time - shield_collected_time >= 15000):  # 15000 миллисекунд = 15 секунд
                shield_pos = [random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
                shield_collected_time = current_time  # Обновляем время сбора щита

        # Проверка на столкновение с щитом
        if pygame.Rect(koala_pos[0], koala_pos[1], 40, 40).colliderect(shield_pos[0], shield_pos[1], 40, 40):
            has_shield = True
            shield_collected_time = pygame.time.get_ticks()  # Сохраняем время, когда щит был собран
            shield_pos = [-100, -100]  # Убираем щит после сбора

        # Отрисовка всех элементов
        screen.blit(koala_image, koala_pos)
        for strawberry in strawberries:
            screen.blit(strawberry_image, strawberry['pos'])
        if has_shield:
            pygame.draw.circle(screen, PROTECT_COLOR, (koala_pos[0] + 20, koala_pos[1] + 20), 30)  # Отображение защитного круга

        # Отрисовка щита на поле (увеличен радиус до 50)
        if shield_pos != [-100, -100]:
            pygame.draw.circle(screen, SHIELD_COLOR, (shield_pos[0] + 20, shield_pos[1] + 20), 30)  # Увеличение радиуса до 70

        # Отображение состояния щита и таймера
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        draw_text(f"Время: {seconds}", small_font, WHITE, 10, 10)
        draw_text("Щит: " + ("Есть" if has_shield else "Нет"), small_font, WHITE, 10, 40)
        draw_text("openai", small_font, WHITE, WIDTH - 70, HEIGHT - 30)

        pygame.display.update()

        # Проверка конца игры
        if game_over:
            time.sleep(2)  # Пауза перед перезапуском
            koala_pos = [WIDTH // 2, HEIGHT // 2]
            strawberries = []
            for _ in range(5):  # Возобновляем 5 клубник
                pos = [random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
                speed = [random.choice([-0.3, 0.3]), random.choice([-0.3, 0.3])]  # Установлена скорость клубники на 0.3
                strawberries.append({'pos': pos, 'speed': speed})

            shield_pos = [-100, -100]
            game_over = False
            has_shield = False
            shield_collected_time = 0  # Сбрасываем время сбора щита
            start_ticks = pygame.time.get_ticks()

# Запуск игрового цикла
game_loop()
pygame.quit()
