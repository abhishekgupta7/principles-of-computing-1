"""
Merge function for 2048 game.
"""

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



