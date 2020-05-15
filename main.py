import pygame as pg
import random 
import cv2
from settings import *
from sprites import *
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
N = 4

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name,size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.players.add(self.player)
        self.score = 0
        for i in range(0,N):
            m = Mob(self,((i+1)*WIDTH/N))
            self.all_sprites.add(m)
            self.mobs.add(m)
        self.run()
    
    def run(self):
        # Game Loop
        self.playing = True
        cap = cv2.VideoCapture(0)
        while self.playing:
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5)
            self.clock.tick(FPS)
            self.events()
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                self.update((img.shape[1]-(x + int(w/2) - 20))*2, (y + int(h/2))*2)
            self.draw(img)
            k = cv2.waitKey(30) & 0xff
            if k==27:
                break
        cap.release()

    def update(self, x, y):
        # Game Loop - Update
        self.players.update(x,y)
        self.mobs.update()
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            self.playing = False

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self, img):
        # Game Loop - draw
        self.screen.fill(BLACK)
        image = pg.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
        image = pg.transform.scale(image, (WIDTH,HEIGHT))
        self.screen.blit(image, (0,0))
        draw_text(self.screen, "Score: "+str(self.score), 20, 40, HEIGHT - 40)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def show_start_screen(self):
        # game splash/ start screen
        self.screen.fill(BLACK)
        self.go = True
        while self.go:
            draw_text(self.screen, "Press Any Key to continue",40, WIDTH/2,HEIGHT/2)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.go = False
                if event.type == pg.QUIT:
                    self.running = False
                    self.go = False

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BLACK)
        self.go = True
        while self.go:
            draw_text(self.screen, "Press Any Key to continue",40, WIDTH/2,HEIGHT/2)
            draw_text(self.screen,"Score: "+str(self.score),20,WIDTH/2,HEIGHT/2 + 50)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.go = False
                if event.type == pg.QUIT:
                    self.running = False
                    self.go = False
g = Game()
g.show_start_screen()
# g.show_go_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()