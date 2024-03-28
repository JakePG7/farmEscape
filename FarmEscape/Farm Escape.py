# Farm Escape
# A platforming game, use the arrow keys to jump on cutting boards and avoid knives
# Creator: Jake Prins-Gervais
# Date: 11/06/2020

import random 
from random import randint # so that I didn't have to type "random." infront of every randint
import pygame 
from pygame.locals import* # So that I didn't have to type "pygame." infront of every KEYDOWN or KEYUP, etc...
import pygame.mixer # So that I can use sounds

pygame.mixer.init() # initiates the sound mixer
clock = pygame.time.Clock()

# Sets the screen size
screenBase = 590 # I use base and height instead of length and width, just a preference
screenHeight = 620
size = screenBase, screenHeight
screen = pygame.display.set_mode(size)

# Importing Sounds
soundName = ["Caching", "Cart", "Chop", "Coin", "Falling", "In-Cart", "Intro", "Jump", "Negative", "Shop", "Text"] # Names for the wav files without the .wav part
soundLibrary = [] # Will store all of the sound locations
for i in range(len(soundName)):
    soundLibrary.append(pygame.mixer.Sound("Sound " + soundName[i] + ".wav")) 
soundLibrary[7].set_volume(0.2) # Sets the jump volume lower (it was very loud originally)

def load(n): #Function that loads the images for the variables, with it's only parameter being the index of the png name in the names array
    return(pygame.image.load(names[n] + ".png"))
names = ["farm", "dirt ground", "Vegetable Sign", "ExitButton", "ShopButton", "Press Space", "Press Reset", "Big Coin", "Shopping Cart", "Score Font", "HighScore", "m", "Glow", "Exit Shop", "Purchase", "Selected", "Tag"] # Names of the pngs without the .png part

# Title screen and Background Images         
background = load(0) # Each uses the load function, so that I don't have to write "pygmae.image.load() a bunch of times
dirt = load(1)
icon = load(2)
saveButton = load(3)
shopButton = load(4)
spaceStart = load(5)
spaceReset = load(6)

# In-Game Non-Object Images
bigCoin = load(7)
bCoinDim = 40 # Image is a square, so the base and the height are the same 
cart = load(8)
scoreWord = load(9)
scoreWordWidth = 202
highScoreWord = load(10)
highWordWidth = 252
m = load(11)
mWidth = 34
glow = load(12)
mGlow = pygame.transform.scale(glow, (35, 35)) # The glow behind the m is smaller than the other ones, so I transformed it

# Shop Images
shelf = pygame.image.load("Shelf.jpg") # This is a jpg file, so I didn't use the load function for it
exitShop = load(13)
buyButton = load(14)
selected = load(15)
tag = load(16)

# Individual Score and bank Number Images
numbers = [] # Where the purple number images will be stored
cNumbers = [] # Where the yellow number images will be stored
numbersWidth = [] # The different colour numbers have the same sizes, so they can share a "width array"

for i in range(10): # there are 10 digits, so it will loop 10 times
    currentI = pygame.image.load(str(i) + ".png") # turns the index number into a string, since all the file names begin with a number and end with .png
    numbers.append(currentI)
    currentI_width, currentI_height = currentI.get_size()
    numbersWidth.append(currentI_width) # stores the width of the digit in the width array
    
    currentI = pygame.image.load(str(i) + "C.png") # Same goes for the coin numbers
    cNumbers.append(currentI)
numberHeight = 50

purchasedSkins = [True] # The purchased array always begins with one true, because the tomato skin is always bought
try: # Sees if there is a save file
    reader = open("Farm Escape Save.txt", "r") # reads the save text file
    highscore = int(reader.readline().strip()) 
    bank = int(reader.readline().strip())
    selectedSkin = int(reader.readline().strip())
    for i in range(5):
        purchasedSkins.append(bool(reader.readline().strip())) # if there is nothing on the line other than a \n, the purchased boolean will be set to False, otherwise True
    reader.close() # Closes the reader
except FileNotFoundError: # If there is no save file, it will set default variables
    highscore = 0
    bank = 0
    selectedSkin = 0
    for i in range(5): 
        purchasedSkins.append(False) # All skins will be set to not purchased, except for the tomato regularly

