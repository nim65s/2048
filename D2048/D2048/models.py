from django.core.urlresolvers import reverse
from django.db.models import Model, IntegerField, ForeignKey, DateTimeField
from django.core.cache import caches

from numpy import array, int64

from .abstract2048 import Abstract2048

UP, LEFT, DOWN, RIGHT = [i for i in range(1, 5)]
CACHE = caches['default']


class Grid(Model):
    H = IntegerField('hauteur', default=4)
    W = IntegerField('largeur', default=4)
    score = IntegerField(default=0)
    goal = IntegerField(default=2048)
    creation = DateTimeField(auto_now_add=True)
    modification = DateTimeField(auto_now=True)
    #end = BooleanField(default=false)  TODO

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def get_grid(self):
        obj = CACHE.get(self.pk)
        if obj:
            return obj
        obj = Abstract2048(self.H, self.W, self.goal, self.score)
        obj.m = array([c.value for c in self.cell_set.all()], dtype=int64).reshape((self.H, self.W))
        return obj

    def save_grid(self, grid=None, pop=False, db=False):
        if grid is None:
            for i in range(self.H):
                for j in range(self.W):
                    Cell(grid=self, cell=i * self.W + j, value=0).save()
            grid = self.get_grid()
        self.score = grid.score
        if pop:
            grid.pop()
        CACHE.set(self.pk, grid, 300)
        if db:
            for i in range(self.H):
                for j in range(self.W):
                    cell = Cell.objects.get(grid=self, cell=i * self.W + j)
                    cell.value = grid.m[i, j]
                    cell.save()

    def move(self, direction):
        grid = self.get_grid()
        if direction == UP:
            move_results = grid.up()
        elif direction == LEFT:
            move_results = grid.left()
        elif direction == DOWN:
            move_results = grid.down()
        else:
            move_results = grid.right()
        if move_results:
            self.save_grid(grid)
        return move_results

    def range_H(self):
        return range(self.H)

    def rang_W(self):
        return range(self.W)


class Cell(Model):
    grid = ForeignKey(Grid)
    cell = IntegerField()
    value = IntegerField()

    class Meta:
        unique_together = ('grid', 'cell')
        ordering = ['grid', 'cell']
