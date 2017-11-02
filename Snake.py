import curses
import time
import threading

RIGHT = [1, 0]
LEFT = [-1, 0]
UP = [0, -1]
DOWN = [0, 1]
STOP = [0, 0]

actions = {
    259: UP,
    258: DOWN,
    260: LEFT,
    261: RIGHT,
    27: STOP
}


class Snake:
    def __init__(self, screen, length=10):
        self.length = length
        self.direction = RIGHT
        self.lock = threading.Lock()
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()
        self.body = [[self.width // 2, self.height // 2]]

    def __enter__(self):
        self.screen.clear()
        curses.curs_set(False)
        self.screen.nodelay(True)

    def __exit__(self, exc_type, exc_value, traceback):
        self.screen.clear()
        curses.curs_set(True)
        self.screen.nodelay(False)

    def show_title(self, title):
        self.screen.addstr(0, 0, title)
        self.screen.refresh()

    def set_direction(self, direction):
        if self is None:
            return
        with self.lock:
            if direction is None:
                return
            self.direction = direction

    def move(self):
        head = self.body[-1]
        head = self.add(head, self.direction)
        self.body.append(head)
        self.screen.addstr(head[1], head[0], "O")
        if len(self.body) > self.length:
            tail = self.body.pop(0)
            self.screen.addstr(tail[1], tail[0], " ")

    def add(self, head, direction):
        new_head = [head[0] + direction[0], head[1] + direction[1]]
        if new_head[0] < 0:
            new_head[0] = self.width - 1
        if new_head[1] < 1:
            new_head[1] = self.height - 1
        if new_head[0] >= self.width:
            new_head[0] = 0
        if new_head[1] >= self.height:
            new_head[1] = 1
        return new_head

    def key_loop(self):
        time.sleep(1)
        self.screen.clear()
        curses.curs_set(False)
        self.screen.nodelay(1)

        while True:
            if self.direction == STOP:
                break
            self.move()
            key = self.screen.getch()
            next_direction = actions.get(key)
            self.set_direction(next_direction)
            time.sleep(0.07)
