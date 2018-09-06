#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018 EPA
# Authors : J. Félix Ontañón <felixonta@gmail.com>

import re
from exceptions import Exception

VOWELS = u'aeiou'
VOWELS_TILDE = u'áéíóú'
VOWELS_CIRCUMFLEX = u'âêîôû'
VOWELS_UP = u'AEIOU'
VOWELS_TILDE_UP = u'ÁÉÍÓÚ' 
VOWELS_CIRCUMFLEX_UP = u'ÂÊÎÔÛ'

# Pre calculation of vowel groups and its variants with accents. Useful for further search & replacement
VOWELS_ALL = VOWELS + VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_NOTILDE = VOWELS + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_TILDE = VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP

# Voiceless alveolar fricative /s/ https://en.wikipedia.org/wiki/Voiceless_alveolar_fricative
VAF = u'ç'
VAF_UP = u'Ç'

# Auxiliary functions
def get_vowel_circumflex(vowel):

    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel) + 5
        return VOWELS_ALL_NOTILDE[i: i+1][0]
    elif vowel and vowel in VOWELS_ALL_TILDE:
        i = VOWELS_ALL_TILDE.find(vowel) + 5
        return VOWELS_ALL_TILDE[i: i+1][0]
    else:
        raise EPAError('Not a vowel', vowel)

def intervowel_circumflex_sub(match):
    prev_char = match.group(1)
    consonant_char = match.group(2)
    next_char = match.group(3)

    prev_char = get_vowel_circumflex(prev_char)

    if consonant_char.isupper(): 
        return prev_char + VAF_UP*2 + next_char
    else: 
        return prev_char + VAF*2 + next_char

# EPA replacement functions
def h_rules(text):
    """Supress mute 'h'"""
    text = re.sub(r'(?<!c)h', '', text, flags=re.IGNORECASE)
    return text

def x_rules(text):
    if text[0] == "X": text[0] = VAF.upper()
    if text[0] == "x": text[0] = VAF

    # Try substitution for all combination of vowels upper/lower and tildes
    for pair in [(VOWELS, VOWELS), (VOWELS_TILDE, VOWELS), (VOWELS_TILDE_UP, VOWELS), (VOWELS, VOWELS_TILDE), (VOWELS, VOWELS_TILDE_UP)]:
        text = re.sub(r'([' + pair[0] + '])(x)([' + pair[1] + '])', intervowel_circumflex_sub, text, flags=re.IGNORECASE)

    return text

def ch_rules(text):
    text = text.replace(u'ch', u'x')
    text = text.replace(u'Ch', u'X')
    text = text.replace(u'CH', u'X')
    text = text.replace(u'cH', u'x') # weird, but who knows?
    return text

# Main function
def cas_to_epa(text):
    text = unicode(text, 'utf-8')
    text = h_rules(text)
    text = x_rules(text)
    text = ch_rules(text)
    return text

class EPAError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(EPAError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors