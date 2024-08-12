#!/usr/bin/env python
# coding: utf-8

# In[2]:


# This script implements a store management system using Pygame. It includes classes for various goods,
# a store and basket management system, and interactive Pygame graphics to handle item display, selection, 
# and basket management. The user can add or remove items from the basket and see the total price and weight.

from abc import ABCMeta, abstractstaticmethod
from datetime import datetime
import pygame
from time import sleep

class Goods:
    def __init__(self, _id, brand, weight, price, size):
        self.id = _id
        self.brand = brand
        self.weight = weight
        self.price = price
        self.size = size

class Copybook(Goods):
    def __init__(self, _id, brand, weight, price, size, cover, ruling):
        super().__init__(_id, brand, weight, price, size)
        self.cover = cover
        self.ruling = ruling
    
class Calculator(Goods):
    def __init__(self, _id, brand, weight, price, size, body_material, feeding):
        super().__init__(_id, brand, weight, price, size)
        self.body_material = body_material
        self.feeding = feeding
        
class Marker(Goods):
    def __init__(self, _id, brand, weight, price, size, quantity_in_package, water_based):
        super().__init__(_id, brand, weight, price, size)
        self.quantity_in_package = quantity_in_package
        self.water_based = water_based
        
class Folder(Goods):
    def __init__(self, _id, brand, weight, price, size, color, transparency):
        super().__init__(_id, brand, weight, price, size)
        self.color = color
        self.transparency = transparency
        
class Sketchbook(Goods):
    def __init__(self, _id, brand, weight, price, size, fastening, number_of_sheets):
        super().__init__(_id, brand, weight, price, size)
        self.fastening = fastening
        self.number_of_sheets = number_of_sheets

class Compass(Goods):
    def __init__(self, _id, brand, weight, price, size, appointment, material):
        super().__init__(_id, brand, weight, price, size)
        self.appointment = appointment
        self.material = material

        
        
class Store:
    __instance = None
    def __init__(self):
        if self.__instance != None:
            raise Exception('You cannot create more than one object')
        Store.__instance = self
        self.amount_and_discounts = {}
    def add_item(self, item, amount, discount):
        item.amount = amount
        item.discount = discount
        if item.id not in self.amount_and_discounts:
            self.amount_and_discounts[item.id] = {'amount': amount, 'discount': discount}
        else:
            self.amount_and_discounts[item.id]['amount'] += amount
            self.amount_and_discounts[item.id]['discount'] = discount
    def remove_item(self, item, amount):
        self.amount_and_discounts[item.id]['amount'] -= amount
    def get_item_amount(self, item):
        return self.amount_and_discounts[item.id]['amount']
    def get_item_discount(self, item):
        return self.amount_and_discounts[item.id]['discount']
    
class Basket:
    def __init__(self):
        self.basket = []
    def add_item(self, item, amount):
        if not any(item == i[0] for i in self.basket):
            self.basket.append([item, amount])
        else:
            for i in self.basket:
                if i[0] == item:
                    i[1] += amount
    def remove_item(self, item, amount):
        for i in range(len(self.basket)):
            if self.basket[i][0] == item and self.basket[i][1] >= amount:
                self.basket[i][1] -= amount
                if self.basket[i][1] == 0:
                    del self.basket[i]
                break
    def sort_by_field(self, field):
        if field == 'item':
            self.basket.sort(key=lambda x: x[0])
        elif field == 'amount':
            self.basket.sort(key=lambda x: x[1])
    def display_items(self, _item):
        for item in self.basket:
            print(f"{_item}: {item[1]} units - {item[0].price * item[1]} UAH")
    def total_price(self):
        total = 0
        for item in self.basket:
            total += item[0].price * item[1] - (item[0].price * item[0].discount * item[1] / 100)
        return total
    def total_weight(self):
        total = 0
        for item in self.basket:
            total += item[0].weight * item[1]
        return total

    
    
    
class StoreManager:
    def __init__(self, item, amount, my_store):
        self.item = item
        self.amount = amount
        self.my_store = my_store
    def __enter__(self):
        if self.my_store.amount_and_discounts[self.item.id]['amount'] >= self.amount:
            return True
        return False
    def __exit__(self, exc_type, exc_value, traceback):
        pass 
    
