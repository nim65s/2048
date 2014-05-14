#!/usr/bin/env python

from random import randrange

from numpy import int64, zeros, dstack, where


class Abstract2048:
    def __init__(self, height=4, width=4, goal=2048, score=0):
        self.H = int(height)
        self.W = int(width)
        self.m = zeros((int(height), int(width)), dtype=int64)
        self.score = int(score)
        self.goal = int(goal)

    def pop(self):
        if self.m.min() == 0:
            while True:
                i = randrange(0, self.H)
                j = randrange(0, self.W)
                if self.m[i, j] == 0:
                    break
            self.m[i, j] = 2 if randrange(0, 10) else 4
            return i, j

    def left(self):
        slides = []

        def slide(i, j):
            slides.append((i, j))
            if j != -1:
                self.m[i, j:-1] = self.m[i, j + 1:]
            self.m[i, -1] = 0

        for i in range(self.H):
            for j in range(self.W - 1):
                if self.m[i, - j - 2] == 0 and (self.m[i, - j - 2:] != 0).any():
                    slide(i, self.W - 2 - j)
            for j in range(self.W - 1):
                if self.m[i, j] == self.m[i, j + 1] != 0:
                    slide(i, j)
                    self.m[i, j] *= 2
                    self.score += self.m[i, j]
        return (slides, self.pop()) if slides else None

    def up(self):
        slides = []

        def slide(i, j):
            slides.append((i, j))
            if i != -1:
                self.m[i:-1, j] = self.m[i + 1:, j]
            self.m[-1, j] = 0

        for j in range(self.W):
            for i in range(self.H - 1):
                if self.m[- i - 2, j] == 0 and (self.m[- i - 2:, j] != 0).any():
                    slide(self.H - 2 - i, j)
            for i in range(self.H - 1):
                if self.m[i, j] == self.m[i + 1, j] != 0:
                    slide(i, j)
                    self.m[i, j] *= 2
                    self.score += self.m[i, j]
        return (slides, self.pop()) if slides else None

    def right(self):
        slides = []

        def slide(i, j):
            slides.append((i, j))
            if j != 0:
                self.m[i, 1:j] = self.m[i, :j - 1]
            self.m[i, 0] = 0

        for i in range(self.H):
            for j in range(1, self.W):
                if self.m[i, j] == 0 and (self.m[i, :j] != 0).any():
                    slide(i, j + 1)
            for j in range(1, self.W):
                if self.m[i, -j] == self.m[i, -j - 1] != 0:
                    slide(i, self.W - j)
                    self.m[i, -j] *= 2
                    self.score += self.m[i, -j]
        return (slides, self.pop()) if slides else None

    def down(self):
        slides = []

        def slide(i, j):
            slides.append((i, j))
            if i != 0:
                self.m[1:i, j] = self.m[:i - 1, j]
            self.m[0, j] = 0

        for j in range(self.W):
            for i in range(1, self.H):
                if self.m[i, j] == 0 and (self.m[:i, j] != 0).any():
                    slide(i + 1, j)
            for i in range(1, self.H):
                if self.m[-i, j] == self.m[-i - 1, j] != 0:
                    slide(self.H - i, j)
                    self.m[-i, j] *= 2
                    self.score += self.m[-i, j]
        return (slides, self.pop()) if slides else None

    def game_over(self):
        val = self.m.min()
        if val == 0:
            return False
        maxi = self.m.max()
        if maxi == self.goal:
            return True
        while val <= maxi:
            pts = dstack(where(self.m == val))[0]
            if len(pts) > 1 and any([(pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 == 1 for pt1 in pts for pt2 in pts]):
                return False
            val *= 2
        return True
