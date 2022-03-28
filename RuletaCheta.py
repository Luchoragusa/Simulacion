# coding: utf-8

"""
Casino - Roulette  https://www.youtube.com/watch?v=1Y1JAR7UCm4
"""

from turtle import *
import random
from datetime import datetime, timedelta
import math

STARTUP = 1
RUNNING = 2
DONE = 3

COLOR_BLACK = "black"
COLOR_BROWN = "brown"
COLOR_GREEN = "green"
COLOR_BLUE = "blue"
COLOR_RED = "red"
COLOR_YELLOW = "yellow"
COLOR_WHITE = "white"

FONT_SCORE = ("Arial", 10, "bold")
FONT_SCORE_TITLE = ("Arial", 16, "bold")
FONT_BUTTON = ("Arial", 20, "normal")
FONT_CHIP = ("Arial", 10, "normal")
FONT_RO_SLOT = ("Arial", 8, "normal")
FONT_BET_TEXT = ("Arial", 16, "bold")

CHIPS = [1, 2, 10, 50]
RONUMS = [34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25, 17]


def in_range(x, y, x1, y1, x2, y2):
    return max(x1, x2) >= x >= min(x1, x2) and max(y1, y2) >= y >= min(y1, y2)


def write_txt(tt, x, y, text, font, color=COLOR_BLACK):
    tt.pencolor(color)
    tt.up()
    tt.goto(x, y)
    tt.down()
    tt.write(text, font=font)


def draw_chip(tt, x, y, heading, r, fgcol, bgcol, num):
    tt.up()
    tt.goto(x, y)
    tt.seth(heading)
    tt.down()
    tt.color(fgcol, bgcol)
    tt.begin_fill()
    tt.circle(r, 360)
    tt.end_fill()
    n = 0
    k = num
    while k // 10 > 0:
        n = n + 1
        k = k / 10
    dx = -3.5 * n
    dy = 8
    write_txt(tt, x + dx, y + dy, str(num), font=FONT_CHIP)


def draw_rect(tt, x, y, w, h, fgcol, bgcol, filled=False):
    tt.color(fgcol, bgcol)
    tt.up()
    tt.goto(x, y)
    tt.down()
    if filled:
        tt.begin_fill()
    tt.seth(0)
    tt.forward(w)
    tt.left(90)
    tt.forward(h)
    tt.left(90)
    tt.forward(w)
    tt.left(90)
    tt.forward(h)
    if filled:
        tt.end_fill()


class Ball:
    def __init__(self, ro_idx=0):
        self.ro_idx = ro_idx
        self.t = Turtle()
        self.t.shape("circle")
        self.t.color(COLOR_BLACK, COLOR_BROWN)
        self.X = -300
        self.Y = 200
        self.R = 170
        self.ball_pos = []
        for i in range(37):
            a = i * 360 / 37 + 5
            x = self.R * math.cos((360-a) * math.pi / 180) + self.X
            y = self.R * math.sin((360-a) * math.pi / 180) + self.Y
            self.ball_pos.append((x, y))

    def get_last_ro_index(self):
        return self.ro_idx

    def update(self, ro_idx):
        self.ro_idx = ro_idx
        tracer(True)
        self.t.up()
        self.t.goto(self.ball_pos[ro_idx])
        self.t.down()
        tracer(False)


class Score:
    def __init__(self):
        self.t = Turtle()
        self.X = 310
        self.Y = 360
        self.W = 30

    def update(self, total_score):
        self.t.clear()
        # get 6-digit number from score
        scores = [0] * 6
        n = total_score
        for i in range(6):
            scores[5 - i] = int(n % 10)
            n = n // 10
        # write title string
        write_txt(self.t, self.X, self.Y + 10, "SCORE:", font=FONT_SCORE_TITLE)
        for i in range(6):
            self.t.up()
            self.t.goto(self.X + 30 * i, self.Y)
            self.t.down()
            # draw box
            for _ in range(4):
                self.t.forward(self.W)
                self.t.right(90)
            # write number in box
            write_txt(self.t, self.X + self.W * i + 10, self.Y - 25, str(scores[i]), font=FONT_SCORE)
        self.t.ht()


