# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:14:27 2016
Program to check if a statement is less than the 140character
limit for twitter before adding it to work.txt
@author: Gareth Miller
"""
import os, string
fileObject = open("work.txt", "a")
phrase = input("Please enter the desired phrase to be checked: ")
if len(phrase) < 130:
    print("Phrase added!")
    fileObject.write('\n')
    fileObject.write(phrase)
    fileObject.close
else:
    print("Too long!")
    print("How about...")
    for c in string.punctuation:
        phrase = phrase.replace(c,"")
    print(phrase)
    answer = input("Is that ok? Y or N: ")
    if answer == "Y" and len(phrase) < 130:
        fileObject.write('\n')
        fileObject.write(phrase)
        fileObject.close
        print("Phrase added")
    else:
        print("Sorry!")