# Object Classes (Will explain the basics on the first class)
class Board: # Cutting Boards
    def __init__(self, x, y): # initializes the board object, with the x and y parameters
        self.x = x
        self.y = y
        self.image = pygame.image.load("cutting board.png") # loads the object images in the class instead of in the beginning of the program
        self.base = 175 
        self.height = 51   
        
    def checkPos(self): # The first class method, that only the Board objects can access
        global boardNeeded # This boardNeeded boolean is changed inside and outside of the method, therefore the global variable must be called into the function
        if self.y < 0 and self.y > -250: 
            boardNeeded = False # If there is a board between y -250 and 0, no board will spawn
        if self.y > 800: 
            self.x = 1000 # If a board is 180 pixels below the screen, it's x will be set to 1000, making it unusable
            
    def checkImpact(self, player): # A player will need to be set as a parameter when called to run properly
        global jumpY, prejumpY, dirtY, dirtX, jumpTimer, lastFloorY # See line 97
        if player.y + player.height >= self.y + 5 and player.y <= self.y - player.height / 1.5 and player.x + player.base / 3 < self.x + 206 and player.x + 2 * (player.base / 3) > self.x and preJumpY > jumpY or player.y + player.height >= dirtY and dirtX != 1000: # First hit box, if the player intersects the top of the board, and the player is going down, or the player lands back on the dirt
            soundLibrary[7].play() # jump Sound
            jumpTimer = 0 # x coordinate on the jump shape parabola will be set to 0, where it restarts
            lastFloorY = player.y 
 
# There is only ever 2 Player objects       
class Player: 
    def __init__(self, x, y, s): # s = selectedSkin
        self.x = x
        self.y = y
        self.image = pygame.image.load(pngNames[s] + ".png")
        self.base, self.height = self.image.get_size()
        self.speed = 0 # How much the player's x moves
        
    def moveToCenter(self): # When the player is falling and it must be ready to fall into the cart
        if self.x > 255:
            self.x -= 20 #If player[0] is to the right of 255, it will move to the left by 20 pixels
            player[1].x -= 20 # Both players must be at the same coordinates during the ending
        elif self.x < 215:
            self.x += 20 # Opposite of line 120
            player[1].x += 20
        else:
            self.x = 235 # Sets the exact position when the player is between x 215 and 255 
            player[1].x = 235 
            
    def cartMovement(self): # I decided to not make the cart an object, as it never has it's own attributes, but shares another's (copy's dirt and player actions)
        global playInCartSound, tickCounter, cartX, squeakCounter, finalScores 
        if self.y <= 380: # If the object is not in the cart, lower it by 2 pixels
            self.y += 2
            playInCartSound = True
        elif playInCartSound == True: # The player Y must also be > 380
            soundLibrary[4].stop() # stops the falling sound
            soundLibrary[5].play()
            playInCartSound = False # So that the sound doesn't repeat
        else: # Player is now in the cart
            if tickCounter < 60: # Waits one second to move, since there are 30 ticks per second and this loops twice per tick
                tickCounter += 1 # will increase by 1 everytime it goes through the loop
            else: # if it's been a second
                if cartX < screenBase: # If the cart is still on the screen
                    self.speed = 5 
                    cartX += 2.5 # Increases by half the player's speed Because there are two players, so this movement will happen twice
                    if squeakCounter % 120 == 0: # The squeak sound will play every 2 seconds (remember, it counts twice)
                        soundLibrary[1].play()
                    squeakCounter += 1
                else:
                    self.speed = 0 # Player and cart stops moving off-screen
                if cartX >= 500:
                    finalScores = True 
                    
    def checkOffScreen(self): 
        if self.x + self.base > screenBase: # If the left of the player[0] is further right than the right of the screen
            player[1].x = self.x - screenBase # player 1 will be sent to the opposite side of the screen
        elif self.x < 0: #opposite scenario of line 154 - 155
            player[1].x = self.x + screenBase
        if self.x > screenBase or self.x < -self.base: 
            self.x = player[1].x # if player[0] is off the screen, it will take player[1]'s position
        elif player[1].x > screenBase or player[1].x < -self.base:
            player[1].x = self.x # Vice versa  
            
    def checkSkin(self, s): # Makes sure that the player's image is up to date (parameter "s" is selected skin)
        self.image = pygame.image.load(pngNames[s] + ".png")
 
