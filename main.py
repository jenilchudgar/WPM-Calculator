import curses
import time
from random import randint
from curses import wrapper

# Constants
NEUTRAL = 1
CORRECT = 2
WRONG = 3

def clear(stdscr):
    stdscr.clear()

def refresh(stdscr):
    stdscr.refresh()

def start_screen(stdscr):
    type(stdscr, text="Welcome to Typer Testing Pro!\nPress any key to continue... ",)

def get_current_highscore():
    with open("highscore_wpm.txt","r") as f:
        return int(f.read())

def set_highscore(score):
    with open("highscore_wpm.txt","w") as f:
        f.write(str(score))

def type(stdscr, text="", get_key=True, pair_id: int = 1,
         row: int = 0, column: int = 0,clear_=True):

    if clear_:
        clear(stdscr)
        append(stdscr,text=text, color=pair_id, row=row,column=column)

    if get_key:
        key = stdscr.getkey()
        refresh(stdscr)
        return key

    refresh(stdscr)

    

def load_random_text():
    with open("text.txt","r") as f:
        lines = f.read().split("\n")
        random_no = randint(0,len(lines)-1)
        return lines[random_no]

def wpm_test(stdscr):
    target_text = load_random_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    i=0
    while True:
        time_elapsed = max(time.time() - start_time,1)
        wpm = round((len(current_text) / (time_elapsed / 60))/5)

        # 60 wpm = 30 chars / (30 seconds / 60)  
        # 120 wpm = 30 chars / (15 seconds / 60)  

        clear(stdscr)
        display_user_entered_text(stdscr,target_text,current_text,wpm)

        if len(current_text) == len(target_text):
            stdscr.nodelay(False)
            
            game_end(stdscr,wpm)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE",'\b','\x7f'):
            if len(current_text) > 0:
                current_text.pop()

        elif len(current_text) < len(target_text):
            current_text.append(key)

        i+=1
        refresh(stdscr)


def append(stdscr,text="",row=0,column=0,color=NEUTRAL):
    stdscr.addstr(row,column,text,curses.color_pair(color))

def display_user_entered_text(stdscr,target_text,
    current_text,wpm=0):
    global acc
    append(stdscr,text=f"{target_text}")
    append(stdscr,text=f"WPM: {wpm}",row=1,column=0)
    
    if get_current_highscore() < int(wpm):
        set_highscore(wpm)

    acc = 0
    for i,char in enumerate(current_text):
        correct_char = target_text[i]
        our_char = current_text[i]

        if correct_char==our_char:
            append(stdscr,text=char,color=CORRECT,row=0,column=i)
            acc+=1
        else:
            append(stdscr,text=correct_char,color=WRONG,row=0,column=i)
        append(stdscr,text=f"Accurary: {round((acc/len(target_text))*100)}%",row=2,column=0)
        

def game_end(stdscr,wpm):
    type(stdscr,text=f"The test ended!\nWPM: {wpm} \nAccuray: {acc}%\nWould you like to play again? [y/n]",get_key=False)
    key = stdscr.getkey()
    if key == 'y':
        main(stdscr)
    else:
        type(stdscr,text="Thank you for playing!\nPress any key to exit...")

def main(stdscr):
    curses.init_pair(NEUTRAL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(CORRECT, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(WRONG, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)
    wpm_test(stdscr)

wrapper(main)