class Button:
    def __init__(self):
        self.t = Turtle()
        self.X = -495
        self.Y = -195
        self.W = 155
        self.H = 40

    def clickable(self, x, y):
        return in_range(x, y, self.X, self.Y, self.X + self.W, self.Y + self.H)

    def update(self, state):
        # draw button
        #
        # background is green means button is clickable, otherwise it unable to click.
        # background is green when state are STARTUP/DONE
        #
        txt = ""
        filled = True
        if state == STARTUP:
            txt = "Start"
        elif state == RUNNING:
            filled = False
            txt = "Running "
        elif state == DONE:
            txt = "New Round"
        self.t.reset()
        dx = (self.W - len(txt)*15.5) / 2
        draw_rect(self.t, self.X, self.Y, self.W, self.H, COLOR_GREEN, COLOR_GREEN, filled)
        write_txt(self.t, self.X + dx, self.Y, txt, font=FONT_BUTTON)
        self.t.ht()


class Chip:
    def __init__(self, chip_idx=0):
        self.t = Turtle()
        self.X = 310
        self.Y = -195
        self.R = 20
        self.chip_idx = chip_idx

    def clickable(self, x, y):
        for i in range(4):
            if in_range(x, y, self.X + i * 50 - self.R, self.Y, self.X + i * 50 + self.R, self.Y + 2 * self.R):
                return True
        return False

    def get_chip_value(self):
        return CHIPS[self.chip_idx]

    def choose(self, x, y):
        chip_idx = -1
        for i in range(4):
            if in_range(x, y, self.X + i * 50 - self.R, self.Y, self.X + i * 50 + self.R, self.Y + 2 * self.R):
                chip_idx = i
                break
        if self.chip_idx != chip_idx:
            self.chip_idx = chip_idx
            self.update(STARTUP)

    def update(self, state):
        # draw chip
        #
        # background color is green means chip is clickable.
        # pencolor is red means chip has been chosen.
        #
        self.t.clear()
        pencols = [COLOR_BLACK] * 4
        bgcols = [COLOR_GREEN] * 4
        for i in range(4):
            pencol = COLOR_RED if i == self.chip_idx else pencols[i]
            bgcol = COLOR_YELLOW if i == self.chip_idx else bgcols[i]
            if state == RUNNING or state == DONE:
                bgcol = COLOR_WHITE
            draw_chip(self.t, self.X + i * 50, self.Y, 0, self.R, pencol, bgcol, CHIPS[i])
        self.t.ht()


