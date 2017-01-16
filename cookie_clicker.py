"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
import math
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
  
    
    def __init__(self):
        
        self.__totalcookies = 0.0
        self.__currentcookies = 0.0
        self.__currenttime = 0.0
        self.__currentcps = 1.0
        self.__cookieshistory = []
        self.update_history(None, 0.0)
        
    def update_history(self, item_bought, item_cost) :
        """
        add to update_history
        """
       
        self.__cookieshistory.append((self.__currenttime, item_bought, item_cost,self.__totalcookies))

        
    def __str__(self):
        """
        Return human readable state
        """
        return "__totalcookies = %s , __currentcookies = %s , __currenttime = %s , __currentcps = %s" \
            %(self.__totalcookies , self.__currentcookies , self.__currenttime, self.__currentcps)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.__currentcookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.__currentcps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.__currenttime
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self.__cookieshistory[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        cookies_needed = cookies - self.get_cookies()
        if cookies_needed <= 0.0 :
            return 0.0
        return math.ceil(cookies_needed/self.get_cps())
         

    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0 :
            return
        cookies_generated = time * self.get_cps()
        self.__currenttime += time
        self.__totalcookies += cookies_generated
        self.__currentcookies += cookies_generated
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.__currentcookies < cost :
            return
        self.__currentcookies -= cost
        self.__currentcps += additional_cps
        self.update_history(item_name, cost)
        
   
    
def simulate_clicker(build_inf, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    build_info = build_inf.clone()
    click_state = ClickerState()
    next_strategy = None
    while(click_state.get_time() <= duration) :
        
        next_strategy = strategy(click_state.get_cookies(), click_state.get_cps(),click_state.get_history(), duration - click_state.get_time() ,build_info)
        if next_strategy == None :
            break
        time_needed =  click_state.time_until(build_info.get_cost(next_strategy))  
        if(time_needed + click_state.get_time() > duration) :
            break
        click_state.wait(time_needed)    
        click_state.buy_item(next_strategy,build_info.get_cost(next_strategy), build_info.get_cps(next_strategy))
        build_info.update_item(next_strategy)
    
    click_state.wait(duration - click_state.get_time())
    print click_state.get_history()
    return click_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    min_cost = float("inf")
    strategy_c = None
    for dummy_item in build_info.build_items() :
        item_cost = build_info.get_cost(dummy_item)
        min_cost = min(min_cost,item_cost)
        if min_cost == item_cost :
            strategy_c = dummy_item

    if min_cost <= time_left * cps :
        return strategy_c
        
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    max_cost = 0
    strategy_c = None
    __currentcookies = cps * time_left + cookies
    for dummy_item in build_info.build_items() :
            item_cost = build_info.get_cost(dummy_item)
            if __currentcookies >= item_cost :
                max_cost = max(max_cost, item_cost) 
                if max_cost == item_cost :
                    strategy_c = dummy_item
    print  strategy_c          
    return strategy_c

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    cookies_ratio = []
    for dummy_item in build_info.build_items() :
        dummy_ratio = build_info.get_cps(dummy_item)/build_info.get_cost(dummy_item)
        cookies_ratio.append((dummy_ratio,dummy_item))
    #print cookies_ratio
    cookies_ratio = sorted(cookies_ratio, reverse=True)
    #print "sorted"
    #print cookies_ratio
    for cost_tuple in cookies_ratio :
            if cps * time_left >= build_info.get_cost(cost_tuple[1]) :
                return cost_tuple[1]
                
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    #Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

