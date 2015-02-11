'''
Created on Feb 11, 2015

@author: adudko
'''
import unittest
from diner_menu import Dish, OrderValidator, MenuSelector,\
    BreakfastMenu, DishType, DinnerMenu, FinishedMeal, ProcessOrder, Menu



class Test(unittest.TestCase):


    def testDish(self):
        dish = Dish(1, 'some dish')
        self.assertEquals(1, dish.type)
        self.assertEquals('some dish', dish.name)
    
    def testMenu(self):
        dish1 = Dish(1, "some dish")
        dish2 = Dish(2, "another dish")
        menu = Menu([dish1, dish2])
        self.assertEquals(2, len(menu.dishes))
        
    def testBreakfastMenuMultiDish(self):
        menu = BreakfastMenu([])
        self.assertEquals(DishType.DRINK, menu.MULTI_DISH_ALLOWED)
        
    def testDinnerMenuMultiDish(self):
        menu = DinnerMenu([])
        self.assertEquals(DishType.SIDE, menu.MULTI_DISH_ALLOWED)
        
        
    def testOrderValidator(self):
        validator = OrderValidator()
        self.assertEqual('Nothing ordered!!!', validator.validate_order())
        
        validator = OrderValidator("afternoon")
        self.assertEquals("time of day should be morning or night... we are simple.", validator.validate_order())
        
        validator = OrderValidator("morning, ")
        validator.validate_order()
        self.assertEquals('morning', validator.time_of_day)
        
        validator = OrderValidator("night , ")
        validator.validate_order()
        self.assertEquals('night', validator.time_of_day)
        
        validator = OrderValidator('morning,1,2,33')
        self.assertTrue(validator.validate_order())
        self.assertEquals('morning', validator.time_of_day)
        self.assertEquals(['1','2','33'], validator.menu_items)
        
    def test_setup_breakfast_menu(self):
        expected_dishes = [Dish(1, 'eggs'), Dish(2, 'toast'), Dish(3, 'coffee')]        
        menu_selector = MenuSelector('morning')
        self.assertEquals(expected_dishes, menu_selector.breakfast_menu_dishes)
        menu = menu_selector.setup_menu()
        self.assertEquals('BreakfastMenu', str(menu))

    def test_setup_dinner_menu(self):
        expected_dishes = [Dish(1, 'steak'), Dish(2, 'potato'), Dish(3, 'wine'), Dish(4, 'cake')]        
        menu_selector = MenuSelector('night')
        self.assertEquals(expected_dishes, menu_selector.dinner_menu_dishes)
        menu = menu_selector.setup_menu()
        self.assertEquals('DinnerMenu', str(menu))     
        
    def test_find_item_on_menu(self):
        menu = Menu([Dish(1, "dish1"), Dish(2, "dish2"), Dish(3, "dish3)")])
        self.assertEquals(Dish(2, "dish2"), menu.find_item(2))
        
    def test_item_not_on_menu(self):
        menu = Menu([Dish(1, "dish1"), Dish(2, "dish2"), Dish(3, "dish3)")])
        self.assertEquals(Dish(99, "error"), menu.find_item(4))    
        

    def test_meal_preparation(self):
        menu = Menu([Dish(1, "dish1"), Dish(2, "dish2"), Dish(3, "dish3")])
        chef = ProcessOrder(menu)
        expected = FinishedMeal()
        expected.serving_plate = [ Dish(2, "dish2"), Dish(3, "dish3")]
        self.assertEquals(expected, chef.prepare_meal(['2', '3']))

        
    def test_adding_dish(self):
        menu = Menu([Dish(1, "dish1"), Dish(2, "dish2"), Dish(3, "dish3")])
        meal = FinishedMeal()
        meal.add_dish(menu, '2')
        self.assertEquals([Dish(2, "dish2")], meal.serving_plate)
        meal.add_dish(menu, '1')
        self.assertEquals([Dish(2, "dish2"), Dish(1, "dish1")], meal.serving_plate)
        
    def test_dish_already_on_plate(self):
        menu = Menu([Dish(1, "dish1"), Dish(2, "dish2"), Dish(3, "dish3")])
        meal = FinishedMeal()
        self.assertFalse(meal.dish_already_on_the_plate('1'))
        meal.add_dish(menu, '2')
        self.assertTrue(meal.dish_already_on_the_plate('2'))
        
        

    def test_add_invalid_dish(self):
        menu = Menu([Dish(1, "dish1"), Dish(2, "dish2"), Dish(3, "dish3")])
        menu.MULTI_DISH_ALLOWED = 2
        meal = FinishedMeal()
        meal.add_dish(menu, '2')
        meal.add_dish(menu, '2')
        self.assertEquals([Dish(2, "dish2"), Dish(2, "dish2")], meal.serving_plate)   
        meal.add_dish(menu, '1')
        try:     
            self.assertRaises(Exception("this dish cannot be served twice : 1"), meal.add_dish, menu, '1')
        except:
            pass
        finally:
            self.assertEquals([Dish(2, "dish2"), Dish(2, "dish2"), Dish(1, "dish1"), Dish(99, "error")], meal.serving_plate)


    def test_meal_presentation(self):
        finished_meal = FinishedMeal()
        finished_meal.serving_plate = [Dish(1, 'dish1'), Dish(4, 'dish4'), Dish(3,'dish3'), Dish(2,'dish2')]
        expected = [Dish(1, 'dish1'), Dish(2,'dish2'), Dish(3,'dish3'), Dish(4, 'dish4'), ]
        self.assertEquals(expected, finished_meal.arrange_dishes())
        

    def test_find_multiple_dishes(self):
        meal = FinishedMeal() 
        meal.serving_plate=[Dish(1, 'dish1'), Dish(2,'dish2'), Dish(2,'dish2'), Dish(3,'dish3'), Dish(4, 'dish4'), ]
        self.assertEquals ({'dish2':2} , meal.find_multiple_dishes())
        
    def test_consolidate_dishes(self):
        meal = FinishedMeal()
        meal.serving_plate=[Dish(1, 'dish1'), Dish(2,'dish2'), Dish(2,'dish2'), Dish(3,'dish3'), Dish(4, 'dish4'), ]
        self.assertEquals('dish1, dish2(x2), dish3, dish4', meal.presentation())
        


if __name__ == "__main__":
    unittest.main()
    