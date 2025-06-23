# chatcolors.py
# 06/22/2025 - Voltur
#
# Just some terminal Colors to use. 
# 


import sys

no_color = "--no-color" in sys.argv

def _enabled():
    return sys.stdout.isatty() and not no_color

def _code(code):
    return code if _enabled() else ""

class Colors:
    reset = _code('\033[0m')
    bold = _code('\033[01m')
    italic = _code('\033[03m')
    disable = _code('\033[02m')
    underline = _code('\033[04m')
    reverse = _code('\033[07m')
    strikethrough = _code('\033[09m')
    invisible = _code('\033[08m')

    class fg:
        black = _code('\033[30m')
        red = _code('\033[31m')
        green = _code('\033[32m')
        orange = _code('\033[33m')
        blue = _code('\033[34m')
        purple = _code('\033[35m')
        cyan = _code('\033[36m')
        lightgrey = _code('\033[37m')
        darkgrey = _code('\033[90m')
        lightred = _code('\033[91m')
        lightgreen = _code('\033[92m')
        yellow = _code('\033[93m')
        lightblue = _code('\033[94m')
        pink = _code('\033[95m')
        lightcyan = _code('\033[96m')

    class bg:
        black = _code('\033[40m')
        red = _code('\033[41m')
        green = _code('\033[42m')
        orange = _code('\033[43m')
        blue = _code('\033[44m')
        purple = _code('\033[45m')
        cyan = _code('\033[46m')
        lightgrey = _code('\033[47m')

# Set up some default Colors
class ChatColors:
    text = Colors.fg.lightgrey
    system = Colors.fg.darkgrey
    sender = Colors.fg.green
    recpt = Colors.fg.purple
    highlight = Colors.fg.cyan


