import pygame
import os
pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("my game")

white = (255, 255, 255)
black = (0, 0, 0)
redc = (255, 0, 0)
yellowc = (255, 255, 0)
fps = 60
vel = 5
bullet_vel = 7
max_bullets = 3

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

# defining a font
health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)

bullet_hit_sound = pygame.mixer.Sound(os.path.join("assets", "Grenade+1.mp3"))
bullet_fire_sound = pygame.mixer.Sound(
    os.path.join("assets", "Gun+Silencer.mp3"))

# subtracting 5 tp put the border in the middle(5 on the left and 5 on the right)
border = pygame.Rect(width//2 - 5, 0, 10, height)
ship_width, ship_height = 55, 40
yellow_ship_img = pygame.image.load(
    os.path.join('assets', 'spaceship_yellow.png'))
red_ship_img = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))

yellow_ship = pygame.transform.rotate(pygame.transform.scale(
    yellow_ship_img, (ship_width, ship_height)), 90)
red_ship = pygame.transform.rotate(pygame.transform.scale(
    red_ship_img, (ship_width, ship_height)), 270)
space = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space.png')), (width, height))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    win.blit(space, (0, 0))
    pygame.draw.rect(win, black, border)
    # the "1" is for anti-aliasing( I HAVE NO FREAKING IDEA WHAT THAT IS SO DON'T ASK ME !!!)
    red_health_text = health_font.render(
        "health: " + str(red_health), 1, white)
    yellow_health_text = health_font.render(
        "health: " + str(yellow_health), 1, white)
    win.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))
    # using blit to display a text or image on the screen
    win.blit(yellow_ship, (yellow.x, yellow.y))
    win.blit(red_ship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(win, redc, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(win, yellowc, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_q] and yellow.x - vel > 0:  # left
        yellow.x -= vel
    # right
    if keys_pressed[pygame.K_d] and yellow.x + vel < border.x - (5 + yellow.width):
        yellow.x += vel
    if keys_pressed[pygame.K_z] and yellow.y - vel > 0:  # up
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height + 10 < height:  # down
        yellow.y += vel


def red_handle_movement(keys_pressed, red):
    # left
    if keys_pressed[pygame.K_LEFT] and red.x - vel > border.x + border.width:
        red.x -= vel
    if keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < width:  # right
        red.x += vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0:  # up
        red.y -= vel
    if keys_pressed[pygame.K_DOWN] and red.y + vel + red.height + 10 < height:  # down
        red.y += vel


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > width:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    win.blit(draw_text, (width//2 - draw_text.get_width() /
             2, height//2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, height/2, ship_width, ship_height)
    yellow = pygame.Rect(100, height/2, ship_width, ship_height)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()  # controlling the speed of the while loop
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_KP_0 and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()

            if event.type == yellow_hit:
                yellow_health -= 1
                bullet_hit_sound.play()

        winner_text = ""

        if yellow_health <= 0:
            winner_text = "red wins!"

        if red_health <= 0:
            winner_text = "Yellow wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        print(yellow_bullets, red_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()
