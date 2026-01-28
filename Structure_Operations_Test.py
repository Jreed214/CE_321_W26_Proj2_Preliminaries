#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:34:19 2021

@author: kendrick shepherd
"""

import sys

# determine if the bar is statically determinate (and belongs to a truss)
def StaticallyDeterminate(nodes,bars):                 
    # Determine the number of nodes in the truss
    n_nodes = len(nodes)
    n_bars = len(bars)
    
    # Determine number of (valid) reactions supported by nodes of the truss
    n_reactions = 0
    for node in nodes:
        if(any(node.ConstraintType())):
            if(2 in node.ConstraintType()):
                sys.exit("Truss cannot support a moment reaction force")
            elif(-1 in node.ConstraintType()):
                sys.exit("Invalid constraint type specified for the truss")
            else:
                n_reactions += len(node.ConstraintType())
    
    # Compute if b + r = 2j (Equation 3-1 of the textbook)
    if(n_bars + n_reactions < 2*n_nodes):
        sys.exit("The truss is unstable; did you input all of the reaction constraints correctly?")
    elif(n_bars + n_reactions > 2*n_nodes):
        sys.exit("The truss is statically indeterminate, and cannot be resolved using method of joints")
    else:
        return True
 
def ComputeReactions(nodes):
    # assume that there is one pin and one roller for our statically determinate structure
    n_pins = 0
    n_roller = 0
    for node in nodes:
        if(node.constraint=="pin"):
            pin_node = node
            n_pins += 1
        elif(node.constraint=="roller_no_xdisp"):
            roller_node = node
            n_roller += 1
        elif(node.constraint=="roller_no_ydisp"):
            roller_node = node
            n_roller += 1
    
    if(n_pins != 1 or n_roller != 1):
        sys.exit("A more clever way must be found to compute the reaction forces")
    
    # Continue from here
    # Sum of moments about the pin

          # gets the x and y coordinate of the node corresponding to the pin 
    [pin_x,pin_y] = pin_node.location
          # gets the x and y coordinate of the node associated with the roller
    [roller_x, roller_y] = roller_node.location

    roller_reaction = 0.0
    for node in nodes:
       [node_x, node_y] = node.location
        # contributions in the y direction
       roller_reaction += node.yforce_external * (node_x - pin_x)
        # contributions in the x direction
       roller_reaction += node.xforce_external * (pin_y - node_y)
       
    if roller_node.constraint == "roller_no_xdisp":
         roller_reaction = -roller_reaction / (pin_y - roller_y)
         roller_node.AddReactionXForce(roller_reaction)
        # runs if the roller supports forces in the x direction
        
    elif roller_node.constraint == "roller_no_ydisp":
         roller_reaction = -roller_reaction / (roller_x - pin_x)
         roller_node.AddReactionYForce(roller_reaction)
         # second computes if the roller supports forces in the y direction
         
         #The computed forces are then stored using the appropriate object function for the node.
        

    # sum of forces in y direction
    sum_Fy = 0.0
    for node in nodes:
     sum_Fy += node.yforce_external
 
    if roller_node.constraint == "roller_no_xdisp":
     # ΣFy = ΣP F_Py + R_piny = 0
     pin_node.AddReactionYForce(-sum_Fy)
    elif roller_node.constraint == "roller_no_ydisp":
     # ΣFy = ΣP F_Py + R_rollery + R_piny = 0
     pin_node.AddReactionYForce(-(sum_Fy + roller_reaction))

# 

    # sum of forces in x direction
    sum_Fx = 0.0
    for node in nodes:
     sum_Fx += node.xforce_external
 
    if roller_node.constraint == "roller_no_xdisp":
     # ΣFx = ΣP F_Px + R_rollerx + R_pinx = 0
     pin_node.AddReactionXForce(-(sum_Fx + roller_reaction))
    elif roller_node.constraint == "roller_no_ydisp":
     # ΣFx = ΣP F_Px + R_pinx = 0
     pin_node.AddReactionXForce(-sum_Fx)
