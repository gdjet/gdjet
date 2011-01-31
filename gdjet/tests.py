__test__ = {"test_searchterms": """
This tests the SearchTerm Functions for correct tokenization, hookdetection.

>>> from gdjet.utils.search import *
>>> SearchTerm( "Ein Hund geht heute NOT spazieren schlafen" ).tokenize()
([['Ein'], ['Hund'], ['geht'], ['heute'], ['schlafen']], ['spazieren'])
>>> SearchTerm( "Apfel AND Banane Joghurt" ).tokenize()
([['Apfel', 'Banane'], ['Joghurt']], [])
>>> SearchTerm( "NOT Apfel AND NOT Joghurt" ).tokenize()
([], ['Apfel', 'Joghurt'])
>>> SearchTerm( "NOT Apfel NOT Joghurt" ).tokenize()
([], ['Apfel', 'Joghurt'])
>>> SearchTerm( "NOT Apfel OR NOT Joghurt" ).tokenize()
([], ['Apfel', 'Joghurt'])
>>> SearchTerm( "NOT Apfel NOT OR Joghurt" ).tokenize()
([], ['Apfel', 'Joghurt'])
>>> SearchTerm( "NOT Apfel NOT AND Joghurt" ).tokenize()
([['Joghurt']], ['Apfel'])
>>> SearchTerm( "Apfel birne:kompott vater:kind" ).hooks
{'birne': 'kompott', 'vater': 'kind'}
"""}
