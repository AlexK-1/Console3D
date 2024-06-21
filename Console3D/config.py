import os


width = os.get_terminal_size().columns  # The width of the terminal/console, automatic detection by default
height = os.get_terminal_size().lines  # The height of the terminal/console, automatic detection by default
font_width = 8  # The width in pixels of the terminal/console symbol
font_height = 16  # The height in pixels of the terminal/console symbol

max_re_reflections = 2  # Maximum number of re-reflections

debug = False