import os


width = os.get_terminal_size().columns  # автоматическое определение ширины и высоты терминала
height = os.get_terminal_size().lines
font_width = 8  # ширина и высота одного символа терминала (можно найти в свойствах терминала, раздел шрифт)
font_height = 16

max_re_reflections = 2