# Fying knife objects       
class Knife: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("Knife.png")        
        self.base = 120
        self.height = 50
        self.moving = True # Explained in checkPos Function
        self.left = False # Explained in directionCheck Function
        
    def checkImpact(self, player): # Knife-to-player hit box
        global dead
        if player.y + player.height >= self.y and player.y <= self.y - self.height and player.x + player.base / 4 <= self.x + self.base and player.x + 3 * (player.base / 4) >= self.x and dead == False:
            soundLibrary[2].play() # If the the player hits the knife in the last 3 quarters of the knife (the blade), and the player is not already dead, the chop sound will play
            dead = True # Will not let the player bounce off the cutting boards  
    
    def checkPos(self, board): # See cutting board checkPos (line 97) for basic explanation
        global knifeNeeded, score
        if (board.y < 0 or board.y > -100) and (self.y < 2000 or self.y < 1000 and score > 10000): # will not spawn if any boards are between y 0 and -100, and spawns every 2000m, until your score reaches above 10000, then it spawns every 1000m
            knifeNeeded = False
        if self.y > 800:
            self.x = 1000
            self.moving = False # knife movement is stopped, so it doesn't creep back on the screen
            
    def directionCheck(self):
        if self.x + self.base >= screenBase: 
            self.image = pygame.transform.flip(self.image, True, False) #Image is flipped from right to left
            self.left = True
        if self.x <= 0:
            self.image = pygame.transform.flip(self.image, True, False) # Image will flipped from left to right
            self.left = False
        if self.left == True:
            self.x -= 5 # Moves left
        elif self.left == False:     
            self.x += 5 # Moves right     

# Small coin objects that appear in-game
class Coin: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("Coin.png")
        self.base = 20
        self.height = 20
        
    def checkPos(self, board): # See line 97 and 183 for basic explanation
        global nextCoinYDiff, coinNeeded
        if self.y < nextCoinYDiff: # If a coin's y is less than the randomly-generated coin difference value, a coin will not be needed
            coinNeeded = False 
        if self.y > 800:
            self.x = 1000        
        if board.y < 0 and board.y > -100: 
            coinNeeded = False    
            
    def checkImpact(self, player): 
        global bank
        if player.y + player.height >= self.y and player.y <= self.y - self.height and player.x <= self.x + self.base and player.x + player.base >= self.x: #If the player intersects a coin
            soundLibrary[3].play() # coin sound
            self.x = 1000 # coin dissapears
            bank += 1 

# The clickable skins in the shop 
class ShopSkin:
    def __init__(self, x, y, p, b): # b stands for boolean
        self.x = x
        self.y = y
        self.image = pygame.image.load(pngNames[i] + ".png")
        self.base, self.height = self.image.get_size()
        self.price = p
        self.purchased = b
        self.index = len(totalShopSkins) # Used in the checkSkinPressed Method
        
    def checkSkinPressed(self, s): # selectedSkin int parameter
        if mouseX > self.x and mouseX < self.x + self.base and mouseY > self.y and mouseY < self.y + self.height: # if skin pressed
            s = self.index
        return(s) # if the if statement is skipped, the selected skin will be returned as it was
            
def XY(o): # Is used for multiple objects, so the object is a parameter
    return(o.x, o.y)
            
def calculateJump(x, y): 
    y = -(x - 18) ** 2 + 324 # Quadratic expression that tells the jumpY function how much it should increase or decrease an object's y to create a jump-like motion
    return (y)
                              
def scroll(o, d): # o = object (board, coin or knife), d = direction (up or down)
    if d == "Up": 
        o.y += jumpY - preJumpY # increases the object's y by the change between the last jumpY and the current one
    else:
        o.y -= preJumpY - jumpY # Opposite from line 253
        