class Table:
    def __init__(self, tot_chips):
        self.t = Turtle()
        self.tot_score = tot_chips
        self.bet_pos = [[0, 0, 0, 0]] * 44
        self.bets = [0] * 44
        self.X_NUM = -110
        self.Y_NUM = 20
        self.W_NUM = 50
        self.H_NUM = 50
        self.X_1ST = -110
        self.Y_1ST = 70
        self.W_1ST = 200
        self.H_1ST = 50
        self.X_EVEN = -110
        self.Y_EVEN = -130
        self.W_EVEN = 150
        self.H_EVEN = 50
        self.R_CHIP = 20

        # POS [0]
        self.bet_pos[0] = [self.X_NUM - 50, self.Y_NUM - 50, self.W_NUM, self.H_NUM]
        # POS [1-37]
        for i in range(12):
            for j in range(3):
                self.bet_pos[i * 3 + j + 1] = [self.X_NUM + i * 50, self.Y_NUM - j * 50, self.W_NUM, self.H_NUM]
        # POS [1st,2nd,3rd]
        for i in range(3):
            self.bet_pos[37 + i] = [self.X_1ST + i * self.W_1ST, self.Y_1ST, self.W_1ST, self.H_1ST]
        # POS [Een,Red,Odd,Black]
        for i in range(4):
            self.bet_pos[40 + i] = [self.X_EVEN + i * self.W_EVEN, self.Y_EVEN, self.W_EVEN, self.H_EVEN]

    def draw_win_pos(self, idx):
        # draw red box in the position
        for i in range(44):
            if idx == i:
                draw_rect(self.t,
                          self.bet_pos[i][0] + 5,
                          self.bet_pos[i][1] + 5,
                          self.bet_pos[i][2] - 10,
                          self.bet_pos[i][3] - 10,
                          COLOR_RED, COLOR_GREEN, False)

    def clickable(self, x, y):
        for i in range(44):
            if in_range(x, y,
                        self.bet_pos[i][0],
                        self.bet_pos[i][1],
                        self.bet_pos[i][0] + self.bet_pos[i][2],
                        self.bet_pos[i][1] + self.bet_pos[i][3]):
                return True
        return False

    def place_bet(self, x, y, chip_value):
        if self.tot_score >= chip_value:
            for i in range(44):
                if in_range(x, y,
                            self.bet_pos[i][0],
                            self.bet_pos[i][1],
                            self.bet_pos[i][0] + self.bet_pos[i][2],
                            self.bet_pos[i][1] + self.bet_pos[i][3]):
                    self.bets[i] = self.bets[i] + chip_value
                    self.tot_score = self.tot_score - chip_value
                    pos = self.get_bet_pos(i)
                    draw_chip(self.t, pos[0], pos[1], 0, self.R_CHIP, COLOR_BLACK, COLOR_YELLOW, self.bets[i])
                    return i
        return -1

    def get_bet_pos(self, idx):
        x = self.bet_pos[idx][0]
        y = self.bet_pos[idx][1]
        w = self.bet_pos[idx][2]
        h = self.bet_pos[idx][3]
        return x + w / 2, y + h / 2 - self.R_CHIP

    def get_total_score(self):
        return self.tot_score

    def get_bet_amount(self):
        tot = 0
        for i in range(44):
            if self.bets[i] > 0:
                tot = tot + self.bets[i]
        return tot

    def update(self, state, ro_idx):
        ro_num = RONUMS[ro_idx]
        self.t.clear()
        # draw bounding box
        draw_rect(self.t, -500, -200, 1000, 600, COLOR_BLACK, COLOR_BLACK, False)
        # draw bet table
        bg_color = COLOR_GREEN if state == STARTUP else COLOR_WHITE
        self.draw_table(bg_color)
        if state == STARTUP:
            # clear bets
            self.bets = [0] * 44
        elif state == RUNNING:
            # draw bets
            for i in range(44):
                if self.bets[i] > 0:
                    pos = self.get_bet_pos(i)
                    draw_chip(self.t, pos[0], pos[1], 0, self.R_CHIP, COLOR_BLACK, COLOR_YELLOW, self.bets[i])
        elif state == DONE:
            # calculate profits and draw win bets
            for i in range(44):
                is_win_pos = False
                if i == ro_num and 36 >= i >= 0:
                    self.bets[i] = self.bets[i] * 35
                    is_win_pos = True
                elif i == 37 and 12 >= ro_num >= 1:
                    self.bets[i] = self.bets[i] * 3
                    is_win_pos = True
                elif i == 38 and 24 >= ro_num >= 13:
                    self.bets[i] = self.bets[i] * 3
                    is_win_pos = True
                elif i == 39 and 36 >= ro_num >= 25:
                    self.bets[i] = self.bets[i] * 3
                    is_win_pos = True
                elif (i == 40 or i == 41) and ro_num % 2 == 1:
                    self.bets[i] = self.bets[i] * 2
                    is_win_pos = True
                elif (i == 42 or i == 43) and ro_num % 2 == 0:
                    self.bets[i] = self.bets[i] * 2
                    is_win_pos = True
                else:
                    self.bets[i] = 0
                if is_win_pos:
                    self.draw_win_pos(i)
                if self.bets[i] > 0:
                    self.tot_score = self.tot_score + self.bets[i]
                    if self.tot_score > 999999:
                        self.tot_score = 999999
                    pos = self.get_bet_pos(i)
                    draw_chip(self.t, pos[0], pos[1], 0, self.R_CHIP, COLOR_BLACK, COLOR_YELLOW, self.bets[i])
        self.t.ht()
        return

    def draw_table(self, bgcol):
        for i in range(44):
            draw_rect(self.t,
                      self.bet_pos[i][0],
                      self.bet_pos[i][1],
                      self.bet_pos[i][2],
                      self.bet_pos[i][3],
                      COLOR_BLACK, bgcol, True)

            x = self.get_bet_pos(i)[0] - 10
            y = self.get_bet_pos(i)[1] + 5
            c = COLOR_BLACK
            txt = ""
            if 36 >= i >= 0:
                txt = str(i)
                dx = 10 if i < 10 else 0
                x = x + dx
                c = COLOR_BLACK if i % 2 == 0 else COLOR_RED
            elif i == 37:
                txt = "1st"
            elif i == 38:
                txt = "2nd"
            elif i == 39:
                txt = "3rd"
            elif i == 40:
                txt = "Even"
                c = COLOR_RED
            elif i == 41:
                txt = "Red"
                c = COLOR_RED
            elif i == 42:
                txt = "Odd"
            elif i == 43:
                txt = "Black"
            write_txt(self.t, x, y, txt, font=FONT_BET_TEXT, color=c)


