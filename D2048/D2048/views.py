import json

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView

from .models import Grid, Cell


class GridCreateView(CreateView):
    model = Grid
    fields = ["H", "W", "goal"]

    def form_valid(self, form):
        super().form_valid(form)
        self.object.save_grid(None, pop=True)
        return HttpResponseRedirect(self.get_success_url())


class GridDetailView(DetailView):
    model = Grid


class GridMoveView(GridDetailView):
    def get(self, request, *args, **kwargs):
        direction = int(kwargs['dir'])
        if direction not in range(1, 5):
            raise SuspiciousOperation('bad direction: %i' % direction)
        self.object = self.get_object()
        context = {'direction': direction}
        context['slides'], context['pop'], context['next'] = self.object.move(direction)
        if self.request.is_ajax():
            return HttpResponse(json.dumps(context), {'content_type': 'application/json'})
        context.update(self.get_context_data(object=self.object))
        return self.render_to_response(context)


class GridSaveView(GridDetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.save_grid(self.object.get_grid(), pop=False, db=True)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