def endScroll(): 
    global endDirtY, cartY, backY, useEndBack, endBackY, startGame
    if endDirtY != 540: # moves the dirt up by 20 pixles until it reaches y 540
        endDirtY -= 20
    if cartY != 370: # cart does the same as the dirt
        cartY -= 20
    if backY < screenHeight: # If the background is still on the screen
        if backY >= 368:
            backY -= (preJumpY - jumpY) / 16 # back will move the dirt up 16 times slower than the jump speed, which is very fast at this point
    else: # if back was not visible when the player fell
        useEndBack = True 
        if endBackY != 368:
            endBackY -= 20
    if (useEndBack == True and endBackY == 368 or useEndBack == False and backY <= 368) and cartY == 370 and endDirtY == 540:
        startGame = False  # will end the game when all the objects ready for the cart movement animation

def colourChange(t): 
    global r, g, b, scoreGlow
    if t == "toDark": 
        if g != 29: # decreases the rgb values proportionately from 92, 139, 215 (medium blue) to 26, 29, 105 (dark blue)
            r -= 0.6
            g -= 1
            b -= 1   
            
    elif t == "toMid": 
        if r != 92: # (read line 260) ... from 204, 230, 243 (light blue) to 92, 139, 215 (medium blue)
            r -= 1
            g -= 0.8125
            b -= 0.25 
        else:
            scoreGlow = True 
            
    elif t == "fromDark":
        r += 4.8 # ... from dark blue to medium blue
        g += 8
        b += 8
        
    elif t == "fromMid":
        r += 8 # ... from medium blue to light blue
        g += 6.5
        b += 2       
        
    else: # if t == "normal" / lightblue
        r = 204
        g = 230
        b = 243  
        
# The Two Score Functions (Very complicated)
def firstNumPlacement(n, a, m, e, d): # n = number to use, a = alignment on screen, m = midpoint (for center alignment), e = extra words or units that increase the width, d = distance from screen edge (for left and right alignment)  This function is for finding the x of the left side of a displayed number. some of these inputs will be 0, because they are not needed for the specific case
    soloNums = []
    for letter in str(n): # Each letter in the variable is seperated into individual strings, so it can be assigned an image
        soloNums.append(letter)
    if a != "left": # the width of a num with left alignment is not needed to find the left side's x
        width = e #adds all extra widths
        for i in range(len(soloNums)):
            width += numbersWidth[int(soloNums[i])] #adds width of each number
    if a == "center": 
        placementX = m - width / 2  # The first image in this number will be placed at the x of the reference middle subtraced by half the width of the entire number
    elif a == "right":
        placementX = screenBase - width - d 
    else: # t == left
        placementX = d
    return(placementX, soloNums) #returns the x value for the first image in the number and the list of individual numbers (needed later)

def drawNums(n, t, x, y, g): # n = numbers, t = type of numbers (coin or not), g = glowBool
    for i in range(len(n)):
        if g == True: # Only true for Score
            screen.blit(glow, (x - 5, y - 5)) # The is 10 pixels bigger on both dimensions, so the image is drawn 5 pixels eariler than the numbers both ways
        screen.blit(t[int(n[i])], (x, y)) 
        x += numbersWidth[int(n[i])] # sets up the x value for the next number
    return(x) # Returns the drawX incase a unit follows the numbers (an m or a big coin)

