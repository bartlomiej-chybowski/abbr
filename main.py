import curses

screen = curses.initscr()
screen.refresh()
curses.napms(3000)
curses.endwin()
