import pygame, random, time, pygame_menu
from pygame import mixer
from pygame_menu import themes

pygame.init()

WIDTH = 900
HEIGHT = 500
fps = 60
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)
yellow = (255, 255, 0)
pygame.display.set_caption("Flappy Space")

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 20)

mixer.init()
mixer.music.load('pygame\cs project\Music background   sound effect.mp3')
mixer.music.play()
#here all of the variables and lists are set
player_x = 225
player_y = 225
y_change = 0
jump_height = 12
gravity = .9
obstacles = [400, 700, 1000, 1300, 1600]
generate_places = True
y_positions = []
game_over = False
speed = 5
score = 0
high_score = 0
stars = []

class button():
    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    def changeColour(self, position):
        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)

    
def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)
    if difficulty == 1:
        print(speed)
    elif difficulty == 2:
        print(speed)



#when the game has started then this function opens the loading menu
def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)
    
    

def level_menu():
    mainmenu._open(level)


####menus

mainmenu = pygame_menu.Menu("Welcome to Flappy Space", WIDTH, HEIGHT, theme=themes.THEME_GREEN)
mainmenu.add.button("Play", start_the_game)
mainmenu.add.button("Levels", level_menu)
mainmenu.add.button("Quit", pygame_menu.events.EXIT)

level = pygame_menu.Menu("Select a Difficulty", WIDTH, HEIGHT, theme=themes.THEME_BLUE)
level.add.selector("Difficulty: ", [("Hard", 1), ("Easy", 2)], onchange=set_difficulty)

loading = pygame_menu.Menu("Loading the Game...", WIDTH, HEIGHT, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200)

###arrows
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10,15))

###events
update_loading = pygame.USEREVENT + 0




def draw_player(x_pos, y_pos):
    global y_change
    mouth = pygame.draw.circle(screen, gray, (x_pos + 25, y_pos+15), 12)
    play = pygame.draw.rect(screen, yellow, [x_pos,y_pos, 30, 30], 0, 12)
    eye = pygame.draw.circle(screen, black, (x_pos + 23, y_pos+12), 5)
    jetpack = pygame.draw.rect(screen, white, [x_pos-20, y_pos, 18, 28], 4, 2)
    if y_change<0:
        flame1 = pygame.draw.rect(screen, red, [x_pos-20, y_pos+29, 7, 20], 0, 2)
        flame1_yellow = pygame.draw.rect(screen, yellow, [x_pos-18, y_pos+30, 3, 18], 0, 2)
        flame2 = pygame.draw.rect(screen, red, [x_pos-10, y_pos+29, 7, 20], 0, 2)
        flame2_yellow = pygame.draw.rect(screen, yellow, [x_pos-8, y_pos+30, 3, 18], 0, 2)

    return play


def draw_obstacles(obst, y_pos, play):
    global game_over
    for i in range(len(obst)):
        y_coord = y_pos[i]
        top_rect = pygame.draw.rect(screen, gray, [obst[i], 0, 40, y_coord])
        top2 = pygame.draw.rect(screen, gray, [obst[i]-3, y_coord-20, 46, 20], 0, 5)
        bot_rect = pygame.draw.rect(screen, gray, [obst[i], y_coord+200, 40, HEIGHT - (y_coord+70)])
        bot2=pygame.draw.rect(screen, gray, [obst[i]-3, y_coord+200, 46, 20], 0, 5)
        if top_rect.colliderect(player) or bot_rect.colliderect(player):
            game_over = True


def draw_stars(stars):
    global total
    for i in range(total-1):
        pygame.draw.rect(screen, white, [stars[i][0], stars[i][1], 3, 3], 0, 2)
        stars[i][0] -= .5
        if stars[i][0] < -3:
            stars[i][0] = WIDTH+3
            stars[i][1] = random.randint(0, HEIGHT)
    return stars



running=True
while running:
    timer.tick(fps)
    screen.fill(black)

    

    if generate_places:

        for i in range(len(obstacles)):
            y_positions.append(random.randint(0, 300))
        total = 100
        for i in range(total):
            x_pos = random.randint(0, WIDTH)
            y_pos = random.randint(0, HEIGHT)
            stars.append([x_pos, y_pos])

        generate_places = False
    

    stars = draw_stars(stars)
    player = draw_player(player_x, player_y)
    draw_obstacles(obstacles, y_positions, player)

    events = pygame.event.get()
    for event in events:

        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() +1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
                mainmenu.disable()
        if event.type == pygame.KEYDOWN and progress.get_value() == 100:
            if event.key == pygame.K_SPACE and not game_over and player_y>0:
                y_change = -jump_height
                #if the spacebar is pressed and the game isnt over, then the change in the y direction is the jump height of the character
            if event.key == pygame.K_r and game_over:
                player_y = 225
                player_x = 255
                y_change = 0
                generate_places=True
                obstacles = [400, 700, 1000, 1300, 1600]
                y_positions = []
                score=0
                pygame.mixer.music.play()
                game_over=False
                #if 'm' is pressed and the game is over, then the game restarts from the beginning


        if event.type == pygame.QUIT:
            running = False
            #if the event is quit, then the variable running gets set to false - this stops the while loop as running is no longer true.

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(screen)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(screen, mainmenu.get_current().get_selected_widget())



    if player_y + y_change < HEIGHT-30:
        player_y +=y_change
        y_change+=gravity
    else:
        player_y = HEIGHT-30


    for i in range(len(obstacles)):
        if not game_over:
            obstacles[i] -= speed
            if obstacles[i]<-30:
                obstacles.remove(obstacles[i])
                y_positions.remove(y_positions[i])
                obstacles.append(random.randint(obstacles[-1] + 280, obstacles[-1] + 320))
                y_positions.append(random.randint(0, 300))
                score += 1
                #in this code, it is how the obstacles are continuosly spawning, as they are removed from the left as they past and appended
                #back to the end of the list, adding a constant value to their position.


    if score>high_score:
        high_score = score
        #if the current score becomes higher than the set high score, the this score will become the new high score.


    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart...", True, white)
        screen.blit(game_over_text, (200, 200))
        #when the user loses, a message pops up onto the screen to restart to game.

    score_text = font.render("Score: "  +str(score), True, white)
    screen.blit(score_text, (10, 450))
    highscore_text = font.render("High Score: "  +str(high_score), True, white)
    screen.blit(highscore_text, (10, 470))
    #this displays the final score and highscore at the end

    pygame.display.flip()
pygame.quit()

    

