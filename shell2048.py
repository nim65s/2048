#!/usr/bin/env python

import sys
import termios
import tty

from abstract2048 import Abstract2048


class Shell2048(Abstract2048):
    def __str__(self):
        return 'Score: {score}\n{m}\n'.format(**self.__dict__)

    def run(self):
        def getchar():
            """ https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user """
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

        while not self.game_over():
            print(self)
            old = self.m.copy()

            while (old == self.m).all():
                c = getchar()
                if c == '4':
                    print(self.left())
                elif c == '8':
                    print(self.up())
                elif c == '6':
                    print(self.right())
                elif c in '25':
                    print(self.down())
                elif c == '0' and self.m.min() == 0:  # cheating
                    print(self.pop())
                elif c == 'q':
                    print('Y U QUIT ? :(')
                    return
        print('game over', self)

if __name__ == '__main__':
    g = Shell2048()
    g.pop()
    g.run()