# The Game Loop
reset = True # Had variable declaration in the game loop so that the game could restart while still open
gameOn = True
while gameOn:
    clock.tick(30)
    
    # Variable declarations
    if reset == True:
        r = 204
        g = 230
        b = 243 # rgb begins as light blue
        shopBrown = 143, 66, 38
        
        startGame = False
        pngNames = ["Tomato", "Apple", "Orange", "Broccoli", "Pineapple", "Grape"]
        player = []     
        for i in range(2): # the two players are created
            player.append(Player(10, 445, selectedSkin))
        lastFloorY = 425
        totalBoards = []
        startBoard = True
        totalKnives = []
        dead = False
        totalCoins = []
        nextCoinYDiff = 0
        dirtY = 540
        dirtX = 0
        backY = 358
        rPressed = False
        lPressed = False
        scrollUp = False
        scrollDown = False
        end = False
        useEndBack = False
        endBackY = 1368
        endDirtY = 1540 
        cartX = 170
        cartY = 1370
        jumpTimer = 0
        jumpY = 0
        score = 0
        scoreGlow = False
        shop = False
        shopPlayerX = [40, 180, 45, 180, 50, 180]
        shopPlayerY = [57, 57, 268, 268, 460, 460]   
        skinPrice = [0, 20, 50, 80, 100, 150]
        totalShopSkins = []
        for i in range(6): # shopSkin objects are created even if not in the shop yet
            totalShopSkins.append(ShopSkin(shopPlayerX[i], shopPlayerY[i], skinPrice[i], purchasedSkins[i]))        
        finalScores = False
        mousePress = False
        playFallingSound = True
        introSongPlay = True
        firstTextSound = True
        secondTextSound = True
        thirdTextSound = True
        tickCounter = 0
        squeakCounter = 0
        resetReady = False 
        reset = False # reverts back to false, so that it doesn't state them everytime the gameloop loops

    if shop == False: 
        if startGame == True: 
            
            #Spawn First Boards
            if startBoard == True:
                totalBoards.append(Board(randint(0, 415), 300)) # creates two new Board objects at randomly generated x's
                totalBoards.append(Board(randint(0, 415), 0))
                startBoard = False # So it doesn't repeat this after the game starts
                
            #Object Position Checkers and send x to 1000s
            boardNeeded = True 
            knifeNeeded = True
            coinNeeded = True
            for i in range(len(totalBoards)): # Checks every board's position
                totalBoards[i].checkPos() # Checks if a board is needed
                for j in range(len(totalKnives)): # nested in the totalBoards loop, so that it can check each board's position and knife position
                    totalKnives[j].checkPos(totalBoards[i])
                for j in range(len(totalCoins)): # same as line 411
                    totalCoins[j].checkPos(totalBoards[i])
            if dirtY >= 1040: # When the first board dissapears
                dirtX = 1000                    
        
            # Spawners
            if boardNeeded == True: 
                totalBoards.append(Board(randint(0, screenBase - totalBoards[0].base), randint(-250, -100))) # Randomly spawns, and has to be between -250 and -100, so that the closest two boards can be is 100 pixels and the furthest possible is 250
            if coinNeeded == True:
                totalCoins.append(Coin(randint(20, 550), randint(-80, -40))) # because it spawns at a different spot than the board, they should not intersect
                nextCoinYDiff = randint(200, 1200) # Sets new distance from the next coin
            if knifeNeeded == True and score > 2000: 
                totalKnives.append(Knife(randint(0, 470), -75)) # It's ok if the coin and knife intersect, so as long as the boad and knife don't intersect
                
            # Checks hit box interactions with the player
            if dead == False: # The player will not interact with any objects if they are dead
                for i in range(len(player)):
                    for j in range(len(totalKnives)): # nested in player length, because there might be 2 players on screen
                        totalKnives[j].checkImpact(player[i])
                    for j in range(len(totalBoards)): 
                        totalBoards[j].checkImpact(player[i])    
                    for j in range(len(totalCoins)):
                        totalCoins[j].checkImpact(player[i])
            
            # Moving the objects
            preJumpY = jumpY
            jumpTimer += 1 # Represents the amount of ticks since the player has touched ground or a board
            jumpY = calculateJump(jumpTimer, jumpY) # x represents time in ticks, y represents height from last ground in pixels
            
            # Scroll Up
            if player[0].y <= 150 and preJumpY < jumpY: # If the player moves any higher than 149 and the jump motion is still increasing
                for i in range(len(totalBoards)):
                    scroll(totalBoards[i], "Up") 
                for i in range(len(totalCoins)):
                    scroll(totalCoins[i], "Up")                  
                for i in range(len(totalKnives)):
                    scroll(totalKnives[i], "Up")                     
                dirtY += jumpY - preJumpY
                backY += (jumpY - preJumpY) / 16 # the background scrolls 16 times slower than any other image
                lastFloorY += jumpY - preJumpY # Since the platforms have moved, the change of the jumpY must be added to the x of the last ground the player has jumped on 
                
                # Score increaser + Background Colour Change
                if score < dirtY - 540: # The score is the dirt distance from it's starting y value, the score is adjusted if it is less than this value
                    score = dirtY - 540            
                if score > 20000: 
                    colourChange("toDark")
                elif score > 10000:
                    colourChange("toMid")
                        
                if score > highscore: 
                    highscore = score                  
                        
            # Scroll Down
            elif player[0].y >= 350 and preJumpY > jumpY and (dirtY - (preJumpY - jumpY) >= 540 or dirtX == 1000): # The player cannot exeed a y value of 350, it will scroll instead
                for i in range(len(totalBoards)):
                    if player[0].y > totalBoards[i].y and totalBoards[i].x == 1000: # The game will end if the player is below a board that has already disapeared
                        end = True
                    
                # Scroll Down Non-Player Objects
                for i in range(len(totalBoards)):
                    if end == False or totalBoards[i].y > -totalBoards[i].height:
                        scroll(totalBoards[i], "Down")
                for i in range(len(totalCoins)):
                    if end == False or totalCoins[i].y > -totalCoins[i].height:
                        scroll(totalCoins[i], "Down")                    
                for i in range(len(totalKnives)):
                    if end == False or totalKnives[i].y > -totalKnives[i].height:
                        scroll(totalKnives[i], "Down")
                if end == False:
                    backY -= (preJumpY - jumpY) / 16
                    dirtY -= preJumpY - jumpY
                    lastFloorY -= preJumpY - jumpY                
                    
            else: # if the screen does not need to scroll
                for i in range(len(player)):
                    player[i].y = lastFloorY - jumpY # both player's scroll (I didn't think this was necessary to put in the player class)
                    
            #Ending sequence
            if end == True:
                for i in range(len(player)):
                    player[i].speed = 0 # user can no longer control the player's speed
                if playFallingSound == True:
                    soundLibrary[4].play()
                    playFallingSound = False
                scoreGlow = False
                if b >= 241: # Reason mentioned in colourChange function
                    colourChange("normal")               
                elif g < 139:
                    colourChange("fromDark")
                elif r < 204:
                    colourChange("fromMid")                  
                    
                # Moves Player to center at Ending
                player[0].moveToCenter()
                    
                # Back images scroll up to be in the frame
                endScroll()           
                
        # Places player in the cart        
        elif end == True and startGame == False:
            player[1].x = player[0].x # The player will now only see one player
            for i in range(len(player)):
                player[i].cartMovement()
        # End of end sequence (other than final scores)
        
        if startGame == True or end == False: # Player can move during the title screen and in-game   
            # Player X Changer if Off-Screen
            player[0].checkOffScreen()
        
        # Player X Changer for speed
        for i in range(len(player)):
            player[i].x += player[i].speed 
            
        # Knife X changer
        for i in range(len(totalKnives)):
            if totalKnives[i].moving == True:
                totalKnives[i].directionCheck()          
    
        # Drawing the images to the screen, the order of the blits are based on how they are layered on-screen
        # Background Blits
        skyblue = r, g, b
        screen.fill(skyblue)
        if end == True:
            if useEndBack == True: # Explained in the endScroll function
                screen.blit(background, (0, endBackY))
            else:
                screen.blit(background, (0, backY))        
            screen.blit(dirt, (0, endDirtY))
        else:
            screen.blit(background, (0, backY))
            screen.blit(dirt, (dirtX, dirtY))
        
        # Object blits
        for i in range(len(totalCoins)):
            screen.blit(totalCoins[i].image, XY(totalCoins[i]))   
        for i in range(len(totalBoards)):
            screen.blit(totalBoards[i].image, XY(totalBoards[i]))     
        for i in range(len(totalKnives)):
            screen.blit(totalKnives[i].image, XY(totalKnives[i]))   
        for i in range(2):
            player[i].checkSkin(selectedSkin)
            screen.blit(player[i].image, XY(player[i]))
            
        screen.blit(cart, (cartX, cartY))
        
        # Score Blits (The score blit system is a bit confusing)
        # In-Game Score 
        if startGame == True:
            drawX, soloNums = firstNumPlacement(score, "left", 0, 0, 10) # uses the score variable, and aligns with the left side of the screen, and is 10 pixels from the left edge of the screen
            drawX = drawNums(soloNums, numbers, drawX, 10, scoreGlow) # the numbers are drawn 
            if scoreGlow == True:
                screen.blit(mGlow, (drawX - 5, 10 + numberHeight / 2 - 5)) # "- 5" (see line 329) and the rest calculates the y placement so that the image to be in the middle of the numbers
            screen.blit(m, (drawX, 10 + numberHeight / 2)) # numberHeight / 2 is always 25
            
        # End Score
        if finalScores == True:
            soundLibrary[1].fadeout(4)
            drawX, soloNums = firstNumPlacement(score, "center", screenBase / 2, scoreWordWidth + mWidth, 0) # aligned to the center, so the midpoint and extra image parameters are important this time
            screen.blit(scoreWord, (drawX, 100)) # this word must be drawn before the numbers
            drawX += scoreWordWidth
            drawX = drawNums(soloNums, numbers, drawX, 100, False)
            screen.blit(m, (drawX, 100 + numberHeight / 2)) 
            
            if firstTextSound == True: # plays sound when score is displayed
                soundLibrary[10].play()
                firstTextSound = False
            if tickCounter != 100: # will stop counting ticks once it reaches 100
                tickCounter += 1
            if tickCounter >= 80: # waits 20 ticks to display high score
                
                # High Score
                drawX, soloNums = firstNumPlacement(highscore, "center", screenBase / 2, highWordWidth + mWidth, 0) # Placement is calculated
                screen.blit(highScoreWord, (drawX, 200)) 
                drawX += highWordWidth
                drawX = drawNums(soloNums, numbers, drawX, 200, False) 
                screen.blit(m, (drawX, 200 + numberHeight / 2)) 
                
                if secondTextSound == True: # PLays sound when highscore is displayed
                    soundLibrary[10].play()
                    secondTextSound = False
                    
                if tickCounter == 100:
                    screen.blit(spaceReset, (48.5, 350)) # "Press space to reset" will apear
                    if thirdTextSound == True: # Plays last sound
                        soundLibrary[10].play()
                        thirdTextSound = False
                    resetReady = True # The user can now reset the game
        
        # Title Screen Blits
        if end == False and startGame == False:
            screen.blit(icon,(45, 30))
            screen.blit(shopButton, (130, 330)) # Most title screen and shop images' x and y values were not calculated placements, just whatever looked nice (indicated with *n)
            screen.blit(saveButton, (300, 330)) # *n
            screen.blit(spaceStart, (109, 575)) # *n 
            if introSongPlay == True:
                soundLibrary[6].play()
                introSongPlay = False
                
    # Shop Blits
    else: # If shop == True
        # Shop Static Images
        screen.fill(shopBrown)
        screen.blit(shelf, (0, 0)) 
        screen.blit(exitShop, (335, 532)) # *n
        
        # Shop Non-static Images
        if totalShopSkins[selectedSkin].purchased == False:
            screen.blit(tag, (340, 335)) # *n
            screen.blit(buyButton, (335, 450)) # *n
            # Skin Price
            drawX, soloNums = firstNumPlacement(totalShopSkins[selectedSkin].price, "center", 340 + 85, bCoinDim + 5, 0) # Not much difference between the Score number placement (see 561)
            drawX = drawNums(soloNums, cNumbers, drawX, 362, False) # This draw uses the coin numbers (yellow)
            screen.blit(bigCoin, (drawX + 5, 362 + numberHeight / 2 - bCoinDim / 2)) # The big coin is placed 5 pixels to the left to not looked cramped
        else: # if the skin was already purchased
            screen.blit(selected, (335, 350)) # *n
            
        for i in range(len(totalShopSkins)):
            screen.blit(totalShopSkins[i].image, XY(totalShopSkins[i]))
            
        displayedSkin = pygame.transform.scale(totalShopSkins[selectedSkin].image, (totalShopSkins[selectedSkin].base * 2, 240)) # displays the selected skin 2 times the original image's size
        screen.blit(displayedSkin, ((270 - totalShopSkins[selectedSkin].base * 2) / 2 + 320, 90)) # the x placement is the middle of the screen not taken up by the shelf image
        
    if shop == True or startGame == True: # When in the shop or playing the game
        soundLibrary[6].stop() # So that the intro song only plays in the startscreen
        
        #Bank Creator (This had to be last because it is layered on the very top)
        drawX, soloNums = firstNumPlacement(bank, "right", 0, bCoinDim + 5, 10) # The only displayed number aligned to the right
        drawX = drawNums(soloNums, cNumbers, drawX, 10, False)
        screen.blit(bigCoin, (drawX + 5, 10 + numberHeight / 2 - bCoinDim / 2)) 
        
    pygame.display.flip() # Displays all images onto the screen	
    
    # Key Presses and Clicks
    for event in pygame.event.get():
        if event.type == QUIT: # If the X is pressed on the window
            pygame.quit() # Will not save any progress if this is how they leave the game
         
       # Key Presses 
        if shop == False: # The shop does not use any key presses
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if resetReady == True:
                        reset = True 
                    elif startGame == False and end == False:
                        startGame = True            
                if event.key == K_RIGHT and end == False:
                    rPressed = True
                elif event.key == K_LEFT and end == False:
                    lPressed = True
                
            elif event.type == KEYUP: # When the user is not pressing a key
                if event.key == K_RIGHT:
                    rPressed = False
                elif event.key == K_LEFT:
                    lPressed = False
                    
            for i in range(len(player)): # To make sure both players have the same speed
                if lPressed == True and rPressed == False:
                    player[i].speed = -20
                elif rPressed == True and lPressed == False:
                    player[i].speed = 20
                else:
                    player[i].speed = 0
                
        #Mouse Presses
        if event.type == MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            mousePress = True   
        elif event.type == MOUSEBUTTONUP:
            mousePress = False
            
        if mousePress == True:
            if shop == True:
                for i in range(len(totalShopSkins)):
                    selectedSkin = totalShopSkins[i].checkSkinPressed(selectedSkin) # Makes sure the display is showing the correct skin
                if mouseX > 335 and mouseX < 575 and mouseY > 450 and mouseY < 516 and totalShopSkins[selectedSkin].purchased == False: # If the user clicks the Purchase Button
                    if bank >= totalShopSkins[selectedSkin].price: # if the user has enough coins to purchase the skin
                        soundLibrary[0].play()
                        bank -= totalShopSkins[selectedSkin].price    
                        totalShopSkins[selectedSkin].purchased = True # The skin is now purchased
                    else: # Plays a negative sound if the player cannot afford the skin
                        soundLibrary[8].play() 
                        
                elif mouseX > 335 and mouseX < 575 and mouseY > 532 and mouseY < 600: # If the user ckicks the Exit Shop Button
                    soundLibrary[9].stop() # Doorbell sound will not play in the title screen
                    if totalShopSkins[selectedSkin].purchased == False:
                        selectedSkin = 0 # If the user leaves the store with a skin selected that they do not own, it will give them the default tomato skin
                    shop = False
                    introSongPlay = True
                        
            # Title Screen Buttons
            elif startGame == False and end == False: 
                if mouseX > 130 and mouseX < 290 and mouseY > 330 and mouseY < 406: # If user clicks the Shop Button
                    soundLibrary[9].play()
                    shop = True
                    
                elif mouseX > 300 and mouseX < 460 and mouseY > 330 and mouseY < 406: # If user clicks the Save & Exit Button
                    saveFile = open("Farm Escape Save.txt", "w") # Program writes a new Save file (will delete previous save file)
                    saveFile.write(str(highscore) + "\n") # Converts all ints to strings so they can be written on
                    saveFile.write(str(bank) + "\n")
                    saveFile.write(str(selectedSkin) + "\n")
                    for i in range(len(totalShopSkins) - 1): # Makes sure the tomato purchase boolean is not written on the save file
                        if totalShopSkins[i + 1].purchased == True:
                            saveFile.write("T\n")
                        else: # if False
                            saveFile.write("\n")
                    saveFile.close() # Closes the text file and quits the game
                    pygame.quit()            