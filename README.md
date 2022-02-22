# PrinterWatch

The Project was seeded in an 'organisation' ~200 employees with 50+ printers ( 4 of them are leased ) 18 different models from 2 manufacturers 
leading to 45 different toners that need to be in storage if needed.

Main Focus:
      Monitor all Printer cartridge type and the current fill % and provide a interface to make everything easy to monitore

In the process it made sense to get some additional data like Location, Page Count, Notes (to add some info manualy) and if there was already a continues
stream of information recieved from all printers why not store them for further analitic processing to help structure the network more efficient.
so i aimed for analysing the cost efficency of each printer (the manufacturer estimation is not always that accurate) the amount of prints made over time for each location
and the average cartridge usage over time.

Some Information to my Person:
I was just 3 month into Python programming when i started this Project with only some  C++ experience ( exclusivly used for programming microcontroller) 
and some simple cmd/batch scripts made prior and i encountered many different proplems that are not always solved as elegant as they could.

current the code lacks decent deployability (working on that) and graphical visualisation of the analized data is only hard coded and a gui for creation of different plots
with a selection of datasets is planed but most likely will end up in a seperate modul.

about the deployablity since there is no SNMP library for python with running windows support i had to install

  Name:			net-snmp-5.4.2.1-1.win32.exe
  URL:			http://www.net-snmp.org
  Build date:		November 2nd, 2008
  Built by:		Alex Burger <alex_b@users.sourceforge.net>
  Installer Package by: Andy Smith <wasmith32@users.sourceforge.net>
  NSIS Compiler:	Version 2.3
