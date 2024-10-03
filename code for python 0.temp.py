# -*- coding: utf-8 -*-
r"""
Spyder Editor

This temporary script file is located here:
C:\Users\cmahone6\.spyder2\.temp.py
"""

# import modules
from scipy import misc  
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import copy
import numpy.ma as ma

# Variables that can be changed'
brainmap = 'PAX3.png'    #The name of your file that holds the brain template
mouse_names = 'h'     # The prefix for all your injection site drawings

# Don't change this code!!!
mask_brain_value = 254.0    #Value below which template should be transparent

brain = misc.imread(brainmap)   #load brain template 

mouse_injections = glob(mouse_names + '*.png')  #Load and overlay injection site files into 3D array
inj_sites = list(mouse_injections)

        
for i in np.arange(np.size(mouse_injections)):        
    inj_sites[i] = misc.imread(mouse_injections[i]);


injection_array = np.empty([np.size(brain[:,0,0]), np.size(brain[0,:,0]), np.size(mouse_injections)])

for i in np.arange(np.size(mouse_injections)):
    injection_array[:,:,i] = inj_sites[i];
    
    
zed_sum = np.sum(injection_array, axis = 2); # Sum each pixel in injection site 3D array to make a 2D array

cmap_inj = copy.copy(plt.cm.get_cmap('jet_r')) #Set colour scheme for injection site heat map (includes masking white space)
cmap_inj.set_over(alpha = 0.0);
mask_inj_value = 255.0 * np.size(mouse_injections) - 1  
 
cmap_brain = copy.copy(plt.cm.get_cmap('gray')) #Set colour scheme for drawing brain template 
cmap_brain.set_over(alpha = 0.0)

#Drawing the image
inj_heatmap = plt.figure()
ax = inj_heatmap.add_subplot(111)

injection_fig = plt.imshow(zed_sum, cmap = cmap_inj, vmax = mask_inj_value);
brain_fig = plt.imshow(brain[:,:,0], cmap = cmap_brain, vmax = mask_brain_value);

heat_ticks = range(0,np.size(mouse_injections)*255,255) #Make colour bar with labels
heat_labels = range(np.size(mouse_injections),0,-1)

for i in np.arange(np.size(heat_ticks)):
    heat_labels[i] = str(heat_labels[i])

cbar = inj_heatmap.colorbar(injection_fig, ticks = heat_ticks, orientation='vertical')
cbar.ax.set_yticklabels(heat_labels)
cbar.ax.invert_yaxis()


