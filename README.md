# Summation calculator  

### HOW TO USE:  
For {param} pattern:  
- Enter a string that represents your equation :  
    - Implicit multiplication is not recognized  
    - No whitespace characters present  
    - Power is represented by '^' (Does not Work Yet) 
    - To represent a negative number's power, use this format (-x^y).
    - To exclude the negative, use this format -(x^y) 
    
For {param} summed_var:  
- Enter the character with which you want to represent the variable that will be summed:   
    - Must be a single character  
    - Must be consistent with {param} pattern  
    
For {param} summed_to_var_with_equal:  
- Enter a string containing the variable you will use to represent the end value, an equal sign, and the end value:  
    - Example : "j=10"   
    - No whitespace characters present  
    - End value must be a positive integer  
    - Must be consistent with {param} pattern  