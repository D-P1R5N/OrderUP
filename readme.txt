'''Hello User, the setup file creates a basic database for interactions with
OrderUP application. Feel free to add tables or fields to the database. The
following patterns should persist through-out the life-cycle of your program:

    Employees :
      Field 1 : Password
      Field 2 : Employee name (Last,First)
      -Optional information can be added and will be supported in the future

    Items:
      Field 1 : Item Name
      Field 2 : Item Price
      Field 3 : Item Sub-Category (see Sub_Cat table)
      Field 4 : Description
      -Optional fields can be added but aren't currently supported

    Main Category:
      Field 1 : ID
      Field 2 : Title

    Sub Category:
      Field 1 : ID
      Field 2 : Title
      Field 3 : Main Category ID'

    Active Orders:
      Field 1 : Table Number
      Field 2 : Ticket Info
      Field 3 : Time
      -Optional Field 4 : Date

    Customer Sales:
      Field 1 : ID
      Field 2 : Date
      Field 3 : Time
      Field 4 : Payment Total
      Field 5 : Payment Type
      -Optional fields can be added but aren't supported
'''
