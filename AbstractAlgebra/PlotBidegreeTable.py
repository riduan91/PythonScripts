# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:15:34 2017

@author: ndoannguyen
"""

import numpy as np

REDUCTION = 0
COL = ['red', 'blue', 'green', 'orange', 'black']

"""
def plotAction(mymod, source_bidegrees, actions, rank, max_x, max_y):
         
    ax = plt.gca()
    ax.set_autoscale_on(False)
    ax.set_xticks(np.arange(0, max_x + 2, 1))
    ax.set_yticks(np.arange(0, max_y + 2, 1))
    

    index = 0
    for action in actions:
        connection_table = mymod.findConnectionsByActionWithLimit(source_bidegrees, action, abs(max_x) + abs(max_y))
        x = [term[0][0] + 0.5 for term in connection_table if term[0][0] > -999] + [term[1][0] + 0.5 for term in connection_table if term[1][0] > -999]
        y = [term[0][1] + 0.5 for term in connection_table if term[0][1] > -999] + [term[1][1] + 0.5 for term in connection_table if term[1][1] > -999]  
               
            
        new_con_tab = [(term[0][0] + 0.5, term[0][1] + 0.5, term[1][0] + 0.5, term[1][1] + 0.5) for term in connection_table if term[1][0] >= 0 and term[1][1] >= 0 ]    


        for (x1, y1, x2, y2) in new_con_tab:
            
            if (x1 == x2):
                r1 = 0
            else:
                r1 = REDUCTION
            if (y1 == y2):
                r2 = 0
            else:
                r2 = REDUCTION
                ax.arrow(x1 + r1 , y1 + r2, x2 - x1 - 2 * r1, y2 - y1 - 2 * r2, head_width = 0.15, head_length = 0.15, color = COL[index % len(COL)])
        index += 1
    
        plt.scatter(x, y, marker='x', s = 32, color = 'red') 
    plt.grid()
    plt.show()
"""

def writeToTex(mymod, source_bidegrees, actions, max_x, max_y, outputfile):
    
    f = open(outputfile, 'w')
    
    """
    f.write("\documentclass{article}\n\n")
    f.write("\usepackage{tikz}\n")
    f.write("\pagenumbering{gobble}\n")
    f.write("\usepackage{pgflibraryarrows}\n\n")
    
    f.write("\usepackage[paperwidth= %.1fcm, paperheight= %.1fcm, margin= 4.0cm]{geometry}\n" % (max_x + 0.5, max_y + 0.5))
    f.write("\\begin{document}\n")
    """
    
    s = "\\begin{figure}\n"
    s += "\\begin{tikzpicture}[scale=0.8]"
    s += "\clip(-1.5,-1.5) rectangle (%.1f,%.1f);\n" % (max_x + 0.5, max_y + 0.5)
    
    s += "\draw[color=gray] (0,0) grid [step=1] (%d , %d);\n" % (max_x, max_y)
    
    s += "\\foreach \\n in {0,1,...,%d}\n" % max_x
    s += "{\n"
    s += "\def\\nn{\\n-0}\n"
    s += "\\node[below] at (\\nn,0) {$\\n$};\n"
    s += "}\n"
    
    s += "\\foreach \s in {0,1,...,%d}\n" % max_y
    s += "{\n"
    s += "\def\ss{\s-0}\n"
    s += "\\node[left] at (-0.4,\ss,0){$\s$};\n"
    s += "}\n"
    
    index = 0
    
    for action in actions:
        connection_table = mymod.findConnectionsByActionWithLimit(source_bidegrees, action, abs(max_x) + abs(max_y))
        x = [term[0][0] for term in connection_table if term[0][0] > -999] + [term[1][0] for term in connection_table if term[1][0] > -999]
        y = [term[0][1] for term in connection_table if term[0][1] > -999] + [term[1][1] for term in connection_table if term[1][1] > -999]  
        for (term1, term2) in connection_table:
            if term1[0] >= 0 and term1[1] >= 0 and term2[0] >= 0 and term2[1] >= 0 and term1[0] <= max_x and term1[1] <= max_y and term2[0] <= max_x and term2[1] <= max_y:
                s += "\draw [->, %s] (%d, %d)--(%d, %d);\n" % (COL[index % len(COL)], term1[0], term1[1], term2[0], term2[1])      
        
        index += 1
        
    setxy = set([(x[i], y[i]) for i in range(len(x)) if x[i] >= 0 and x[i] <= max_x and y[i] >= 0 and y[i] <= max_y])
    listxy = list(setxy)
    
    for (x, y) in listxy:
        s += "\draw [fill] (%d, %d) circle [radius = 0.1]; \n" % (x, y);
    
    s += "\end{tikzpicture}\n"
    s += "\end{figure}\n"
    
    f.write(s)
    
    f.close()
    return s