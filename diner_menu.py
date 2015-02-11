'''
Created on Feb 11, 2015

@author: adudko
'''
from sys import version_info

class DishType():
    ENTREE = 1
    SIDE = 2
    DRINK = 3
    DESSERT = 4
    
    

class Dish():
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __eq__(self, other):
        #should be replaced with a smarter dictionary comparer, but for purposes of this exercise, keeping it simple)
        return (self.type == other.type and self.name == other.name)
    
    def __str__(self):
        return self.name


class Menu():
    ERROR_DISH = Dish(99, "error")
    def __init__(self, dishes=[]):
        self.dishes = dishes  
        
    def __str__(self):
        return str(self.__class__.__name__)
    
    def find_item(self, dish_type):
        for dish in self.dishes:
            if dish.type == dish_type:
                return dish
        return self.ERROR_DISH  


class BreakfastMenu(Menu):
    MULTI_DISH_ALLOWED = DishType.DRINK

    
class DinnerMenu(Menu):
    MULTI_DISH_ALLOWED = DishType.SIDE


class FinishedMeal():
    def __init__(self):
        self.serving_plate = []

    def dish_already_on_the_plate(self, item):
        for dish in self.serving_plate:
            if dish.type == int(item):
                return True
        return False
        

    def add_dish(self, menu, item):
        if self.dish_already_on_the_plate(item) and int(item) != menu.MULTI_DISH_ALLOWED:
            self.serving_plate.append(menu.ERROR_DISH)
            raise Exception("this dish cannot be served twice : %s" % item)
        self.serving_plate.append(menu.find_item(int(item)))

    def arrange_dishes(self):
        self.serving_plate.sort(key=lambda obj:obj.type)
        return self.serving_plate


    def find_multiple_dishes(self):
        counter_dic = {}
        for dish  in self.serving_plate:
            if dish.name in counter_dic:
                counter_dic[dish.name] +=1 
            else:
                counter_dic[dish.name] = 1
        multiple_dishes =  [{dish:count} for dish,count in counter_dic.iteritems() if count>1]       
        return multiple_dishes[0] if len(multiple_dishes) > 0 else {}

   
    def presentation(self):
        new_plate=[]
        multiple_dishes = self.find_multiple_dishes()
        for dish in self.serving_plate:
            if dish.name in multiple_dishes:
                dish_name = dish.name + '(x%s)' % multiple_dishes[dish.name]
            else: 
                dish_name = dish.name
            if dish_name not in new_plate:
                new_plate.append(dish_name) 
        return ', '.join(new_plate)

    def __eq__(self, other):
        return self.serving_plate == other.serving_plate

class OrderValidator():
    def __init__(self, order=None):
        self.order = order
        self.time_of_day = None
        self.menu_items = []
        
    def validate_order(self):
        if self.order is not None:
            parts = self.order.split(',') 
        if self.order is None or len(parts) == 0:
            return 'Nothing ordered!!!'
        
        if parts[0].lower().strip() not in ['morning', 'night']:
            return 'time of day should be morning or night... we are simple.' 
        self.time_of_day = parts[0].lower().strip()
        self.menu_items = parts[1:]
        return True
        

class MenuSelector():
    BREAKFAST_MENU = 'morning'
    BREAKFAST_MENU_ITEMS = [(DishType.ENTREE, 'eggs'), (DishType.SIDE, 'toast'), (DishType.DRINK, 'coffee')]
    DINNER_MENU = 'night'
    DINNER_MENU_ITEMS = [(DishType.ENTREE, 'steak'), (DishType.SIDE, 'potato'), (DishType.DRINK, 'wine'), (DishType.DESSERT, 'cake')]
    
    def __init__(self, menu_type):
        self.menu_type = menu_type
        
    def setup_menu(self):
        if self.menu_type == self.BREAKFAST_MENU:
            return BreakfastMenu(self.breakfast_menu_dishes)
        
        if self.menu_type == self.DINNER_MENU:
            return DinnerMenu(self.dinner_menu_dishes)
        
    @property
    def breakfast_menu_dishes(self):
        return [Dish(menu_item[0], menu_item[1]) for menu_item in self.BREAKFAST_MENU_ITEMS]
   
    @property       
    def dinner_menu_dishes(self):
        return [Dish(menu_item[0], menu_item[1]) for menu_item in self.DINNER_MENU_ITEMS]
    


    
class ProcessOrder():
    def __init__(self, menu):
        self.menu = menu
        
    def prepare_meal(self, order_items):
        try:
            meal = FinishedMeal()
            for item in order_items:
                meal.add_dish(self.menu, item)
        except Exception, e:
            ## uh uh - exception was raise, we would log it here, but give the customer what he wanted....
            pass
        finally:
            meal.arrange_dishes()
            return meal

    def present_meal(self, order_items):
        prepared_meal = self.prepare_meal(order_items)
        return prepared_meal.presentation()
        
   

if __name__ == '__main__':
    print "welcome to this this low-key diner! menu slection: 1- entree; 2 - side 3 - drink, 4 - dessert"
    order_str = 'please enter your order in form of "time of day (morning or night), list of numbers of dishes from the above menu separated by commas" : '
    if version_info[0] > 2:
        order = input(order_str)
    else:
        order = raw_input(order_str)
        
    print "processing order : " , order
    waiter = OrderValidator(order)
    if waiter.validate_order():
        menu = MenuSelector(waiter.time_of_day).setup_menu()
        chef = ProcessOrder(menu)
        print "here is your meal: %s " % chef.present_meal(waiter.menu_items)
        
        
