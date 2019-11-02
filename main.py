import curses
from curses import wrapper, newwin
from curses.textpad import Textbox
import pandas as pd
import numpy as np


def teardown(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.doupdate()
    curses.endwin()


def search_box(stdscr):
    scr_height, scr_width = stdscr.getmaxyx()
    boxwin = newwin(4, 46, int(scr_height / 2 - 2), int(scr_width / 2 - 23))
    editwin = newwin(1, 44, int(scr_height / 2), int(scr_width / 2 - 22))
    boxwin.border(1)
    boxwin.addstr(1, 1, "Search for definition")
    boxwin.refresh()
    editwin.refresh()
    box = Textbox(editwin)
    box.edit()

    return box.gather()


def fill_pad(stdscr, definitions):
    height, width = stdscr.getmaxyx()

    num_of_rows = 0
    for item in definitions.iterrows():
        if item[1].description is not np.nan:
            num_of_rows += int(len(item[1].description) / (width - 2)) + 5
        else:
            num_of_rows += 4

    pad = curses.newpad(num_of_rows, width - 3)

    line = 0
    for item in definitions.iterrows():
        pad.addstr(line, 0, str(item[0]) + ". Abbr: " + str(item[1].abbreviation), curses.A_BOLD)
        pad.addstr(line+1, 0, "Full name: " + str(item[1].fullname))
        pad.addstr(line+2, 0, "Description: ")
        if item[1].description is not np.nan:
            pad.addstr(line+3, 0, item[1].description)
            line += int(len(item[1].description) / (width - 2)) + 5
        else:
            line += 4

    pad.refresh(0, 0, 1, 2, height - 2, width - 2)
    return pad, num_of_rows-5


def main(stdscr):
    df = pd.read_csv('test.csv')
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.start_color()
    stdscr = curses.initscr()
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.border(1)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    offset = 1
    num_of_rows = 10
    pad = None

    while True:
        c = stdscr.getch()

        if c == ord('q'):
            break
        elif c == curses.KEY_F2:
            reply = search_box(stdscr)
            try:
                definitions = df[df.abbreviation.str.lower().str.contains(reply.strip().lower())]
                stdscr.clear()
                stdscr.border(1)
                stdscr.refresh()
                pad, num_of_rows = fill_pad(stdscr, definitions)
            except Exception as e:
                stdscr.clear()
                stdscr.border(1)
                stdscr.addstr(1, 1, "Definition not found, error: " + str(e))
                stdscr.refresh()
                pad = None
        elif c == curses.KEY_UP:
            if pad is not None and offset > 0:
                offset -= 1
                pad.refresh(offset, 0, 1, 2, height-2, width-2)
        elif c == curses.KEY_DOWN:
            if pad is not None and offset < (num_of_rows - 10):
                offset += 1
                pad.refresh(offset, 0, 1, 2, height-2, width-2)

    teardown(stdscr)


wrapper(main)
