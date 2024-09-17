import pygame as pg
import time
import pickle

pg.init()
RES = WIDTH, HEIGHT = 500, 500
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()
FPS = 60
font = pg.font.Font('freesansbold.ttf', 32)
mouse_pos = (0, 0)
index = 0
score = [0, 0]
path = 'data/data'
    
    
def CountingPoints(pick1, pick2):
    if pick1 == pick2: return [0, 0]
    if pick1 == 'r':
        if pick2 == 's':
            return [1, 0]
        else: return [0, 1]
    if pick1 == 's':
        if pick2 == 'l':
            return [1, 0]
        else: return [0, 1]
    if pick1 == 'l':
        if pick2 == 'r':
            return [1, 0]
        else: return [0, 1]
    
class UI():
    def __init__(self):
        self.x, self.y = WIDTH//2, 150
        self.font48 = pg.font.Font('freesansbold.ttf', 48)
        self.font32 = pg.font.Font('freesansbold.ttf', 32)
        self.text = self.font48.render('SCORE : '+str(score[0])+' | '+str(score[1]), True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        self.rnd = ''
        self.button = [self.font32.render('VIEW STATS', True, (255, 255, 255)),
                    self.font32.render('VIEW STATS', True, (255, 255, 255)).get_rect(center=(WIDTH//2, 75)),
                    pg.Rect(WIDTH-30, 10, 20, 20)]

    def update(self):
        self.text = self.font48.render('SCORE : '+str(score[0])+' | '+str(score[1]), True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        pg.draw.rect(screen, (0, 0, 0), self.button[1], 0, 4)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.button[0], self.button[1])

    def new_turn(self, score):
        self.text = self.font48.render('NOBODY WON, TIE', True, (0, 0, 0))
        if score == [1, 0]:
            self.text = self.font48.render('PLAYER 1 WON', True, (0, 0, 0))
        if score == [0, 1]:
            self.text = self.font48.render('PLAYER 2 WON', True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        screen.fill((255, 255, 255))
        screen.blit(self.text, self.text_rect)
        pg.display.flip()
        time.sleep(1)
    def view_stats(self):
        file = open(path, 'rb')
        data = pickle.load(file)
        file.close()
        running = True
        while running:
            screen.fill((255, 255, 255))
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if self.button[2].collidepoint(mouse_pos) and event.type == pg.MOUSEBUTTONDOWN:
                    running = False
            for i in [('ROCK', 0), ('PAPER', 1), ('SCISSOR', 2)]: 
                text = self.font32.render(i[0]+' WINS : '+str(data[i[1]]), True, (0, 0, 0))
                rect = text.get_rect(center = (WIDTH//2, 50+i[1]*(HEIGHT)/3))
                screen.blit(text, rect)
            pg.draw.rect(screen, (255, 0, 0), self.button[2], 0, 4)
            pg.display.flip()
            clock.tick(FPS)
                
        
class Object():
    def __init__(self, x, y, type_of):
        self.x = x
        self.y = y 
        self.type_of = type_of
        if self.type_of == 'r': self.size = self.width, self.height = 100, 80
        else: self.size = self.width, self.height = 60, 80
        if self.type_of == 'r': self.image =  pg.image.load("ressources/pierre.jfif")
        if self.type_of == 's': self.image =  pg.image.load("ressources/ciseaux.jfif")
        if self.type_of == 'l': self.image =  pg.image.load("ressources/feuille.jfif")
        self.new_image = pg.transform.scale(self.image, self.size)
        self.rect = self.new_image.get_rect(center=(self.x, self.y))
    def update(self):
        self.new_image = pg.transform.scale(self.image, self.size)
        self.rect = self.new_image.get_rect(center=(self.x, self.y))
        screen.blit(self.new_image, self.rect)
        if self.rect.collidepoint(mouse_pos): 
            if self.size[0]<120:
                self.size = (self.size[0]+1, self.size[1]+1)
        else:
            if self.type_of == 'r': self.size = self.width, self.height = 100, 80
            else: self.size = self.width, self.height = 60, 80

        
            
class Player():
    def __init__(self, name):
        self.name = name
        self.pick = 0
        self.new_pick = 0
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.text = font.render(str(self.name)+' turn : ', True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(WIDTH//2, HEIGHT-200))
    def turn(self):
        screen.blit(self.text, self.text_rect)
        return True if self.new_pick != 0 else False
    
rock = Object(WIDTH//4, HEIGHT-80, 'r')
scissor = Object(WIDTH//2, HEIGHT-80, 's')
leaf = Object(WIDTH//2+WIDTH//4, HEIGHT-80, 'l')
players = [Player('Player 1'), Player('Player 2')]
ui = UI()

running = True
while running:
    screen.fill((255, 255, 255))
    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if rock.rect.collidepoint(mouse_pos):
                players[index].new_pick = 'r'
            if scissor.rect.collidepoint(mouse_pos):
                players[index].new_pick = 's'
            if leaf.rect.collidepoint(mouse_pos):
                players[index].new_pick = 'l'
            if ui.button[1].collidepoint(mouse_pos):
                ui.view_stats()
            
    if players[index].turn():
        if index<len(players)-1:
            players[index].pick = players[index].new_pick
            players[index].new_pick = 0
            index+=1
        else:
            players[index].pick = players[index].new_pick
            new_score = CountingPoints(players[0].pick, players[1].pick)
            score[0] += new_score[0]
            score[1] += new_score[1]
            players[index].new_pick = 0
            index = 0
            ui.new_turn(new_score)
            
            file = open(path, 'rb')
            data = pickle.load(file)
            print(data)
            file.close()
            if new_score != [0, 0]:
                player = players[new_score[1]]
                if player.pick == 'r': data[0] += 1
                if player.pick == 's': data[1] += 1
                if player.pick == 'l': data[2] += 1
            file = open(path, 'wb')
            pickle.dump(data, file)
            file.close()
            
    rock.update()
    scissor.update()      
    leaf.update()
    ui.update()
    
    pg.display.flip()
    clock.tick(FPS)
pg.quit()