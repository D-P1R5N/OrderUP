# OrderUP
PoS system for educational purposes

This was started as an educational project to create dynamic and appealing GUIs. 

The project has a large list of features in development ranging from user interface to data management and network compatibility. A proposed feature being researched is allowing customers to place their own order with their own profile. 

Extensions in progress
    
      Host related features;
  
      Table management
   
      Chef features [including dynamic inventory management and recipe management and touchscreen ticket response]
   
      Expodite features [including computer vision assisted order tracking] 
   
      Customer databasing
   
      Data interpretation / visualization [real time graphing or general purpose graphing from data sources]
   
# Updates:
7.17.2020

    The setup.py file has been added to the file directory; this setup creates the necessary database to be used for the program. It also instantiates default values so that you have basic categories for menu items commonly found on most menus. The employee table is given a default value, but I have not programmed an interface to add employees. 

7.18.2020

    The setup.py has been updated to expand the database.
    The style option has been moved to an external text file and parsed with JSON
    An employee window has been created to add Employees to the database
    The OrderMenu now passes the data from ordering around as a data structure instead of seperate pieces of info. 
    
9.7.2020
    
    The OrderMenu has been rewritten to be more asthetically pleasing and the style code has been temporarily added to the top of the file.
    A KitchenView window has been added to the file list, which checks the database for active tickets and creates the necessary widgets to process from an expediter position.
    There is a small bug currently with the individual Main.Ticket.ticket_timer() function where all the tickets will reference the last Ticket's thread. 
    
9.22.2020

    The kitchen_a.py file has been added. This file offers flexible task handling of tickets and a time-based ticket progressbar. There is also a functional clock. 
