# Data acquisition and processing 
In this section, we will focus on how to obtain option data and make time judgments.
Two functions are defined: get_min is used to obtain option data at the minute level, and is_in_time is used to determine whether the current time is within the trading time.

# Trading strategy implementation
The trading strategy is the core part of the entire system, which determines when to buy or sell options.
In this function, the TA-Lib library is used to calculate the Bollinger Bands and MACD indicators. Based on these indicators, it is determined whether the conditions for buying or selling are met.

# Order operation
Placing an order is to convert trading signals into actual trading behavior
Here, two functions are defined: buy is used to perform buying operations, and sell is used to perform selling operations. The specific order logic needs to be written according to the actual situation, either through the qmt interface or through pyautogui simulated page operations.

# Scheduled tasks and execution 

In order to implement scheduled execution tasks, we need to use Python's schedule library
Here, a scheduled task function named job and a main function named start are defined. The start function executes the my_task function every 1 second and checks in an infinite loop whether there are tasks to be executed.
