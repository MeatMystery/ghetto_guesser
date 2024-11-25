# GhettoGusser - Remake of 'Ghetto Price is Right' from 2022 CCOMP-11p class
# Originally by Story on the Programming Discord, re-made Chase Varvayanis

# x

# last revision 11-14-2024
 

import os
import requests
from bs4 import BeautifulSoup
from random import sample


def link_list_trimmer(filename):
    """
    gathers 15 randon links from the craigslist search results, and stores to a list
    """
    all_links = []
    
    parent_folder = os.path.dirname(os.path.abspath(__file__))
    file_to_open = os.path.join(parent_folder, filename)
    
    with open(file_to_open) as file:
        for line in file:
            all_links.append(line.rstrip())
    
    all_links = all_links[2:]

    trimmed_list = sample(all_links, 15)

    return trimmed_list


def round_maker():
    pass


# Test Code
if __name__  == '__main__':
    print(link_list_trimmer('cl_listings_file.txt'))


