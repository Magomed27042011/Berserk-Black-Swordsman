import pygame  # Импортируем библиотеку Pygame для создания игры
clock = pygame.time.Clock()  # Создаем объект для контроля частоты кадров (FPS)

pygame.init()  # Инициализируем все встроенные модули Pygame

screen = pygame.display.set_mode((618, 359))  # Создаем игровое окно размером 618 на 359 пикселей

pygame.display.set_caption('RasulGames')  # Устанавливаем заголовок игрового окна

pygame.display.set_icon(pygame.image.load('icons/icon.png'))  # Загружаем и устанавливаем иконку для окна

bg = pygame.image.load('icons/icon5.png').convert_alpha()  # Загружаем фоновую картинку с поддержкой прозрачности
walk_right = [  # Создаем список из 4 кадров анимации для движения игрока вправо
    pygame.image.load('icons/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('icons/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('icons/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('icons/player_right/player_right4.png').convert_alpha(),
]
walk_left = [  # Создаем список из 4 кадров анимации для движения игрока влево
    pygame.image.load('icons/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('icons/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('icons/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('icons/player_left/player_left4.png').convert_alpha(),
]

ghost = pygame.image.load('icons/icon6.png')  # Загружаем изображение врага (призрака)
ghost_list_in_game = []  # Создаем пустой список, где будут храниться прямоугольники (rect) активных врагов

player_anim_count = 0  # Переменная-индекс для отслеживания текущего кадра анимации игрока
bg_x = 0  # Начальная координата X для заднего фона (нужна для эффекта движения)
player_speed = 5  # Скорость перемещения игрока по горизонтали
player_x = 150  # Стартовая координата игрока по оси X
player_y = 250  # Стартовая координата игрока по оси Y
is_jump = False  # Флаг-переключатель: прыгает ли игрок в данный момент
jump_count = 8  # Переменная для расчета физики/высоты прыжка
bg_sound = pygame.mixer.Sound('sounds/sound1.mp3')  # Загружаем файл фонового звука/музыки
bg_sound.play()  # Запускаем воспроизведение фоновой музыки

ghost_timer = pygame.USEREVENT + 1  # Создаем уникальный идентификатор для пользовательского игрового события
pygame.time.set_timer(ghost_timer, 2500)  # Запускаем таймер: событие вызова призрака будет срабатывать каждые 2.5 секунды

label = pygame.font.Font('fonts/Opensans.ttf', 40)  # Загружаем шрифт OpenSans размером 40 пикселей
lose_label = label.render('Вы проиграли!', False, (193, 196, 199))  # Создаем текстовую надпись проигрыша серого цвета
restart_label = label.render('Играть заново', False, (115, 132, 148))  # Создаем сине-серую надпись кнопки перезапуска
restart_label_rect = restart_label.get_rect(topleft=(180, 200))  # Получаем хитбокс (рамку) для кнопки перезапуска и ставим в координаты (180, 200)

gameplay = True  # Статусный флаг: True — игра идет, False — экран проигрыша
running = True  # Флаг работы главного цикла программы
bullets_left = 5  # Количество доступных патронов/снарядов у игрока
bullet = pygame.image.load('icons/icon7.png')  # Загружаем изображение пули
bullets = []  # Создаем пустой список для хранения летящих на экране пуль

while running:  # Главный игровой цикл, работает пока running равен True
    
    keys = pygame.key.get_pressed()  # Получаем состояние всех клавиш клавиатуры (нажаты/отжаты)
    screen.blit(bg, (bg_x, 0))  # Отрисовываем первый (основной) фон по координате bg_x
    screen.blit(bg, (bg_x + 618, 0))  # Отрисовываем второй фон правее первого, чтобы картинка была бесшовной при движении

    if gameplay:  # Проверяем, идет ли сейчас активный игровой процесс
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))  # Создаем виртуальный хитбокс игрока на его текущих координатах
        
        if ghost_list_in_game:  # Проверяем, есть ли вообще призраки в списке
           for (i, el) in enumerate(ghost_list_in_game):  # Перебираем всех призраков с получением их индексов (i) и хитбоксов (el)
              screen.blit(ghost, el)  # Отрисовываем картинку призрака на позиции его хитбокса el
              el.x -= 10  # Двигаем призрака влево на 10 пикселей

              if el.x < -10:  # Если призрак полностью улетел за левую границу экрана
                 ghost_list_in_game.pop(i)  # Удаляем этого призрака из списка по индексу, чтобы не тратить память

              if player_rect.colliderect(el):  # Проверяем, столкнулся ли хитбокс игрока с хитбоксом текущего призрака
                gameplay = False  # Если столкнулись, останавливаем геймплей и переключаем на экран проигрыша

        if keys[pygame.K_LEFT]:  # Если зажата стрелка влево
         screen.blit(walk_left[player_anim_count], (player_x, player_y))  # Отрисовываем текущий кадр анимации движения влево
        else:  # Во всех остальных случаях (стоит или идет вправо)
           screen.blit(walk_right[player_anim_count], (player_x, player_y))  # Отрисовываем текущий кадр анимации движения вправо

        if keys[pygame.K_LEFT] and player_x > 50:  # Если зажата стрелка влево и игрок не уперся в левую невидимую границу (50px)
           player_x -= player_speed  # Уменьшаем координату X игрока (двигаем влево)
        elif keys[pygame.K_RIGHT] and player_x < 200:  # Если зажата стрелка вправо и игрок не ушел слишком далеко вправо (200px)
           player_x += player_speed  # Увеличиваем координату X игрока (двигаем вправо)

        if not is_jump:  # Если игрок сейчас не находится в состоянии прыжка
           if keys[pygame.K_SPACE]:  # И при этом нажат пробел
              is_jump = True  # Включаем режим прыжка
        else:  # Если игрок уже прыгает (is_jump равен True)
              if jump_count >= -8:  # Проверяем этап прыжка (от верхней точки 8 до нижней -8)
                 if jump_count > 0:  # Если jump_count положительный — игрок летит вверх
                    player_y -= (jump_count ** 2) / 2  # Формула замедления движения вверх (парабола)
                 else:  # Если jump_count отрицательный — игрок падает вниз
                    player_y += (jump_count ** 2) / 2  # Формула ускорения падения вниз
                 jump_count -= 1  # Уменьшаем счетчик этапа прыжка на каждом кадре
              else:  # Если цикл прыжка полностью завершился (jump_count стал меньше -8)
                 is_jump = False  # Выключаем режим прыжка
                 jump_count = 8  # Сбрасываем счетчик прыжка в начальное значение для следующего раза

        if player_anim_count == 3:  # Если дошли до последнего (4-го) кадра анимации (индекс 3)
         player_anim_count = 0  # Сбрасываем счетчик анимации на первый кадр
        else:  # Если текущий кадр не последний
           player_anim_count += 1  # Переключаем на следующий кадр анимации

        bg_x -= 2  # Двигаем координату фона влево на 2 пикселя для создания эффекта бега
        if bg_x == -618:  # Если картинка фона полностью сместилась влево на свою ширину
           bg_x = 0  # Возвращаем координату фона в ноль для цикличного повторения
           

        if bullets:  # Проверяем, есть ли летящие пули на экране
            for (i, el) in enumerate(bullets):  # Перебираем список пуль с индексами (i) и хитбоксами (el)
                screen.blit(bullet, (el.x, el.y))  # Рисуем пулю на экране по её текущим координатам
                el.x += 4  # Двигаем пулю вправо на 4 пикселя
                if el.x > 630:  # Если пуля улетела за правую границу экрана
                   bullets.pop(i)  # Удаляем пулю из списка, чтобы она больше не обрабатывалась

                if ghost_list_in_game:  # Если на экране в этот момент есть враги
                   for (index, ghost_el) in enumerate(ghost_list_in_game):  # Перебираем всех призраков
                      if el.colliderect(ghost_el):  # Если хитбокс пули (el) пересёкся с хитбоксом призрака (ghost_el)
                         ghost_list_in_game.pop(index)  # Уничтожаем призрака (удаляем из списка)
                         bullets.pop(i)  # Уничтожаем пулю (удаляем из списка)
    else:  # Если gameplay равен False (игрок проиграл, активен экран меню)
       screen.fill((87, 88, 89))  # Закрашиваем весь экран сплошным темно-серым цветом
       screen.blit(lose_label, (180, 100))  # Отрисовываем текст «Вы проиграли!» по координатам (180, 100)
       screen.blit(restart_label, (restart_label_rect))  # Отрисовываем кнопку «Играть заново» по её заготовленному хитбоксу
       
       mouse = pygame.mouse.get_pos()  # Получаем текущие координаты курсора мыши на экране
       if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:  # Если мышь наведена на кнопку рестарта и нажата левая кнопка мыши (индекс 0)
          gameplay = True  # Возвращаем игру в активное состояние
          player_x = 150  # Сбрасываем позицию игрока по X на начальную
          ghost_list_in_game.clear()  # Полностью очищаем список врагов на экране
          bullets.clear()  # Полностью очищаем список летящих пуль
          bullets_left = 5  # Восстанавливаем запас патронов до 5 штук

    pygame.display.update()  # Обновляем содержимое всего экрана, чтобы отобразить изменения

    for event in pygame.event.get():  # Цикл обработки системных событий от операционной системы
        if event.type == pygame.QUIT:  # Если пользователь нажал на крестик закрытия окна
            running = False  # Останавливаем главный игровой цикл
            pygame.quit()  # Корректно завершаем работу модулей Pygame
        if event.type == ghost_timer and gameplay:  # Если сработал таймер призраков и игра сейчас активна
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))  # Создаем хитбокс нового призрака за правой границей (620, 250) и добавляем в список
