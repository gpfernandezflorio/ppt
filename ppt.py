#!/usr/bin/env python
# -*- coding: utf-8 -*-2

# Piedra = 0 ; Papel = 1 ; Tijera = 2

import sys
import pygame
import random
from pygame import *

class Player(object):
  def __init__(self):
    pass
  def decide(self):
    while True:
      event = pygame.event.wait()
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()
        elif event.key == K_z:
          return 0
        elif event.key == K_x:
          return 1
        elif event.key == K_c:
          return 2
  def tie(self):
    pass
  def win(self):
    pass
  def lose(self):
    pass

class QLearningPlayer(Player):
  def __init__(self):
    self.q = {}
    self.hist = ()
    self.last_move = None
    self.mem = 3
    self.gamma = 0.9
    self.alpha = 0.4
    self.wr = 2.0
    self.lr = -2.0
    self.tr = -1.0
    self.initial = -0.5
  def getQ(self, state, action):
    if self.q.get((state, action)) is None:
      return self.initial
    return self.q.get((state, action))
  def decide(self):
    if len(self.hist) < self.mem:
      i = random.choice([0,1,2])
    else:
      qs = map(lambda x : self.getQ(self.hist, x), [0,1,2])
      maxQ = max(qs)
      if qs.count(maxQ) > 1:
        best_options = [i for i in range(3) if qs[i] == maxQ]
        i = random.choice(best_options)
      else:
        i = qs.index(maxQ)
    self.last_move = i
    return i
  def tie(self):
    n = (str(self.last_move)+'T')
    if len(self.hist) < self.mem:
      t = list(self.hist)
      t.append(n)
      self.hist = tuple(t)
    else:
      self.learn(n, self.tr)
  def win(self):
    n = (str(self.last_move)+'W')
    if len(self.hist) < self.mem:
      t = list(self.hist)
      t.append(n)
      self.hist = tuple(t)
    else:
      self.learn(n, self.wr)
  def lose(self):
    n = (str(self.last_move)+'L')
    if len(self.hist) < self.mem:
      t = list(self.hist)
      t.append(n)
      self.hist = tuple(t)
    else:
      self.learn(n, self.lr)
  def learn(self, n, reward):
    result = list(self.hist)[1:]
    result.append(n)
    result = tuple(result)
    prev = self.getQ(self.hist, self.last_move)
    maxqnew = max([self.getQ(result, a) for a in [0,1,2]])
    self.q[(self.hist, self.last_move)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)
    self.hist = result

screen = None
hist1 = None
hist2 = None
rock = None
paper = None
scissors = None
zlabel = None
xlabel = None
clabel = None
game = None
h1 = None
h2 = None
WIN = (0,230,20)
LOSE = (220,0,20)
GRAY = (230,230,230)

def paint():
  screen.fill((20,20,20),rival)
  screen.blit(rock,(w/4-rock.get_rect().w/2,5*h/8))
  screen.blit(paper,(w/2-paper.get_rect().w/2,5*h/8))
  screen.blit(scissors,(3*w/4-scissors.get_rect().w/2,5*h/8))
  screen.blit(zlabel,(w/4-zlabel.get_rect().w/2,5*h/8))
  screen.blit(xlabel,(w/2-xlabel.get_rect().w/2,5*h/8))
  screen.blit(clabel,(3*w/4-clabel.get_rect().w/2,5*h/8))
  for i in range(3):
    screen.fill(game[i][0],hist1[i])
    screen.fill(game[i][1],hist2[i])
    screen.blit(h1[i],hist1[i])
    screen.blit(h2[i],hist2[i])
  pygame.display.update()

if __name__ == "__main__":
  pygame.init()
  pygame.mouse.set_visible(0)
  infoObject = pygame.display.Info()
  w = infoObject.current_w
  h = infoObject.current_h
  rival = Rect(w/2-w/6,h/8,w/3,w/6+w/16)
  h1 = [Surface((0,0)),Surface((0,0)),Surface((0,0))]
  h2 = [Surface((0,0)),Surface((0,0)),Surface((0,0))]
  hist1 = [Rect(24*w/32,h/8,w/14,w/14),Rect(24*w/32,h/8+w/12,w/14,w/14),Rect(24*w/32,h/8+w/6,w/14,w/14)]
  hist2 = [Rect(28*w/32,h/8,w/14,w/14),Rect(28*w/32,h/8+w/12,w/14,w/14),Rect(28*w/32,h/8+w/6,w/14,w/14)]
  screen = pygame.display.set_mode((w,h), FULLSCREEN)
  rock = pygame.image.load("rock.png").convert_alpha()
  rock = pygame.transform.scale(rock, (w/6, w/6))
  minirock = pygame.transform.scale(rock, (w/16, w/16))
  paper = pygame.image.load("paper.png").convert_alpha()
  paper = pygame.transform.scale(paper, (w/6, w/6))
  minipaper = pygame.transform.scale(paper, (w/16, w/16))
  scissors = pygame.image.load("scissors.png").convert_alpha()
  scissors = pygame.transform.scale(scissors, (w/6, w/6))
  miniscissors = pygame.transform.scale(scissors, (w/16, w/16))
  font1 = pygame.font.SysFont("monospace", w/25, True)
  zlabel = font1.render("Z",True,(0,0,0))
  xlabel = font1.render("X",True,(0,0,0))
  clabel = font1.render("C",True,(0,0,0))
  RED = (160,20,20)
  BLUE = (20,20,140)
  GREEN = (20,150,20)
  game = [((0,0,0),(0,0,0)),((0,0,0),(0,0,0)),((0,0,0),(0,0,0))]
  screen.fill(GRAY)
  paint()
  p1 = QLearningPlayer()
  p2 = Player()

  while True:
    win = False
    lose = False
    d1 = p1.decide()
    d2 = p2.decide()
    screen.fill((20,20,20),rival)
    if d1 == 0:
      screen.blit(rock,(w/2-rock.get_rect().w/2,rival.y+w/32))
      h1.insert(0,minirock)
    elif d1 == 1:
      screen.blit(paper,(w/2-paper.get_rect().w/2,rival.y+w/32))
      h1.insert(0,minipaper)
    elif d1 == 2:
      screen.blit(scissors,(w/2-scissors.get_rect().w/2,rival.y+w/32))
      h1.insert(0,miniscissors)
    pygame.display.update(rival)
    if not pygame.event.peek(pygame.USEREVENT):
      pygame.time.wait(200)
    if pygame.key.get_pressed()[K_ESCAPE]:
      pygame.quit()
      sys.exit()
    screen.fill((20,20,20),rival)
    if d1 == d2:
      p1.tie()
      p2.tie()
      game.insert(0,(BLUE,BLUE))
    elif d1 == d2 + 1 or (d1 == 0 and d2 == 2):
      p1.win()
      p2.lose()
      lose = True
      game.insert(0,(GREEN,RED))
    else:
      p1.lose()
      p2.win()
      win = True
      game.insert(0,(RED,GREEN))
    if d2 == 0:
      h2.insert(0,minirock)
    elif d2 == 1:
      h2.insert(0,minipaper)
    elif d2 == 2:
      h2.insert(0,miniscissors)
    if win:
      screen.fill(WIN)
    elif lose:
      screen.fill(LOSE)
    else:
      screen.fill(GRAY)
    paint()
  pygame.quit()
  sys.exit()
