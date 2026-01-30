#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:25:01 2021

@author: kendrick shepherd
"""

import math
import numpy as np
import sys

# length of the beam
def Length(bar):
    # find a node of the bar
    bar_node = bar.init_node
    # convert the node and bar to a vector
    bar_vector = BarNodeToVector(bar, bar_node)
    # find the length of vector
    length = VectorTwoNorm(bar_vector)
    # output the vector length
    return length

# Find two norm (magnitude) of a vector
def VectorTwoNorm(vector):
    norm = 0
    for i in range(0,len(vector)):
        norm += vector[i]**2
    return np.sqrt(norm)

# Find a shared node between two bars
def FindSharedNode(bar_1,bar_2):
    return

# Given a bar and a node on that bar, find the other node
def FindOtherNode(node,bar):
    if(bar.init_node == node):
        return bar.end_node
    elif(bar.end_node == node):
        return bar.innit_node
    else:
        sys.exit("The input node is not on the bar")
        
# Find a vector from input node (of the input bar) in the direction of the bar
def BarNodeToVector(origin_node,bar):
    other_node = FindOtherNode(origin_node, bar)
    origin_loc = origin_node.location
    other_loc = other_node.location
    vec = [other_loc[0]-origin_loc[0], other_loc[1]-origin_loc[1]]
    return vec


# Convert to bars that meet at a node into vectors pointing away from that node
def BarsToVectors(bar_1,bar_2):
    return

# Cross product of two vectors
def TwoDCrossProduct(vec1,vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]

# Dot product of two vectors
def DotProduct(vec1,vec2):
    dot = 0
    for i in range(len(vec1)):
       dot += vec1[i] * vec2[i]
    return dot

# Cosine of angle from local x vector direction to other vector
def CosineVectors(local_x_vec,other_vec):
    return DotProduct(local_x_vec, other_vec) / (VectorTwoNorm(local_x_vec) * VectorTwoNorm(other_vec))

# Sine of angle from local x vector direction to other vector
def SineVectors(local_x_vec,other_vec):
    return TwoDCrossProduct(local_x_vec, other_vec) / (VectorTwoNorm(local_x_vec) * VectorTwoNorm(other_vec))

# Cosine of angle from local x bar to the other bar
def CosineBars(local_x_bar,other_bar):
    return

# Sine of angle from local x bar to the other bar
def SineBars(local_x_bar,other_bar):
    return
