import pygame
import time
import random

class Game:
    # Constructor for initializing
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Brick Game")

        # Ball Variables
        self.ball_x = 383
        self.ball_y = 540
        self.ballDirection = 'UpRight'
        self.ball_stop = True

        # Paddle Variables
        self.paddle_x = 350
        self.paddle_y = 548
        self.paddle_stop = True

        # Game logic variables
        self.game_started = False
        self.pause = False
        self.running = True
        self.lives = 3
        self.score = 0
        self.high_score = 0

        # Brick Variables
        self.bricks = []
        self.power_ups =[]
        self.cracked_bricks = []
        self.brick_states = {}

        # Load Images
        self.purple_bricks = pygame.image.load('img/Breakout Tile Set Free/PNG/05-Breakout-Tiles.png')
        self.purple_bricks_cracked = pygame.image.load('img/Breakout Tile Set Free/PNG/06-Breakout-Tiles.png')
        self.grey_bricks = pygame.image.load('img/Breakout Tile Set Free/PNG/17-Breakout-Tiles.png')
        self.grey_bricks_cracked = pygame.image.load('img/Breakout Tile Set Free/PNG/18-Breakout-Tiles.png')
        self.heart = pygame.image.load('img/Breakout Tile Set Free/PNG/60-Breakout-Tiles.png')
        self.paddle = pygame.image.load('img/Breakout Tile Set Free/PNG/56-Breakout-Tiles.png')
        self.ball = pygame.image.load('img/Breakout Tile Set Free/PNG/58-Breakout-Tiles.png')
        self.power_up =  pygame.image.load('img/Breakout Tile Set Free/PNG/60-Breakout-Tiles.png')

        # Image Transformation
        self.paddle = pygame.transform.scale(self.paddle, (80, 20))
        self.heart = pygame.transform.scale(self.heart, (20, 20))
        self.ball = pygame.transform.scale(self.ball, (15, 15))
        self.power_up = pygame.transform.scale(self.power_up, (30, 30))
        self.purple_bricks = pygame.transform.scale(self.purple_bricks, (60, 20))
        self.grey_bricks = pygame.transform.scale(self.grey_bricks, (60, 20))
        self.purple_bricks_cracked = pygame.transform.scale(self.purple_bricks_cracked, (60, 20))
        self.grey_bricks_cracked = pygame.transform.scale(self.grey_bricks_cracked, (60, 20))

        # Load sounds
        self.hit_brick_sound = pygame.mixer.Sound('img/Breakout Tile Set Free/PNG/brick.wav')
        self.hit_paddle_sound = pygame.mixer.Sound('img/Breakout Tile Set Free/PNG/glass.wav')
        self.game_over_sound = pygame.mixer.Sound('img/Breakout Tile Set Free/PNG/game_over2.wav')
        self.life_lost_sound = pygame.mixer.Sound('img/Breakout Tile Set Free/PNG/game_over.wav')

    # FUNCTIONS


    # brick creation
    def generate_bricks(self):
        brick_x = 65
        brick_y = 20
        for row in range(4):
            for col in range(13):
                x = col * brick_x
                y = 50 + row * brick_y
                brick_color = self.purple_bricks if (row + col) % 2 == 0 else self.grey_bricks
                brick_rect = pygame.Rect(x, y, brick_x, brick_y)
                self.bricks.append({"rect": brick_rect, "color": brick_color, "state": 0})
    def all_bricks_removed(self):
        if not self.bricks:
            self.ball_stop = True
            self.reset_ball()
            time.sleep(0.2)
            self.generate_bricks()


    # ball reset
    def reset_ball(self):
        self.ball_x, self.ball_y = 383, 540
        self.paddle_x = 350
        self.paddle_y = 548
        for power_up in self.power_ups:
            self.power_ups.remove(power_up)


    # store highscore
    def highScore(self):
        self.file = open("HighScore.txt", "a+")
        self.file.seek(0)
        self.content = self.file.read()

        if not self.content:
            self.high_score = 0
        else:
            self.high_score = int(self.content)

        if self.score > self.high_score:
           self.high_score = self.score
           self.file.seek(0)
           self.file.truncate()
           self.file.write(str(self.high_score))

        self.file.close()


    # MOVEMENTS

    def go_up_right(self):
        self.ball_x += 1.7
        self.ball_y -= 3
        time.sleep(0.007)

    def go_down_left(self):
        self.ball_x -=1.7
        self.ball_y += 3
        time.sleep(0.007)

    def go_up_left(self):
        self.ball_x -= 1.7
        self.ball_y -= 3
        time.sleep(0.007)

    def go_down_right(self):
        self.ball_x += 1.7
        self.ball_y += 3
        time.sleep(0.007)

    def ball_movement(self):
            if self.ballDirection == 'UpRight':
                self.go_up_right()
            if self.ballDirection == 'DownLeft':
                self.go_down_left()
            if self.ballDirection == 'UpLeft':
                self.go_up_left()
            if self.ballDirection == 'DownRight':
                self.go_down_right()

            if self.ball_x <= 0:
                self.ballDirection = 'DownRight'

            if self.ball_x >= 785:
                self.ballDirection = 'DownLeft'
            if self.ball_y <= 0:
                self.ballDirection = 'DownLeft'

            self.paddle_collision()
            self.brick_collision()

            if self.ball_y >= 600:
                self.life_lost_sound.play()
                self.lives -= 1
                if self.lives > 0:
                    self.reset_ball()
                    self.ball_stop = True
                    self.paddle_stop = True
                    self.ballDirection = 'UpRight'
                    time.sleep(2)
                else:
                    self.game_over_sound.play()
                    self.gameOverScreen()

    def paddle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle_x > 0:
            self.paddle_x -= 10
        if keys[pygame.K_RIGHT] and self.paddle_x < 720:
            self.paddle_x += 10

    def power_up_movement(self):
        for power_up in self.power_ups[:]:
            power_up.y += 2

            if power_up.y > 600:
                self.power_ups.remove(power_up)


    # COLLISIONS

    def brick_collision(self):
        ball_rect = pygame.Rect(self.ball_x, self.ball_y, 15, 15)
        for brick in self.bricks[:]:
            if brick["rect"].colliderect(ball_rect):
                self.hit_brick_sound.play()
                if brick["state"] == 0:
                    brick["state"] = 1
                    self.score += 5
                    self.ballDirection = 'DownLeft'
                elif brick["state"] == 1:
                    self.bricks.remove(brick)
                    self.score += 10
                    self.ballDirection = 'DownRight'
                    if random.randint(1, 4) == 1:
                        power_up_rect = pygame.Rect(brick["rect"].x, brick["rect"].y, 20, 20)
                        self.power_ups.append(power_up_rect)
                    break

    def paddle_collision(self):
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, 80, 20)
        ball_rect = pygame.Rect(self.ball_x, self.ball_y, 15, 15)
        for power_up in self.power_ups[:]:
            if power_up.colliderect(paddle_rect):
                self.lives += 1
                self.power_ups.remove(power_up)
        if paddle_rect.colliderect(ball_rect):
            self.hit_paddle_sound.play()
            if self.ball_x < self.paddle_x + 40:
                self.ballDirection = 'UpLeft'
            else:
                self.ballDirection = 'UpRight'


    # SCREEN DISPLAYS

    def mainScreen(self):
        self.screen.fill((190, 143, 255))
        font = pygame.font.SysFont('Arial', 30)
        playerScore = font.render(str(int(self.score)), True, (255, 255, 255))
        self.screen.blit(playerScore, (400, 0))
        for i in range(self.lives):
            self.screen.blit(self.heart, (750 - (i * 30), 10))
        for brick in self.bricks:
            if brick["state"] == 0:
                self.screen.blit(brick["color"], brick["rect"].topleft)
            elif brick["state"] == 1:
                cracked_image = self.purple_bricks_cracked if brick["color"] == self.purple_bricks else self.grey_bricks_cracked
                self.screen.blit(cracked_image, brick["rect"].topleft)
        for power_up in self.power_ups:
            self.screen.blit(self.power_up, power_up.topleft)

        self.screen.blit(self.paddle, (self.paddle_x, self.paddle_y))
        self.screen.blit(self.ball, (self.ball_x, self.ball_y))
        pygame.display.update()

    def startScreen(self):
        introScreen = pygame.image.load("img/Breakout Tile Set Free/PNG/intro.png")
        self.screen.blit(introScreen, (0, 0))
        pygame.display.update()

    def pauseScreen(self):
        pauseS = pygame.image.load("img/Breakout Tile Set Free/PNG/pause.png")
        self.screen.blit(pauseS, (0, 0))
        font = pygame.font.SysFont('Arial', 30)
        playerScore = font.render(str(int(self.score)), True, (255, 255, 255))
        self.screen.blit(playerScore, (390, 265))
        pygame.display.update()

    def gameOverScreen(self):
        game_over = pygame.image.load("img/Breakout Tile Set Free/PNG/gameover.png")
        font = pygame.font.SysFont("Arial", 30)
        self.highScore()
        scoreText=font.render(str(int(self.score)), True, (255, 255, 255))
        highScoreText = font.render(str(int(self.high_score)), True, (255, 255, 255))

        self.screen.blit(game_over, (0, 0))
        self.screen.blit(scoreText, (387, 249))
        self.screen.blit(highScoreText, (387, 309))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.run()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        quit()
    # Complete reset
    def reset(self):
        self.ball_x, self.ball_y = 383, 540
        self.paddle_x, self.paddle_y = 350,548
        self.score = 0
        self.lives = 3
        self.generate_bricks()

    # Game run loop
    def run(self):
        self.reset()
        #self.generate_bricks()
        self.startScreen()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_started = True
                    elif event.key == pygame.K_SPACE and self.game_started:
                        self.ball_stop = False
                        self.paddle_stop=False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_p:
                        self.pause = not self.pause
            if not self.pause:
                if self.game_started:
                    self.mainScreen()
                    self.all_bricks_removed()
                    if not self.ball_stop:
                       self.ball_movement()

                    if not self.paddle_stop:
                        self.paddle_movement()
                        self.power_up_movement()
            else:
                self.pauseScreen()

        pygame.quit()

# Entry point
if __name__ == '__main__':
    game = Game()
    game.run()
