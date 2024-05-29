import pygame
from sys import exit #closes any code when called
from random import randint, choice

dash_audio_counter = 1
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk1 = pygame.transform.scale(player_walk1, (64,84))
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        player_walk2 = pygame.transform.scale(player_walk2, (64,84))

        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_jump= pygame.transform.scale(self.player_jump, (64,84))


        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity =0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom =300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index =0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]


    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        self.animation_state()
        if self.rect.x <= -100:
            self.kill()




def display_score():
    current_time = int(pygame.time.get_ticks() /1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)

    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list: #check if empty list or not
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    global player_surf, player_index

    #if player isnt on the ground, else:
    if player_rect.bottom < 300:
        #jump
        player_surf = player_jump
    else:
        #walking
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
    #play walking animation is player is in floor
    #display jump surface when player is NOT on floor


pygame.init() #initialiing pygame

#display surface: tuple(width, height)
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Mitsuru's Dash")
clock = pygame.time.Clock()
#Font(font type, font size)
test_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(.2)
bg_music.play(loops= -1) #plays this sound infinitely




#groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()


sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
#render('text', Anti aliencing, color)
#score_surf = test_font.render('My game', False, (64,64,64))
#score_rect = score_surf.get_rect(center = (400, 50))

#snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames= [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list= []



player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()


player_surf = player_walk[player_index]
#Rect(left, top, width, height)
#get_rect-> draws rect based on image
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#intro screen
intro_text = test_font.render('Mitsuru\'s Dash', False, ('#FF9302'))
intro_text_rect = intro_text.get_rect(center = (400,80))


instruction_text = test_font.render('press space to run', False, ('#FF9302'))
instruction_text_rect  = instruction_text.get_rect(center = (400, 340))


player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rect = player_stand.get_rect(center = (400, 200))

#timer
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer, 200)



while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        if game_active:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom >= 300:
                        player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= 300:
                        player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int (pygame.time.get_ticks() /1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                #if randint(0,2):
                #    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100),300)))
                #else:
                #   obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]


    if game_active:


        if dash_audio_counter ==1:
            dash_audio = pygame.mixer.Sound('audio/dash.mp3')
            dash_audio.set_volume(.6)
            dash_audio.play()
            dash_audio_counter=0

        #block image transfer: tuple(surface, position (left, right || up, down))
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, 300))


        score = display_score()

        #snail_rect.x -= 4
        #if snail_rect.right <=0:
            #snail_rect.left = 800
        #screen.blit(snail_surf, snail_rect)


        #player
        #player_gravity+=1
        #player_rect.y += player_gravity #y axis
        #if player_rect.bottom >= 300:
        #    player_rect.bottom = 300
        #player_animation()
        #screen.blit(player_surf, player_rect)

        #sprites for player
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()


        #obstacle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        game_active = collision_sprite()
        #game_active = collisions(player_rect, obstacle_rect_list)

    else:

        dash_audio_counter=1
        screen.fill(('#EEE5E6'))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0



        score_message = test_font.render(f'Your previous score: {score}', False, ('#FF9302'))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(intro_text, intro_text_rect)

        if score == 0:
            screen.blit(instruction_text, instruction_text_rect)
        else:

            screen.blit(score_message, score_message_rect)


    #draw element
    #update everything
    pygame.display.update()
    clock.tick(60)