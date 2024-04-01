#!/usr/bin/env python

import time

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

from vtkmodules.vtkCommonCore import VTK_INT
from vtkmodules.util.misc import calldata_type


class vtkTimerCallback():
    @calldata_type(VTK_INT)
    def __init__(self, steps, name):
        self.steps = steps
        self.name = name
        self.timerId = None
        self.t0 = time.time()

    def execute(self, obj, event):
        self.steps -= 1
        print(event, ' ', self.name, ' Step:', self.steps, '  t = %.3f' % (time.time() - self.t0))


if __name__ == '__main__':
    sphereSource = vtkSphereSource()
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sphereSource.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)

    # Setup a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)

    renderWindow.Render()
    renderer.GetActiveCamera().Zoom(0.8)
    renderWindow.Render()

    # Initialize must be called prior to creating timer events.
    renderWindowInteractor.Initialize()

    # Sign up to receive TimerEvent
    cb1 = vtkTimerCallback(3, 'Timer1')
    renderWindowInteractor.AddObserver('TimerEvent', cb1.execute)
    cb1.timerId = renderWindowInteractor.CreateRepeatingTimer(1000)

    # start the interaction and timer
    renderWindow.Render()
    renderWindowInteractor.Start()
