#Libraries used
import pygame
import Network

#Display settings (window name, dimensions etc)
pygame.init()
WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Table Tenis")
FPS = 60
PEACH = (255, 167, 129)
MAROON = (91, 14, 45)
SCORE_FONT = pygame.font.SysFont("algerian", 40)
WINNING_SCORE = 10

#Creating paddles
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

class Paddle:

    COLOUR = PEACH
    VEL = 5
    
    def __init__ (self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw (self, win):
        pygame.draw.rect (win, self.COLOUR, (self.x, self.y, self.width, self.height))

    def move (self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
            
    def reset (self):
        self.x = self.original_x
        self.y = self.original_y
            
#Creating ball
BALL_RADIUS = 15

class Ball:

    COLOUR = PEACH
    MAX_VEL = 7

    def __init__ (self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw (self, win):
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.radius)
    
    def move (self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset (self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0

#Graphics
def draw (win, paddles, ball, left_score, right_score):
    win.fill(MAROON)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, PEACH)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, PEACH)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range (10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        else:
            pygame.draw.rect(win, PEACH, (WIDTH//2 - 5, i, 10, HEIGHT//20))
    ball.draw(win)
    pygame.display.update()

#Collisions
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if ball.y>= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

#Movement
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VEL <= HEIGHT:
        right_paddle.move(up=False)

def read_pos():
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

#Main game
def main ():
    run = True
    n = Network
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball (WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        key = pygame.key.get_pressed()
        if key [pygame.K_ESCAPE]:
            pygame.QUIT
            break
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        if left_score >= WINNING_SCORE:
            win_text = "LEFT PLAYER WON!"
            text = SCORE_FONT.render(win_text, 1, PEACH)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(2000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        elif right_score >= WINNING_SCORE:
            win_text = "RIGHT PLAYER WON!"
            text = SCORE_FONT.render(win_text, 1, PEACH)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
    pygame.quit()

if __name__ == "__main__":
    main()