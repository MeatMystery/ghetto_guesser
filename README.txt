GhettoGuessr - Chase Varvayanis 2024

------------------------------------------------------------------------------------------------------------

HOW TO LAUNCH GAME:
    Play by running PLAY_GHETTO_GUESSR.py

    Requires the following dependencies not included in Python by default:
        requests
        Pillow
        beautifulsoup4

    install all dependencies before running the game for the first time with the following command
    in a terminal for each dependency needed:
        pip install <dependency name>

------------------------------------------------------------------------------------------------------------

RULES & GAMEPLAY:
    An up to 4 player game where players attempt to guess the price of the fine listings that can be found on
    craigslist.

    Scoring is based on a combination of GeoGuessr and Price is Right rules; The closer you get to the actual
    price, the more points you get. BUT if you go over, you earn no points. There are a maximum of 10,000 points
    to be earned per round over five rounds, with a perfect game resulting in 50,000 points (hard to do)

------------------------------------------------------------------------------------------------------------

KNOWN ISSUES AND MISSING FEATURES:
    - No launcher window, boots straight into game
    - If no one guesses/leaves all guess fields blank for whole game, game results in a tie.
    - 'Next Round' button still displayed on last round, not a functional issue but does not make sense,
      should probably read 'Results' or something
    - Not every price in descriptions/titles is completely or properly redacted
    - May be issues with window being cut off on low resolution displays, program was built and tuned on a 
      1080p display
    - Mac/Linux rendering issues

------------------------------------------------------------------------------------------------------------

OTHER INFO:
    This game is a remake of 'Ghetto Price is Right' from 2022 CCOMP-11p class Originally by Story on the
    Programming Discord, re-made Chase Varvayanis. ChatGPT used to help resolve syntax issues & make docstring 
    format prettier linted w/ FLAKE8, spellchecked w/ StreetSideSoftware's Spell Checker. Stack Overflow used where 
    referenced.
