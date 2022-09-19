########################################################################################################
## File Name: CelebGame.py                                                                            ##
## Author: Nahal H.                                                                                   ##
## Modules Used: pygame, random and inputbox                                                          ##
## Description: this game displays mixed tiles of an image from a chosen category which then starts   ##
## to reorder itself while clues are displayed and faded out. The difficulty of the game is chosen and##
## manipulated by the number of tiles that are displaying the image. The user has a chance to enter   ##
## the name of the celebrity in an inputbox which evaluates whether it's right or not and give a score##
## based on how fast they were to enter their guess. They are allowed to direct back to categories    ##
## screen and choose a new image to guess as well. If they don't make a guess before image is         ##
## reordered they will lose as well.                                                                  ##
## Input: user inputs mouse position by clicking in order to make the buttons function accordingly    ##
## and they also use it to choose a category as direct themselves to the input box which will pop     ##
## up in order to let them type in their answer and check if they guessed correctly or not.           ##
########################################################################################################

#----------------#
#    IMPORTS     #
#----------------#
import pygame
pygame.init()
from pygame import *
import random
import inputbox

#----------------#
#   CONSTANTS    #
#----------------#
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
GREY = (230,230,230)
BLACK = (0,0,0)
LIGHT_RED = (255,40,0)

ASPECT_RATIO = .75
IMG_HEIGHT = 520
IMG_WIDTH = int(IMG_HEIGHT * ASPECT_RATIO)
blitX = (640 - IMG_HEIGHT * ASPECT_RATIO) // 2
blitY = 30
BORDER_WIDTH = 3
EASY_TILE_ROWS_COLS = 5
MEDIUM_TILE_ROWS_COLS = 10          # possible values 5,10,13,26,65,130
HARD_TILE_ROWS_COLS = 26
UPDATE_IMAGE_FRAME_RATE = 5
START_SCREEN = 0
MAIN_SCREEN = 1
CATEGORIES_SCREEN = 2
DIFFICULTY_SCREEN = 3
GUESS_SCREEN = 4
#----------------#
#   FUNCTIONS    #
#----------------#
# FUNCTION TO DRAW RECTANGULAR BUTTONS #
def DrawRectButtons(screen,text,r,bColor=(0,255,0),fColor=(0, 0, 0),font=pygame.font.SysFont("arial", 30)):
    pygame.draw.rect(screen,bColor,r)
    pygame.draw.rect(screen,fColor, r, 3)
    txtSurface = font.render(text,True,fColor)
    screen.blit(txtSurface, (r[0]+(r[2]-txtSurface.get_width())//2,r[1]+(r[3]-txtSurface.get_height())//2))

# FUNCTION TO DRAW RECTANGULAR BUTTONS IN A ROW #
def drawRectBtns(rList, txtList):
    for i,r in enumerate (rList):
        DrawRectButtons(screen,txtList[i],r)

# FUCTION TO GET RECTANGULAR BUTTONS INDEX #
def getRectButtonIndex(rList, mp): 
    for i,r in enumerate(rList):
        if pygame.Rect(r).collidepoint(mp):
            return i
    return -1

# FUNCTION TO RESIZE IMAGE #
def resizeImage(img,Aratio,endH,endW):
        imgh = pygame.Surface.get_height(img)
        imgw = pygame.Surface.get_width(img)
        AR = imgw / imgh 
        if AR > Aratio:
            newH = endH 
            newW = imgw * endH // imgh
            round(newW, 0)
            resizeImg = pygame.transform.scale(img,(newW, newH))
            x = (newW - endW) // 2
            newImg = resizeImg.subsurface(x,0,endW,endH)
        elif AR <= Aratio:
            newW = endW
            newH = imgh * endW // imgw
            resizeImg = pygame.transform.scale(img,(newW, newH))
            newImg = resizeImg.subsurface(0,0,endW,endH)
        return newImg
# FUNCTION TO CUT THE IMAGE INTO TILES #
def createImgTiles(img,rowCols):
    tileLst = []
    imgh = pygame.Surface.get_height(img)
    imgw = pygame.Surface.get_width(img)
    y_length = imgh // rowCols
    x_length = imgw // rowCols
    for y in range(0,imgh,y_length):
        for x in range(0,imgw,x_length):
            tileLst.append(img.subsurface((x,y,x_length,y_length)))
    return tileLst

# FUNCTION TO GET EACH TILES COORDINATES #                        
def tileCoordinates(img,rowCols,startx,starty):
    x,y = (startx, starty)
    imgh = pygame.Surface.get_height(img)
    imgw = pygame.Surface.get_width(img)
    y_length = imgh // rowCols
    x_length = imgw // rowCols
    tileCoordinates = []
    for cols in range(rowCols):
        for rows in range(rowCols):
                tileCoordinates.append((x,y))
                x += x_length
        x = startx
        y += y_length
    return tileCoordinates

# FUNCTION TO DRAW TILES #
def drawTiles(screen,tileCoordinates,startx,starty,tileLst,tileIndices):
    x,y = (startx,starty)
    for i,xy in enumerate(tileCoordinates):
            screen.blit(tileLst[tileIndices[i]],(xy))
# FUNCTION TO READ IN FILE #
def readInfile():
        try:
                fi = open('celebs.txt')
        except:
                print('could not open file')
        puzzles = [[],[],[]]
        categories = ['Actor', 'Sports', 'Famous Canadians']
        while True:
            answer = fi.readline().strip()
            if answer == '':
                    break
            category = fi.readline().strip()
            possible_ans = fi.readline().strip().split('+')
            imgFile = fi.readline().strip()
            clues= fi.readline().strip().split('+')
            newPuzzle = [answer,possible_ans, imgFile, clues]
            puzzles[categories.index(category)].append(newPuzzle)
        return puzzles

# FUNCTION TO ANIMATE IMAGE#
def animateImage(img):
    x = 305
    y = 270
    w = 30
    h = 40
    f = 13
    hf = int(pygame.Surface.get_height(img)) / f
    wf = int(pygame.Surface.get_width(img))  / f
    while w <= 390 and h <= 520:
        resizeImg = pygame.transform.scale(img,(w,h)) #resize gradually
        screen.blit(resizeImg,(x,y))
        w += int(wf)
        h += int(hf)
        x -= wf/2
        y -= hf/2

# FUNCTION TO FADE OUT THE CLUES #
def fadeOutClues(txtSurface,alph,incAmt):
        txtSurface.set_alpha(alph)   
    
    
# THE REDRAW FUNCTION #
def redraw_game_window():
    global yOffset
    global yBlit
    global guessMode
    global gameDone
    global lostGame
    global winGame
    global clockOn
    global guessValue
    global currentScreen
    global alph
    global incAmt
    if currentScreen == GUESS_SCREEN: #if you have pressed the guess button
        screen.fill(GREY)
        answer = inputbox.ask(screen, "Your Answer: ", (170,305,300,90))
        clockOn = False
        if answer.lower() == Ans.lower() or answer.lower() in possibleAns:
            winGame = True #you will win game
            animate = True
            pygame.mixer.music.load('winner.mp3')
            pygame.mixer.music.play()
        else:
            lostGame = True #you will lose game
            animate = True
            pygame.mixer.music.load('loser.mp3')
            pygame.mixer.music.play()
        currentScreen = MAIN_SCREEN #screen changes back to main screen as soon as conditionals are over
    elif currentScreen == MAIN_SCREEN:
        screen.fill(GREY)
        drawRectBtns(settingBtns,settingBtnstxt)
        if gameDone == False: #if game is still going on
            drawTiles(screen,tileCoords,blitX,blitY,tileLst,tileIndices)
            drawRectBtns(guessBtn,guessBtntxt)
            if cInd > -1 and cInd <= 2:  #clues variables to be blited on screen
                txtSurface = pygame.font.SysFont("arial", 20).render('<'+clues[cInd]+'>',True,(0,0,0),(230,230,230))
                fadeOutClues(txtSurface,alph,incAmt)
                screen.blit(txtSurface,((640-txtSurface.get_width())//2,550))
        else:    
            screen.blit(cImage, (blitX, yBlit+yOffset)) #image animated and move down the screen
            if yOffset < 550:
                yOffset += 10    
            if lostGame: #messages displayed if you lose game
                loseSurface = pygame.font.SysFont("arial", 30).render('The Answer is'+'<'+Ans+'>',True,(0,0,0))
                screen.blit(loseSurface,((640-loseSurface.get_width())//2,550))
                commentSurface = pygame.font.SysFont("arial", 30).render('Better luck next time!',True,(255,0,0))
                screen.blit(commentSurface,((640-commentSurface.get_width())//2,600))
            elif OutofTime:  #messages displayed if you run out of time 
                timeOSurface = pygame.font.SysFont("arial", 30).render('The Answer is'+'<'+Ans+'>',True,(0,0,0))
                screen.blit(timeOSurface,((640-timeOSurface.get_width())//2,550))
                commentTOSurface = pygame.font.SysFont("arial", 30).render('Be faster next time!',True,(255,0,0))
                screen.blit(commentTOSurface,((640-commentTOSurface.get_width())//2,600))
            elif winGame:  #messages displayed if you win game
                winSurface = pygame.font.SysFont("arial", 30).render('Congrats!You guessed it right!',True,(0,0,0))
                screen.blit(winSurface,((640-winSurface.get_width())//2,550))
                scoreSurface = pygame.font.SysFont("arial", 30).render('Your Score is '+str(score)+'/1000! Can you be any faster?',True,(255,0,0))
                screen.blit(scoreSurface,((640-scoreSurface.get_width())//2,600))
    elif currentScreen == CATEGORIES_SCREEN: 
        screen.fill(LIGHT_RED)
        drawRectBtns(categoriesBtn,categories)
        drawRectBtns(quitBtn,quitBtntxt)
        screen.blit(curtainImg,(0,0))
    elif currentScreen == DIFFICULTY_SCREEN:
        screen.fill(LIGHT_RED)
        screen.blit(curtainImg,(0,0))
        drawRectBtns(categoriesBtn,difficultiesBtntxt)
        drawRectBtns(quitBtn,quitBtntxt)
    elif currentScreen == START_SCREEN:
        screen.fill(LIGHT_RED)
        screen.blit(curtainImg,(0,0))
        titleSurface = pygame.font.SysFont("rockwell", 100).render('GUESS',True,(177,156,217))
        screen.blit(titleSurface,(120,50))
        titleSurface1 = pygame.font.SysFont("sans serif", 50).render('The',True,(64,224,208))
        screen.blit(titleSurface1,(450,115))
        titleSurface2 = pygame.font.SysFont("impact", 140).render('CELEBRITY',True,(255,255,0))
        screen.blit(titleSurface2,((640-titleSurface2.get_width())//2,135))
        drawRectBtns(startBtn,startBtntxt)
    pygame.display.update()

#-----------------------------------------#
#   VARIABLE AND OBJECT INITIALIZATION    #
#-----------------------------------------#
# create window
screen = pygame.display.set_mode((640,700))
pygame.display.set_caption('CELBRITY GUESSING GAME BY NAHAL H.')
# load image  WILL BE A FUNCTION EVENTUALLY
curtainImg = pygame.image.load('curtainImage.png')
#----------------------------#
#  the MAINLINE begins here  #
#----------------------------#
# VARIABLES SET TO INITIAL VALUES BEFORE LOOP BEGINS #
inPlay = True
gameDone = False
lostGame = False
winGame = False
clockOn = True
animate = False
OutofTime = False
guessMode = False
currentScreen = START_SCREEN
#button lists 
startBtn = [(195,350,250,100)]
startBtntxt = ['Start']
categoriesBtn = [(195,130,250,100),(195,270,250,100),(195,410,250,100)]
categories = ['Actor', 'Sports', 'Famous Canadians']
difficultiesBtntxt = [ 'EASY', 'MEDIUM', 'HARD']
quitBtn = [(195,550,250,50)]
quitBtntxt = ['<QUIT>']
settingBtns = [(530,50,100,50),(530,120,100,50)]
settingBtnstxt = [ 'Menu', 'Quit']
guessBtn = [(270,600,100,50)]
guessBtntxt = ['GUESS']
#variables to display clues/and reshuffle images etc.
reOrderCount = 0
frameRate = 40
clueRate = 270
frameSpeed = 0
cInd = -1
score = 1000
puzzles = readInfile() #text file is processed and read through
yOffset = 0
yBlit = -520
alph = 255 
incAmt = 0.1
# THE GAME LOOP STARTS HERE# 
while inPlay:
    redraw_game_window()
    pygame.time.delay(10)               
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:   
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('make a guess')
        if event.type == pygame.MOUSEBUTTONDOWN:   #if user clicks anywhere on screen
            clickPos = pygame.mouse.get_pos()
            if currentScreen == START_SCREEN:      #you're in the start screen
                startBtnIndex = getRectButtonIndex(startBtn, clickPos)
                if  startBtnIndex != -1:
                    currentScreen = CATEGORIES_SCREEN
            elif currentScreen == CATEGORIES_SCREEN: # you're in categories screen
                    categoriesBtnIndex = getRectButtonIndex(categoriesBtn, clickPos)
                    quitBtnIndex = getRectButtonIndex(quitBtn, clickPos)
                    if categoriesBtnIndex != -1:
                        c = categoriesBtnIndex
                        rndPuzzleIndex = random.randrange(0,len(puzzles[c])) #random indice for picking a puzzle for the category
                        puzzle = puzzles[c][rndPuzzleIndex] #variable to store the picture
                        Ans = puzzle[0]
                        possibleAns = puzzle[1]
                        imgFile = pygame.image.load('images\\'+ puzzle[2]) #load the image
                        clues = puzzle[3]
                        currentScreen = DIFFICULTY_SCREEN 
                    elif quitBtnIndex != -1:
                        inPlay = False
            elif currentScreen == DIFFICULTY_SCREEN:      # you're in difficulties screen
                diffBtnIndex = getRectButtonIndex(categoriesBtn, clickPos)
                quitBtnIndex = getRectButtonIndex(quitBtn, clickPos)
                if diffBtnIndex != -1:
                    cImage = resizeImage(imgFile,ASPECT_RATIO,IMG_HEIGHT,IMG_WIDTH) #image is resized
                    if diffBtnIndex == 0:  #easy mode(25 tiles)
                        tileLst = createImgTiles(cImage,EASY_TILE_ROWS_COLS)
                        tileCoords = tileCoordinates(cImage,EASY_TILE_ROWS_COLS,blitX,blitY)
                        tileIndices = list(range(EASY_TILE_ROWS_COLS**2))
                        random.shuffle(tileIndices)
                        reorderLst = list(range(EASY_TILE_ROWS_COLS**2))
                        random.shuffle(reorderLst)
                    elif diffBtnIndex == 1:  #medium mode(100 tiles)
                        tileLst = createImgTiles(cImage,MEDIUM_TILE_ROWS_COLS)
                        tileCoords = tileCoordinates(cImage,MEDIUM_TILE_ROWS_COLS,blitX,blitY)
                        tileIndices = list(range(MEDIUM_TILE_ROWS_COLS**2))
                        random.shuffle(tileIndices)
                        reorderLst = list(range(MEDIUM_TILE_ROWS_COLS**2))
                        random.shuffle(reorderLst)
                    elif diffBtnIndex == 2: #hard mode(676 tiles)
                        tileLst = createImgTiles(cImage,HARD_TILE_ROWS_COLS)
                        tileCoords = tileCoordinates(cImage,HARD_TILE_ROWS_COLS,blitX,blitY)
                        tileIndices = list(range(HARD_TILE_ROWS_COLS**2))
                        random.shuffle(tileIndices)
                        reorderLst = list(range(HARD_TILE_ROWS_COLS**2))
                        random.shuffle(reorderLst)
                    reOrderRange = len(tileIndices) - 1 #to calculate time of player
                    currentScreen = MAIN_SCREEN
                elif quitBtnIndex != -1:
                    inPlay = False  
            elif currentScreen == MAIN_SCREEN:
                settingBtnsIndex = getRectButtonIndex(settingBtns, clickPos)
                guessBtnIndex = getRectButtonIndex(guessBtn,clickPos)
                if guessBtnIndex != -1:
                    currentScreen = GUESS_SCREEN
                    guessMode = True
                    gameDone = True
                    clockOn = False
                elif settingBtnsIndex != -1:
                    if settingBtnsIndex == 0: #values are reset for another round
                        gameDone = False
                        lostGame = False
                        winGame = False
                        guessMode = False
                        OutofTime = False
                        clockOn = True
                        cInd = -1
                        reOrderCount = 0
                        frameSpeed = 0
                        currentScreen = CATEGORIES_SCREEN
                        rndPuzzleIndex = random.randrange(0,len(puzzles[c])) #random indice for picking a puzzle for the category
                        puzzle = puzzles[c][rndPuzzleIndex] #variable to store the picture
                        yOffset = 0
                        yBlit = -520
                        alph = 255 
                        incAmt = 0.1
                        clueRate = 270
                    else:
                        inPlay = False
    if currentScreen == MAIN_SCREEN:   # you're in main screen
        if clockOn:  #clock is working and images are being rearranged
            frameSpeed += 1
            if alph >= 0:
                alph -= incAmt
            if reOrderCount <= reOrderRange:  #until all tiles are reordered
                if frameSpeed % frameRate == 0:
                    tileIndices[reorderLst[reOrderCount]] = reorderLst[reOrderCount]
                    reOrderCount += 1
                    score -= 10
            else: #you ran out of time 
                reOrderCount = 0
                pygame.mixer.music.load('loser.mp3')
                pygame.mixer.music.play()
                gameDone = True
                OutofTime = True #allows redraw screen to display message
                animate = True   
                clockOn = False
            if frameSpeed % clueRate == 0 and cInd <= 2:
                print('test2')
                cInd += 1
                score -= 100
                clueRate += 270  #the time between each clue displayed becomes larger
                
                        
                    

            






        
                   
                
                
pygame.quit()                
                
        
                
                
        
        
# The following optional paremeters can be used to customize:
# txtColor=(0,0,0), fillColor=(255,255,255), borderColor=(0,0,0), borderWidth=3, fontType="calibri", fontSize=18, promptColor=(96,96,96)
                              
                          