class BasketManager:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount
    def __enter__(self):
        for i in range(len(Basket().basket)):
            if Basket().basket[i][0] == self.item and Basket().basket[i][1] >= self.amount:
                return True
        return False
    def __exit__(self, exc_type, exc_value, traceback):
        pass 
    
    
    
    
class Sell:
    def discount(self, item, original_price, discount):
        return original_price*(discount/100)
    def time_log(self):
        self.time_log = datetime.now()
    def to_basket(self, item, amount, my_store, my_basket):
        with StoreManager(item, amount, my_store) as store:
            if store:
                my_store.remove_item(item, amount)
                my_basket.add_item(item, amount)
            else:
                print('There are not enough products in the store')
    def from_basket(self, item, amount, my_store, my_basket):
        with BasketManager(item, amount) as basket:
            if basket:
                my_basket.remove_item(item, amount)
                my_store.add_item(item, amount)
            else:
                print('There are not enough products in the basket')
    def check(self, field):
        Basket().sort_by_field(field)
        Basket().display_items()
        print('\nTotal price:', Basket().total_price())
        print('Total weight:', Basket().total_weight())
    def buy(self, my_basket):
        my_basket.basket = []
        print('Will you take the bag?')
                
                
                
                
class SellCopybook(Copybook, Sell):
    pass
    
class SellCalculator(Calculator, Sell):
    pass
        
class SellMarker(Marker, Sell):
    pass
        
class SellFolder(Folder, Sell):
    pass
        
class SellSketchbook(Sketchbook, Sell):
    pass

class SellCompass(Compass, Sell):
    pass

        

my_store = Store()
my_basket = Basket()
copybook1 = Copybook(1, 'kite', 50, 70, (20, 10, 2), 'soft', 'cell')
copybook2 = Copybook(2, 'kite', 100, 120, (40, 30, 6), 'hard', 'line')
calculator1 = Calculator(3, 'easy solve', 50, 250, (20, 15, 5), 'metal', 'solar battery')
marker1 = Marker(4, 'color life', 20, 80, (18, 1, 1), 7, True)
marker2 = Marker(5, 'just life', 120, 230, (18, 1, 1), 24, True)
folder1 = Folder(6, 'foLd', 10, 15, (25, 18, 0.5), 'red', True)
folder2 = Folder(7, 'foLd', 10, 15, (25, 18, 0.5), 'blue', True)
folder3 = Folder(8, 'foLd', 10, 15, (25, 18, 0.5), 'green', True)
sketchbook1 = Sketchbook(9, 'kite', 40, 60, (20, 10, 2), 'rings', 250)
compass1 = Compass(11, 'nature', 200, 1500, (10, 10, 3), 'tourist', 'metal')
my_store.add_item(copybook1, 50, 50)
my_store.add_item(copybook2, 30, 30)
my_store.add_item(calculator1, 20, 12)
my_store.add_item(marker1, 30, 3)
my_store.add_item(marker2, 20, 3)
my_store.add_item(folder1, 40, 60)
my_store.add_item(folder2, 40, 60)
my_store.add_item(folder3, 40, 60)
my_store.add_item(sketchbook1, 10, 20)
my_store.add_item(compass1, 5, 30)
sell_compass = SellCompass(11, 'nature', 200, 1500, (10, 10, 3), 'tourist', 'metal')
sell_sketchbook = SellSketchbook(9, 'kite', 40, 60, (20, 10, 2), 'rings', 250)
sell_folder = SellFolder(6, 'foLd', 10, 15, (25, 18, 0.5), 'red', True)
sell_folder2 = SellFolder(7, 'foLd', 10, 15, (25, 18, 0.5), 'blue', True)
sell_folder3 = SellFolder(8, 'foLd', 10, 15, (25, 18, 0.5), 'green', True)
sell_marker = SellMarker(4, 'color life', 20, 80, (18, 1, 1), 7, True)
sell_marker2 = SellMarker(5, 'just life', 120, 230, (18, 1, 1), 24, True)
sell_copybook = SellCopybook(1, 'kite', 50, 70, (20, 10, 2), 'soft', 'cell')
sell_copybook2 = SellCopybook(2, 'kite', 100, 120, (40, 30, 6), 'hard', 'line')
sell_calculator = SellCalculator(3, 'easy solve', 50, 250, (20, 15, 5), 'metal', 'solar battery')



