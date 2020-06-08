import pygame
import random
import time
import threading
import sys
import numpy as np

size = width, height = 1920, 1000
ball_size = 10
black = [0, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
starting_balls = 100
numBalls = 0
show_symptoms_delay = 0
infection_recovery_time = 10
ball_list = np.zeros((4, 1))
print(ball_list)


class Ball():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speedX = 0
        self.speedY = 0
        self.color = [0, 0, 0]


def make_ball(color):
    ball = Ball()
    ball.x = random.randint(ball_size, width - ball_size)
    ball.y = random.randint(ball_size, height - ball_size)
    ball.speedX = random.randrange(-2, 3)
    ball.speedY = random.randrange(-2, 3)
    while ball.speedX == 0 and ball.speedY == 0:
        ball.speedX = random.randrange(-2, 3)
        ball.speedY = random.randrange(-2, 3)
    ball.color = color
    # ball.color = [random.randint(0, 255)for i in range(3)] #random color
    return ball


def infection(balls, infected_balls):
    time.sleep(show_symptoms_delay)
    for ball in balls:
        ball.color = [0, 255, 0]
    time.sleep(infection_recovery_time)
    for ball in balls:
        ball.color = [0, 0, 255]
        infected_balls.remove(ball)
    sys.exit(0)


def find_nearest(ball, ball_list, infected_balls):
    near_balls = []
    for check_ball in ball_list:
        if abs(check_ball.x - ball.x) - ball_size <= 50 and abs(check_ball.y - ball.y) - ball_size <= 50:
            if check_ball not in infected_balls:
                near_balls.append(check_ball)

    if len(near_balls) > 0:
        return near_balls
    else:
        return []


def balls_to_infect(infection_list, infected_balls):
    threading.Thread(target=infection, args=(infection_list, infected_balls)).start()
    for i in infection_list:
        infected_balls.append(i)
    print('Infected: ' + str(len(infected_balls)))


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Balls")
    done = False
    clock = pygame.time.Clock()
    ball_list = []
    infected_balls = []
    for i in range(starting_balls):
        ball = make_ball(blue)
        ball_list.append(ball)

    for i in range(0):
        ball = make_ball(green)
        ball_list.append(ball)
        infected_balls.append(ball)

    while not done:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exiting...')
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    newBall = make_ball(blue)
                    ball_list.append(newBall)
                    print('Num Balls: ' + str(len(ball_list)))
                if event.key == pygame.K_BACKSPACE:
                    try:
                        del ball_list[random.randrange(0, len(ball_list))]
                        print('Num Balls: ' + str(len(ball_list)))
                    except ValueError:
                        print('There are no more balls to remove')
                if event.key == pygame.K_g:
                    newBall = make_ball(green)
                    ball_list.append(newBall)
                    infected_balls.append(newBall)
                    print('Num Balls: ' + str(len(ball_list)))

        for ball in ball_list:
            ball.x += ball.speedX
            ball.y += ball.speedY

            if ball.x > width - ball_size or ball.x < ball_size:
                ball.speedX *= -1
            if ball.y > height - ball_size or ball.y < ball_size:
                ball.speedY *= -1

            if ball.color == green:
                near = find_nearest(ball, ball_list, infected_balls)
                if len(near) > 0:
                    #  near = balls to infect
                    balls_to_infect(near, infected_balls)

        for ball in ball_list:
            pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball_size)

        clock.tick(120)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()