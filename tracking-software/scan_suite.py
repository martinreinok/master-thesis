# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

import multiprocessing

from vtkmodules.vtkCommonCore import VTK_INT
from vtkmodules.util.misc import calldata_type

import sys
import numpy as np
import vtk

sys.path.append("./modules")
import modules.accessi_local as Access
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
import zmq

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkFiltersSources import vtkCylinderSource, vtkCubeSource, vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget, vtkSplineWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

from vtk import vtkSTLReader


class ScanSuiteWindow:
    def __init__(self, SUBSCRIBE_PORT=None, accessi_ip_address=None, accessi_version=None):
        self.SUBSCRIBE_PORT = SUBSCRIBE_PORT
        self.Access = Access
        self.registered = False
        self.Access.config.ip_address = accessi_ip_address
        self.Access.config.version = accessi_version
        self.renderer = None
        self.window_interactor = None
        self.mri_slice_object = None
        self.mri_slice_actor = None
        self.stl_reader = None
        self.stl_actor = None
        self.render_window = None
        self.camera_manipulator_widget = None
        self.spline_widget = None

    @staticmethod
    def start(SUBSCRIBE_PORT=None, accessi_ip_address=None, accessi_version=None):
        scan_suite = ScanSuiteWindow(SUBSCRIBE_PORT, accessi_ip_address, accessi_version)
        scan_suite.register()
        scan_suite.initialize_vtk()
        scan_suite.add_mri_slice_actor()
        scan_suite.add_spline_widget()
        scan_suite.add_phantom_actor()
        scan_suite.add_axes_actor()
        scan_suite.start_vtk()

    def register(self):
        if self.Access.config.ip_address is not None:
            try:
                self.registered = self.Access.Authorization.register(name="UTwente", start_date="20231102",
                                                                     warn_date="20251002",
                                                                     expire_date="20251102", system_id="152379",
                                                                     hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                                                                     informal_name="ScanSuite")
            except:
                pass

    def initialize_vtk(self, window_size=(512, 512)):
        colors = vtkNamedColors()
        colors.SetColor('ParaViewBkg', [82, 87, 110, 255])
        self.camera_manipulator_widget = vtkCameraOrientationWidget()

        self.render_window = vtkRenderWindow()
        self.render_window.SetSize(window_size[0], window_size[1])
        self.window_interactor = vtkRenderWindowInteractor()
        self.window_interactor.SetRenderWindow(self.render_window)

        self.window_interactor.Initialize()
        self.window_interactor.CreateRepeatingTimer(1000)
        self.window_interactor.AddObserver("TimerEvent", self.set_mri_slice_transform_callback)
        style = vtkInteractorStyleTrackballCamera()
        self.window_interactor.SetInteractorStyle(style)

        self.renderer = vtkRenderer()
        self.renderer.SetBackground(colors.GetColor3d('ParaViewBkg'))

    def add_mri_slice_actor(self):
        self.mri_slice_object = vtkCubeSource()
        self.mri_slice_object.SetCenter(0, 0, 0)
        self.mri_slice_object.SetXLength(0)
        self.mri_slice_object.SetYLength(0)
        self.mri_slice_object.SetZLength(0)
        mapper_mri_slice = vtkPolyDataMapper()
        mapper_mri_slice.SetInputConnection(self.mri_slice_object.GetOutputPort())
        self.mri_slice_actor = vtkActor()
        self.mri_slice_actor.SetMapper(mapper_mri_slice)
        self.mri_slice_actor.GetProperty().SetOpacity(0.5)
        self.renderer.AddActor(self.mri_slice_actor)

    def add_phantom_actor(self):
        self.stl_reader = vtkSTLReader()
        self.stl_reader.SetFileName("STL_MODEL/phantom.stl")
        self.stl_reader.Update()
        stl_mapper = vtkPolyDataMapper()
        stl_mapper.SetInputConnection(self.stl_reader.GetOutputPort())
        self.stl_actor = vtkActor()
        self.stl_actor.SetMapper(stl_mapper)
        self.renderer.AddActor(self.stl_actor)
        self.stl_actor.GetProperty().SetOpacity(1)
        # self.stl_actor.GetProperty().SetEdgeVisibility(1)
        # self.stl_actor.GetProperty().SetEdgeColor(1, 1, 1)
        self.window_interactor.Render()

    def add_axes_actor(self):
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(400, 400, 400)
        widget = vtk.vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(axes)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        rgba = [0] * 4
        vtk.vtkNamedColors().GetColor('Carrot', rgba)
        widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
        self.renderer.AddActor(axes)

    def add_spline_widget(self):
        self.spline_widget = vtkSplineWidget()
        self.spline_widget.PlaceWidget(-2.5, 2.5, 3.5, 3.5, 0, 0, )
        self.spline_widget.SetProp3D(self.mri_slice_actor)
        self.spline_widget.AddObserver(vtkCommand.EndInteractionEvent, SplineCallback(self.spline_widget))

    def convert_mri_orientation_to_vtk(self, normal, phase, read):
        """
        Convert MRI slice orientation data to VTK rotation angles.
        """
        x_deg = np.degrees(np.arctan2(read.z, read.x))  # Rotation around x-axis
        y_deg = np.degrees(
            np.arctan2(-phase.y, np.sqrt(phase.x ** 2 + phase.z ** 2)))  # Rotation around y-axis
        z_deg = np.degrees(np.arctan2(normal.y, normal.x))  # Rotation around z-axis
        x_deg %= 360
        y_deg %= 360
        z_deg %= 360
        return x_deg, y_deg, z_deg

    @calldata_type(VTK_INT)
    def set_mri_slice_transform_callback(self, caller, timer_event, some_argument):
        if self.registered:
            position = self.Access.ParameterStandard.get_slice_position_dcs().value
            orientation = self.Access.ParameterStandard.get_slice_orientation_dcs()
            thickness = self.Access.ParameterStandard.get_slice_thickness().value
            field_of_view = self.Access.ParameterStandard.get_field_of_view_read().value
            orientation_vtk = self.convert_mri_orientation_to_vtk(orientation.normal, orientation.phase,
                                                                  orientation.read)

            self.mri_slice_actor.SetPosition(position.x, position.y, position.z)
            self.mri_slice_actor.SetOrientation(orientation_vtk[0], orientation_vtk[1], orientation_vtk[2])
            self.mri_slice_object.SetXLength(field_of_view)
            self.mri_slice_object.SetYLength(field_of_view)
            self.mri_slice_object.SetZLength(int(thickness))
            self.mri_slice_actor.GetProperty().SetColor((1, 0, 0))
            self.render_window.Render()

    def start_vtk(self):
        self.window_interactor.Render()

        self.render_window.AddRenderer(self.renderer)
        self.window_interactor.SetRenderWindow(self.render_window)
        self.camera_manipulator_widget.SetParentRenderer(self.renderer)
        self.camera_manipulator_widget.On()
        self.spline_widget.SetInteractor(self.window_interactor)
        self.spline_widget.On()
        self.render_window.Render()
        self.render_window.SetWindowName("3D Suite")
        self.window_interactor.Start()


class SplineCallback:
    def __init__(self, spline_widget):
        self.spline = spline_widget

    def __call__(self, caller, ev):
        spline_widget = caller
        length = spline_widget.GetSummedLength()
        print(f'Length: {length}')


if __name__ == "__main__":
    ScanSuite = ScanSuiteWindow()
    ScanSuite.start()
