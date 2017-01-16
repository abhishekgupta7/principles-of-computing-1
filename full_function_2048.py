"""
Clone of 2048 game.
"""

import poc_2048_gui
from random import randint
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # length of line
    length = len(line)
    
    if length == 0 :
        return line
    result  = line[:]
    
    current = 0
    while current< length :
        val = result[current]
        nextp = current+1
        
        while(nextp < length and result[nextp] == 0 ) :
            nextp = nextp+1
            
        if(nextp == length) :
            return result
        
        if(val == result[nextp]) :
            result[current] = val * 2
            result[nextp] = 0
            
        elif(val == 0) :
            result[current] = result[nextp]
            current = current-1
            result[nextp] = 0
            
        elif(current+1 != nextp):
            result[current+1] = result[nextp] 
            result[nextp] = 0

            
        current = current+1
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    
    def __init__(self, grid_height, grid_width):
        self.__height = grid_height
        self.__width = grid_width 
        self.__mygrid = [[row+col for col in range(self.__width)]
                           for row in range(self.__height)]
        self.__dicend = {}
        up_end = set()
        for  start_width in range(grid_width) :
            up_end.add((0,start_width))
        self.__dicend[UP] = up_end
        down = set()
        for  start_width in range(grid_width) :
            down.add((grid_height-1,start_width))
        self.__dicend[DOWN] = down
        
        left = set()
        
        for  start_height in range(grid_height) :
            left.add((start_height,0))
        self.__dicend[LEFT] = left
        
        right = set()
        for  start_height in range(grid_height) :
            right.add((start_height,grid_width-1))
        self.__dicend[RIGHT] = right
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self.__emptyl = []
        for s_row in range(self.__height) :
            for s_col in range(self.__width) :
                self.__mygrid[s_row][s_col] = 0
                self.__emptyl.append((s_row,s_col))
        self.new_tile()        
        self.new_tile()        

    def cal_empty(self) :
        """
        Calculate empty places in the grid
        """
        # replace with your code
        self.__emptyl = []

        for s_row in range(self.__height) :
            for s_col in range(self.__width) :
                if(self.__mygrid[s_row][s_col] == 0) :
                    self.__emptyl.append((s_row,s_col))
        
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        empty_string = ""
        for s_row in range(self.__height):
             empty_string = empty_string+ str(self.__mygrid[s_row])
        return empty_string       

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.__height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.__width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        list_end = self.__dicend[direction]
        max_len = 0
        if len(list_end) == self.__height :
            max_len = self.__width
        else :
            max_len = self.__height
        is_moved = False   
        for end in list_end :
            actual_list = []
            row = end[0]
            col = end[1]
            for dummy_len in range(max_len) :
                actual_list.append(self.__mygrid[row] [col])
                row = row + OFFSETS[direction][0]
                col = col + OFFSETS[direction][1]
            
            new_list = merge(actual_list)
            
            row = end[0]
            col = end[1]
            
            for s_row in range(max_len) :
                self.__mygrid[row] [col]  = new_list[s_row]
                if(new_list[s_row] != actual_list[s_row]) :
                    is_moved = True;
                row = row + OFFSETS[direction][0]
                col = col + OFFSETS[direction][1]
                
        if(is_moved) :
            self.new_tile()
       
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
             
        self.cal_empty()
    

        ac_len = len(self.__emptyl)
        if( ac_len == 0) :
            return
        
        ran_pos = self.__emptyl.pop(random.randint(0, ac_len-1))
        rand_val = random.randint(0,9)
        ac_value = 2
        if(rand_val == 4) :
            ac_value = 4
        self.__mygrid[ran_pos[0]][ran_pos[1]] = ac_value
        
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        
        if(row >= self.__height or col >=  self.__width) :
            return
        self.__mygrid[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        #return 0

        return self.__mygrid[row] [col]


poc_2048_gui.run_gui(TwentyFortyEight(2, 3))



