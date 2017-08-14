# Traveling-Salesman-Ideas
This repository will contain a list of ideas I have had about the Traveling Salesman problem. They will each be compared vs Nearest Neighbor to see if they are reasonable solutions. All run-times are calculated before the defined function.

NOTE: All ideas in this repository are my own. As far as I am aware, no one else has come up with solutions like these. I do not expect any of these to beat NN, but it is a fun thing to try with. 

NOTE: All solutions are run vs NN 4500 times; 500 itterations on each incriment of nodes from 10 to 100. Total results are listed at the end.

NOTE: Feel free to build off of my ideas. If you discover something, let me know! I'd love to hear what other people have come up with!




RESULTS:
    NN is still the defending champion. Out of ~46k test results for each trial version of any of the ideas, NN always wins with at least 66% of the routes won. 
    
    Divide and Conquer (original) is so far the closest with 33% win rate.
    Insertion is the next best.
    Selection is by far the worst due to its N^3 run time, but still wins some.
    Divide and Conquer V2 is about on par with Selection, but in terms of win rate.
    
    Overall: NN is still the best.
