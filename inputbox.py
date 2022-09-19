# A simple module to get user input allowing for backspace but not arrow keys or delete key
# Location indicated by a rectangle parameter 
# Called by:
# import inputbox
# answer = inputbox.ask(screen, prompt, rect)
# The following optional paremeters can be used to customize:
# txtColor=(0,0,0), fillColor=(255,255,255), borderColor=(0,0,0), borderWidth=3, fontType="calibri", fontSize=18, promptColor=(96,96,96)

import pygame, pygame.font, pygame.event, pygame.draw, string
pygame.init()
from pygame.locals import *

VALID_KEYS = string.printable
capsOn = False

def display_box(screen, prompt, r, currentInput, txtColor, fillColor, borderColor, borderWidth, fontType, fontSize, promptColor):
  # Print a message in a box in the middle of the screen
  pygame.draw.rect(screen, borderColor, r)
  pygame.draw.rect(screen, fillColor,(r[0]+borderWidth,r[1]+borderWidth,r[2]-borderWidth*2,r[3]-borderWidth*2))
  if len(prompt) != 0:
    fontobject = pygame.font.SysFont(fontType,fontSize)
    prompt_surface = fontobject.render(" "+prompt, True, promptColor)
    x = r[0] + borderWidth + 1
    y = r[1] + (r[3] - prompt_surface.get_height()) // 2
    screen.blit(prompt_surface,(x,y))
  if len(currentInput) != 0:
    fontobject = pygame.font.SysFont(fontType,fontSize)
    input_surface = fontobject.render(" " + "".join(currentInput), True, txtColor)
    x += prompt_surface.get_width() + 1
    y = r[1] + (r[3] - prompt_surface.get_height()) // 2
    if x + input_surface.get_width() > r[0] + r[2] - (borderWidth + 3):
      xOffSet = (x + input_surface.get_width()) - (r[0] + r[2] - (borderWidth + 3)) 
      input_surface = input_surface.subsurface((xOffSet,0,input_surface.get_width()-xOffSet,input_surface.get_height()))
    screen.blit(input_surface,(x,y))
  pygame.display.flip()

def ask(screen, prompt, rect, txtColor=(0,0,0), fillColor=(255,255,255), borderColor=(0,0,0), borderWidth=3, fontType="calibri", fontSize=18, promptColor=(96,96,96)):
  global VALID_KEYS
  current_string = ''
  display_box(screen, prompt, rect, current_string, txtColor, fillColor, borderColor, borderWidth, fontType, fontSize, promptColor)
  enteringText = True
  while enteringText:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        keyPressed = event.unicode
        if keyPressed in VALID_KEYS:
          current_string += keyPressed
        if event.key == K_BACKSPACE:
          current_string = current_string[:-1]
        if event.key == K_RETURN:
          enteringText = False
    display_box(screen, prompt, rect, current_string, txtColor, fillColor, borderColor, borderWidth, fontType, fontSize, promptColor) 
  return current_string.strip()

def main():
  screen = pygame.display.set_mode((320,240))
  screen.fill((0,255,255))
  userName = ask(screen, "Name:", (20,20,250,40))
  print(userName)

if __name__ == '__main__': main()
