graphFitter2.py:

What it does:
	It reads all the qTables, and uses them to form a the spectra and solve for the spacing
	Take a look at my weekly report for 6/10 to get details and physical reasonings
	Also the code is commented, so take a look at that too

Input:
	Requires the qTables to run
	They need to be organized like they are
	The naming convention is "#" + "#" + qtable where the first number is chain length and second is spacing
	
Output:
	Outputs all the interpolated csv files (Program doesnt use these, only generates them)
	Outputs a file called "to_plot.txt" 
		-This file contains the plot for a certain spacing


Note: graphFitter.py is just a relic