class Roulette:
    def __init__(self):
        self.t = Turtle()

    def update(self):
        self.t.clear()
        self.draw_roulette()
        self.t.ht()

    def draw_dot(self, slot_pos, heading, r, a, col):
        self.t.up()
        self.t.goto(slot_pos)
        self.t.seth(heading)
        self.t.down()
        self.t.circle(r, a)
        self.t.dot(10, col)
        return self.t.pos(), self.t.heading()

    def draw_roulette(self):
        a = 360 / 37
        (pos1, head1) = ((-100, 200), 90)
        (pos2, head2) = ((-120, 200), 90)
        (pos3, head3) = ((-140, 200), 90)
        for i in range(37):
            old_pos2 = pos2
            # draw arc
            (pos1, head1) = self.draw_dot(pos1, head1, 200, a, COLOR_BLUE)
            (pos2, head2) = self.draw_dot(pos2, head2, 180, a, COLOR_RED)
            (pos3, head3) = self.draw_dot(pos3, head3, 160, a, COLOR_GREEN)
            # draw line
            self.t.up()
            self.t.goto(pos1)
            self.t.down()
            self.t.goto(pos3)
            # write number (0-36)
            dx = 3.5 if i < 10 else 7
            dy = 8
            x = (pos1[0] + old_pos2[0]) / 2 - dx
            y = (pos1[1] + old_pos2[1]) / 2 - dy
            self.t.up()
            self.t.goto(x, y)
            self.t.down()
            ro_num = RONUMS[36 - i]
            c = COLOR_RED if ro_num % 2 == 1 else COLOR_BLACK
            write_txt(self.t, x, y, str(ro_num), font=FONT_RO_SLOT, color=c)


class Game:
    def __init__(self):
        self.table = Table(10000)
        self.ro = Roulette()
        self.chip = Chip()
        self.score = Score()
        self.command = Button()
        self.ball = None
        self.ro_end_time = datetime.today()
        self.state = STARTUP

    def tick(self):
        if self.state == RUNNING and self.ro_end_time >= datetime.today():
            # move ball to next position
            tracer(True)
            ro_idx = self.ball.get_last_ro_index() + 1
            if ro_idx == 37:
                ro_idx = 0
            self.ball.update(ro_idx)

            if datetime.today().second == self.ro_end_time.second:
                # it is the end time, the ball stop running
                self.state = DONE
                self.update(self.ball.get_last_ro_index())
        ontimer(self.tick, 10)

    def onclick(self, x, y):
        if self.chip.clickable(x, y):
            if self.state == STARTUP:
                # selected chip
                self.chip.choose(x, y)

        if self.table.clickable(x, y):
            if self.state == STARTUP:
                # placed bets, update score
                self.table.place_bet(x, y, self.chip.get_chip_value())
                self.score.update(self.table.get_total_score())

        if self.command.clickable(x, y):
            if self.state == DONE:
                # start next round, clear table
                self.state = STARTUP
                self.update(self.ball.get_last_ro_index())

            elif self.state == STARTUP:
                if self.table.get_bet_amount() > 0:
                    # stop bet
                    self.state = RUNNING
                    self.update(self.ball.get_last_ro_index())
                    # set the end time, the ball stops rotating at the time
                    self.ro_end_time = datetime.today() + timedelta(seconds=random.randint(8, 12))

    def update(self, ro_idx, demo=False):
        tracer(demo)
        self.table.update(self.state, ro_idx)
        self.ro.update()
        self.chip.update(self.state)
        self.score.update(self.table.get_total_score())
        self.command.update(self.state)
        if not self.ball:
            self.ball = Ball()
        self.ball.update(ro_idx)

    def run(self):
        # To show drawing process, set "demo=True"
        self.update(ro_idx=28, demo=False)
        onscreenclick(self.onclick, btn=1)
        self.tick()
        # Turtle().getscreen().getcanvas().postscript(file="roulette.eps")


def main():
    game = Game()
    game.run()
    return "EVENTLOOP"


if __name__ == '__main__':
    main()
    mainloop()