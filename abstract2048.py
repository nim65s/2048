#!/usr/bin/env python

from random import randrange

from numpy import int64, zeros


class Abstract2048:
    def __init__(self, height=4, width=4, goal=2048):
        self.H = height
        self.W = width
        self.m = zeros((height, width), dtype=int64)
        self.score = 0
        self.goal = goal
        self.pop()

    def pop(self):
        if self.m.min() == 0:
            while True:
                i = randrange(0, self.H)
                j = randrange(0, self.W)
                if self.m[i, j] == 0:
                    break
            self.m[i, j] = 2 if randrange(0, 10) else 4

    def left(self):
        def slide(i, j):
            if j != -1:
                self.m[i, j:-1] = self.m[i, j + 1:]
            self.m[i, -1] = 0

        for i in range(self.H):
            for j in range(self.W - 1):
                if self.m[i, - j - 2] == 0:
                    slide(i, - 2 - j)
            for j in range(self.W - 1):
                if self.m[i, j] == self.m[i, j + 1]:
                    slide(i, j)
                    self.m[i, j] *= 2
                    self.score += self.m[i, j]

    def up(self):
        def slide(i, j):
            if i != -1:
                self.m[i:-1, j] = self.m[i + 1:, j]
            self.m[-1, j] = 0

        for j in range(self.W):
            for i in range(self.H - 1):
                if self.m[- i - 2, j] == 0:
                    slide(- 2 - i, j)
            for i in range(self.H - 1):
                if self.m[i, j] == self.m[i + 1, j]:
                    slide(i, j)
                    self.m[i, j] *= 2
                    self.score += self.m[i, j]

    def right(self):
        def slide(i, j):
            if j != 0:
                self.m[i, 1:j] = self.m[i, :j - 1]
            self.m[i, 0] = 0

        for i in range(self.H):
            for j in range(1, self.W):
                if self.m[i, j] == 0:
                    slide(i, j + 1)
            for j in range(1, self.W):
                if self.m[i, -j] == self.m[i, -j - 1]:
                    slide(i, -j)
                    self.m[i, -j] *= 2
                    self.score += self.m[i, -j]

    def down(self):
        def slide(i, j):
            if i != 0:
                self.m[1:i, j] = self.m[:i - 1, j]
            self.m[0, j] = 0

        for j in range(self.W):
            for i in range(1, self.H):
                if self.m[i, j] == 0:
                    slide(i + 1, j)
            for i in range(1, self.H):
                if self.m[-i, j] == self.m[-i - 1, j]:
                    slide(-i, j)
                    self.m[-i, j] *= 2
                    self.score += self.m[-i, j]