def draw_(var, size, x, y):
    font = pygame.font.SysFont('Arial', size-3)
    img = font.render(str(var), True, (0, 0, 0))
    screen.blit(img, (x, y))
    
def remove_(var, size, x, y):
    font = pygame.font.SysFont('Arial', size-3)
    img = font.render(str(var), True, (255, 255, 255))
    screen.blit(img, (x, y))

def for_var(rect_n, rect_nn, var_n):
    if rect_n.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] == 1:
            var_n += 1
            sleep(0.3)
    if rect_nn.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] == 1:
            if var_n == 0:
                pass
            else:
                var_n -= 1
            sleep(0.3)
    return var_n
    
def for_buy(rect_n, sell_obj, name, amount):
    if rect_n.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] == 1:
            sell_obj.to_basket(name, amount, my_store, my_basket)
            sleep(0.3)
            
def draw_var(var, size, x, y):
    font = pygame.font.SysFont('Arial', size-3)
    rect_n = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, (255, 255, 255), rect_n)
    img = font.render(str(var), True, (0, 0, 0))
    screen.blit(img, (x, y))


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fon = pygame.image.load('shop.jpg')
screen.blit(fon, (0, 0))
copybook = pygame.image.load('copybook.png')
copybook = pygame.transform.scale(copybook, (150, 150))
screen.blit(copybook, (150, 200))
calculator = pygame.image.load('calculator.png')
calculator = pygame.transform.scale(calculator, (140, 170))
screen.blit(calculator, (350, 180))
markers = pygame.image.load('markers.png')
markers = pygame.transform.scale(markers, (180, 180))
screen.blit(markers, (550, 180))
folder = pygame.image.load('folder.png')
folder = pygame.transform.scale(folder, (100, 170))
screen.blit(folder, (150, 390))
sketchbook = pygame.image.load('sketchbook.png')
sketchbook = pygame.transform.scale(sketchbook, (150, 150))
screen.blit(sketchbook, (350, 410))
compass = pygame.image.load('compass.png')
compass = pygame.transform.scale(compass, (150, 150))
screen.blit(compass, (550, 410))
buy_button = pygame.image.load('buy_button.png')
buy_button = pygame.transform.scale(buy_button, (150, 150))
rect_buy_button_1 = buy_button.get_rect()
rect_buy_button_2 = buy_button.get_rect()
rect_buy_button_3 = buy_button.get_rect()
rect_buy_button_4 = buy_button.get_rect()
rect_buy_button_5 = buy_button.get_rect()
rect_buy_button_6 = buy_button.get_rect()
rect_buy_button_3.topleft = (550, 470)
rect_buy_button_2.topleft = (350, 470)
rect_buy_button_1.topleft = (130, 470)
rect_buy_button_6.topleft = (568, 260)
rect_buy_button_5.topleft = (350, 260)
rect_buy_button_4.topleft = (130, 260)
screen.blit(buy_button, (550, 470))
screen.blit(buy_button, (350, 470))
screen.blit(buy_button, (130, 470))
screen.blit(buy_button, (568, 260))
screen.blit(buy_button, (350, 260))
screen.blit(buy_button, (130, 260))
buy_now_button = pygame.image.load('buy_now_button.png')
buy_now_button = pygame.transform.scale(buy_now_button, (150, 150))
rect_buy_now_button_1 = buy_now_button.get_rect()
rect_buy_now_button_1.topleft = (650, 50)
screen.blit(buy_now_button, (650, 50))
var = 1
draw_var(var, 33, 690, 530)
draw_var(var, 33, 490, 530)
draw_var(var, 33, 270, 530)
draw_var(var, 33, 270, 320)
draw_var(var, 33, 490, 320)
draw_var(var, 33, 709, 320)
arow1 = pygame.image.load('arow1.png')
arow1 = pygame.transform.scale(arow1, (33, 10))
rect1 = arow1.get_rect()
rect1.topleft = (690, 520)
arow2 = pygame.image.load('arow1.png')
arow2 = pygame.transform.scale(arow2, (33, 10))
rect2 = arow2.get_rect()
rect2.topleft = (490, 520)
arow3 = pygame.image.load('arow1.png')
arow3 = pygame.transform.scale(arow3, (33, 10))
rect3 = arow3.get_rect()
rect3.topleft = (270, 520)
arow4 = pygame.image.load('arow1.png')
arow4 = pygame.transform.scale(arow4, (33, 10))
rect4 = arow4.get_rect()
rect4.topleft = (270, 310)
arow5 = pygame.image.load('arow1.png')
arow5 = pygame.transform.scale(arow5, (33, 10))
rect5 = arow5.get_rect()
rect5.topleft = (490, 310)
arow6 = pygame.image.load('arow1.png')
arow6 = pygame.transform.scale(arow6, (33, 10))
rect6 = arow6.get_rect()
rect6.topleft = (709, 310)
arow11 = pygame.image.load('arow2.png')
arow11 = pygame.transform.scale(arow11, (33, 10))
rect11 = arow11.get_rect()
rect11.topleft = (690, 560)
arow22 = pygame.image.load('arow2.png')
arow22 = pygame.transform.scale(arow22, (33, 10))
rect22 = arow22.get_rect()
rect22.topleft = (490, 560)
arow33 = pygame.image.load('arow2.png')
arow33 = pygame.transform.scale(arow33, (33, 10))
rect33 = arow33.get_rect()
rect33.topleft = (270, 560)
arow44 = pygame.image.load('arow2.png')
arow44 = pygame.transform.scale(arow44, (33, 10))
rect44 = arow44.get_rect()
rect44.topleft = (270, 350)
arow55 = pygame.image.load('arow2.png')
arow55 = pygame.transform.scale(arow55, (33, 10))
rect55 = arow55.get_rect()
rect55.topleft = (490, 350)
arow66 = pygame.image.load('arow2.png')
arow66 = pygame.transform.scale(arow66, (33, 10))
rect66 = arow66.get_rect()
rect66.topleft = (709, 350)
screen.blit(arow1, (270, 520))
screen.blit(arow2, (490, 520))
screen.blit(arow3, (690, 520))
screen.blit(arow4, (270, 310))
screen.blit(arow5, (490, 310))
screen.blit(arow6, (709, 310))
screen.blit(arow11, (270, 560))
screen.blit(arow22, (490, 560))
screen.blit(arow33, (690, 560))
screen.blit(arow44, (270, 350))
screen.blit(arow55, (490, 350))
screen.blit(arow66, (709, 350))
rect_basket = pygame.Rect(677, 43, 100, 50)
pygame.draw.rect(screen, (255, 255, 255), rect_basket)
draw_(0, 33, 700, 50)
run = True
var1 = var2 = var3 = var4 = var5 = var6 = 1
FPS = 60
clock = pygame.time.Clock()         
while run:
    previous_price = my_basket.total_price()
    draw_var(var1, 33, 690, 530)
    draw_var(var2, 33, 490, 530)
    draw_var(var3, 33, 270, 530)
    draw_var(var4, 33, 270, 320)
    draw_var(var5, 33, 490, 320)
    draw_var(var6, 33, 709, 320)
    var1 = for_var(rect1, rect11, var1)
    var2 = for_var(rect2, rect22, var2)
    var3 = for_var(rect3, rect33, var3)
    var4 = for_var(rect4, rect44, var4)
    var5 = for_var(rect5, rect55, var5)
    var6 = for_var(rect6, rect66, var6)
    for_buy(rect_buy_button_5, sell_calculator, calculator1, var5)
    for_buy(rect_buy_button_6, sell_marker, marker1, var6)
    for_buy(rect_buy_button_3, sell_compass, compass1, var1)
    for_buy(rect_buy_button_4, sell_copybook, copybook1, var4)
    for_buy(rect_buy_button_1, sell_folder, folder1, var3)
    for_buy(rect_buy_button_2, sell_sketchbook, sketchbook1, var2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    local_price = my_basket.total_price()
    if previous_price != local_price:
        remove_(previous_price, 33, 700, 50)
        draw_(local_price, 33, 700, 50)
    if rect_buy_now_button_1.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] == 1:
            run = False
            print(f'{my_basket.total_price()} UAH\nWill you take the bag?')
    clock.tick(FPS)
    #pygame.display.update(rect_update)
    pygame.display.update()

            
pygame.quit()

