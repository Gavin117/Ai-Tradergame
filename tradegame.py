import pygame
from collections import namedtuple
import csv
import time
import os
import random

def process_data(filename):
    def _scale_prices(value,minn,maxx):
        NewValue = (((value - minn) * (470 - 10)) / (maxx - minn)) + 10
        return NewValue
    with open(filename) as file:
        reader = csv.reader(file)
        header = next(reader)
        data = [row for row in reader]
        file.close()
    #timestamp = [row[0] for row in data]
    close = [float(row[4]) for row in data]
    min_price = min(close)
    max_price = max(close)
    #time_price = list(zip(timestamp,close))
    scaled_close = [_scale_prices(i,min_price,max_price) for i in close]
    return scaled_close


pygame.init()
font = pygame.font.Font('arial.ttf', 14)
font_end = pygame.font.Font('arial.ttf', 40)
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)


line_width = 2
count = 0
Point = namedtuple('Point', 'x, y')
print('Starting Balance = $100')

class TradeGame:
    
    def __init__(self, w=750, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        self.display.fill(BLACK)
        pygame.display.set_caption('Trader')   
        self.interval = 2
        
        self.price = 0
        self.balance = 100
        self.portfolio = 0
        self.pnl = 0
        self.score = 0
        self.chart = chart_data
        self.history = []
        self.trades = []
        self._place_price()
        
        
    def _place_price(self):
        price = self.chart[0]
        y = int(round(480-price))
        x = self.interval
        self.price = Point(x,y)
        self.history.append(self.price)
        self.chart.pop(0)
        #print(self.price)
    
    def _buy_trade(self):
        self.portfolio = self.balance/(480-self.price.y)
        self.pnl = self.balance
        self.balance = 0
        self.trades.append([1,self.price])
        print('BUY',round(self.portfolio,2),'BTC')
        print()
      
    def _sell_trade(self):
        self.balance = self.portfolio*(480-self.price.y) 
        self.portfolio = 0
        self.pnl = 0
        self.trades.append([0,self.price])
        print('Sell $', round(self.balance,2))
        print()
    
    def _update_ui(self):
        self.display.fill(BLACK)
        
        usdt = font.render("USDT: $" + str(round(self.balance,2)), True, WHITE)
        self.display.blit(usdt, [0, 0])
        portfolio = font.render(f"{FILENAME[:3]}: " + str(round(self.portfolio,2)), True, WHITE)
        self.display.blit(portfolio, [0, 20])
        profit_loss = font.render("PNL: $" + str(round(((480-self.price.y)*self.portfolio)-self.pnl,2)), True, WHITE)
        self.display.blit(profit_loss, [0, 40])
        
        
        for trade in self.trades:
            if trade[0] == 1:
                pygame.draw.circle(self.display, GREEN, (trade[1].x,trade[1].y), 10)
            else:
                pygame.draw.circle(self.display, RED, (trade[1].x,trade[1].y), 10)
        
        for hist in self.history:
            pygame.draw.rect(self.display, WHITE, pygame.Rect(hist.x, hist.y, line_width, line_width))

        pygame.draw.rect(self.display, WHITE, pygame.Rect(self.price.x, self.price.y, line_width, line_width))
        pygame.display.flip()
        

    def playstep(self):
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._buy_trade()
                elif event.key == pygame.K_RIGHT:
                    self._sell_trade()
                else:
                    pass

        if len(self.chart) != 1:
            game_over = False
            self._place_price()
            self._update_ui()
            self.interval += 2
        
            return game_over,self.balance
        else:
            game_over = True
            return game_over,self.balance
        
    def end_game(self):
        self.display.fill(BLACK)
        info = "usdt:   $" + str(round(balance,2))
        final_balance = font_end.render(('Final Balance'), True, WHITE)
        self.display.blit(final_balance, [round((self.w/2)-((len(info)/2))*20), self.h/4])
        end_game_screen = font_end.render((info), True, WHITE)
        self.display.blit(end_game_screen, [round((self.w/2)-((len(info)/2))*20), self.h/2])
        pygame.display.flip()
           



     

if(__name__=="__main__"):
    charts = os.listdir('/charts')
    charts = [i for i in charts if i[-3:] == 'csv']
    for i in range(5):
        FILENAME = random.choice(charts)
        
        chart_data = process_data(FILENAME)
        game = TradeGame()
        
        while True:
            game_over,balance = game.playstep()
            time.sleep(0.01)
            if game_over == True:
                game.end_game()
                print('Final Balance: $'+str(round(balance,2)))
                break
        time.sleep(3)
    pygame.quit()
