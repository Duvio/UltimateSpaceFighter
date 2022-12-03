"""
Copyright (C) 2022  Ben Baule

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
"SpaceShip" by pitrizzo licensed GPL 3.0: opengameart.org/content/spaceship-1
"Snowball Pixel Art" by alf0186 licensed CC0: opengameart.org/content/snowball-pixel-art
"Blaster bolt" by AlejandroHaibi licensed CC0: opengameart.org/content/blaster-bolt
"Space Backgrounds" by Rawdanitsu licensed CC0: opengameart.org/content/space-backgrounds-3
"alien" by Carlos Alface licensed CC-BY 3.0: opengameart.org/content/alien-1
"""


import pygame, time


BLACK = (0, 0, 0)
RED = (0,255,0)
W = 640
H = 480



class shot:
    def __init__(self, posX, posY, movY, isSuperShot):
        self.posX = posX
        self.posY = posY
        self.movY = movY
        self.width = 25
        self.height = 25
        self.lives = 1
        self.isSuperShot = isSuperShot
        if isSuperShot:
            self.width = 100
            self.height = 100
            self.lives = 3
            
    def update(self):
        self.posY += self.movY
        
    def getRect(self):
        return pygame.Rect(self.posX, self.posY, self.width, self.height)



def tastatur():
    global gameActive, quitGame, alienMovX, rocketMovX, alienPosX, alienWidth, alienPosY, alienHeight, rocketPosX, rocketWidth, rocketPosY, laserShots, cannonballShots
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            gameActive = False
            quitGame = True
        
        #movement/weapon keys pressed
        elif event.type == pygame.KEYDOWN:
            #movement keys
            if event.key == pygame.K_LEFT:
                alienMovX -= 10
            elif event.key == pygame.K_RIGHT:
                alienMovX += 10
            if event.key == pygame.K_a:
                rocketMovX -= 10
            elif event.key == pygame.K_d:
                rocketMovX += 10
            
            #weapon keys
            if len(laserShots) < 3:
                if event.key == pygame.K_UP:
                    laserShots.append( shot(alienPosX + alienWidth / 2 - 10, alienPosY + alienHeight - 20, 10, False))
                if event.key == pygame.K_DOWN:
                    laserShots.append( shot(alienPosX + alienWidth / 2 - 45, alienPosY + alienHeight - 20, 5, True))
            if len(cannonballShots) < 3:
                if event.key == pygame.K_w:
                    cannonballShots.append( shot(rocketPosX + rocketWidth/2 - 10, rocketPosY + 15, -10, False))
                if event.key == pygame.K_s:
                    cannonballShots.append( shot(rocketPosX + rocketWidth/2 - 45, rocketPosY-15, -5, True))
                    
        #movement keys release
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                alienMovX += 10
            elif event.key == pygame.K_RIGHT:
                alienMovX -= 10
            if event.key == pygame.K_a:
                rocketMovX += 10
            elif event.key == pygame.K_d:
                rocketMovX -= 10


def updateMovement():
    global rocketPosX, alienPosX

    rocketPosX += rocketMovX
    alienPosX += alienMovX
    
    for l in laserShots:
        l.update()
        if l.posY > H:
            laserShots.remove(l)
    
    for c in cannonballShots:
        c.update()
        if c.posY < 0:
            cannonballShots.remove(c)


def borderCheck():
    global rocketPosX, rocketWidth, W, alienPosX, alienWidth
    #check borders of rocket
    if rocketPosX+rocketWidth > W:
        rocketPosX = W-rocketWidth
    elif rocketPosX < 0:
        rocketPosX = 0
    
    #check borders of alien
    if alienPosX+alienWidth > W:
        alienPosX = W-alienWidth
    elif alienPosX < 0:
        alienPosX = 0


def drawScreen():
    global rocketPosX, rocketPosY, alienPosX, alienPosY, rocketf, alienf
    
    screen.fill(BLACK)
    
    start = time.time()
    backgroundf = screen.blit(background, (0, 0))
    print("bgblit", time.time()-start)

    rocketf = screen.blit(rocket_small, (rocketPosX, rocketPosY))
    alienf = screen.blit(alien_small, (alienPosX, alienPosY))

    for l in laserShots:
        if not l.isSuperShot:
            screen.blit(laser_small, (l.posX - 32, l.posY - 10))
        else:
            screen.blit(laser_super, (l.posX - 82, l.posY - 20))
        
    for c in cannonballShots:
        if not c.isSuperShot:
            screen.blit(cannonball_small, (c.posX, c.posY))
        else:
            screen.blit(cannonball_super, (c.posX, c.posY))


def collisionCheck():
    global gameActive, laserShots, cannonballShots
    for l in laserShots:
        if rocketf.colliderect(l.getRect()):
            print("Aliens won!")
            gameActive = False
            
    for c in cannonballShots:
        if alienf.colliderect(c.getRect()):
            print("Humans won!")
            gameActive = False
            
    for c in cannonballShots:
        for l in laserShots:
            if c.getRect().colliderect(l.getRect()):
                l.lives -= 1
                c.lives -= 1
                if l.lives == 0:
                    laserShots.remove(l)
                if c.lives == 0:
                    cannonballShots.remove(c)



def gameLoop():
    global quitGame, gameActive, rocketMovX, rocketMovY, rocketPosX, rocketPosY, alienMovX, alienMovY, alienPosX, alienPosY 
    while gameActive:
        tastatur()

        updateMovement()

        borderCheck()

        drawScreen()

        collisionCheck()

        pygame.display.flip()

        clock.tick(30)




if __name__ == "__main__":
    pygame.init()

    quitGame = False
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Ultimate Space Fighter")
    
    rocket = pygame.image.load("./assets/rocket.png")
    rocket_small = pygame.transform.scale(rocket, (75, 75))
    rocketWidth = rocket_small.get_rect()[2]
    rocketHeight = rocket_small.get_rect()[3]

    alien = pygame.image.load("./assets/alien.png")
    alien_small = pygame.transform.scale(alien, (75, 75))
    alienWidth = alien_small.get_rect()[2]
    alienHeight = alien_small.get_rect()[3]

    cannonball_small = pygame.transform.scale(pygame.image.load("./assets/snowball.png"), (25, 25))
    cannonball_super = pygame.transform.scale(pygame.image.load("./assets/snowball.png"), (100, 100))
    cannonballWidth = cannonball_small.get_rect()[2]
    cannonballHeight = cannonball_small.get_rect()[3]

    laser_small = pygame.transform.scale(pygame.image.load("./assets/laser.png"), (100, 45))
    laser_super = pygame.transform.scale(pygame.image.load("./assets/laser.png"), (300, 150))
    laserWidth = laser_small.get_rect()[2]
    laserHeight = laser_small.get_rect()[3]
    
    background = pygame.transform.scale(pygame.image.load("./assets/SpaceBackground.jpg").convert(), (W, H))

    alienMovX = 0
    alienMovY = 0

    rocketMovX = 0
    rocketMovY = 0
        
    while True:
        gameActive = True

        rocketPosX = W/2
        rocketPosY = H-20-rocketHeight

        alienPosX = W/2
        alienPosY = 20
        
        laserShots = []
        
        cannonballShots = []

        gameLoop()

        if quitGame:
            break


pygame.quit()