import pickle
import time
from threading import Thread
from threading import Lock

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.util import numpy_support
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkImageData

import multiprocessing

from vtkmodules.vtkCommonCore import VTK_INT
from vtkmodules.util.misc import calldata_type

import sys
import os
import numpy as np
import vtk
from vtkmodules.vtkFiltersCore import vtkCutter, vtkStripper

sys.path.append("./modules")
import modules.accessi_local as Access
import modules.ImageData as ImageData
from modules.shared_methods import convert_metadata_to_image

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
import zmq
import math

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkFiltersSources import vtkCylinderSource, vtkCubeSource, vtkSphereSource, vtkPlaneSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget, vtkSplineWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer, vtkTexture
)

from vtk import vtkSTLReader

lineColor = vtkNamedColors().GetColor3d('peacock')


class ScanSuiteWindow:
    def __init__(self, SUBSCRIBE_PORT=None, accessi_ip_address=None, accessi_version=None):
        # this is awful but no comment, it works.
        self.SUBSCRIBE_PORT = SUBSCRIBE_PORT
        self.subscriber_socket = None
        self.Access = Access
        self.registered = False
        self.Access.config.ip_address = accessi_ip_address
        self.Access.config.version = accessi_version
        self.renderer = None
        self.window_interactor = None
        self.mri_slice_fov = None
        self.mri_image_plane_actor = None
        self.mri_image_plane_source = None
        self.mri_slice_object = None
        self.mri_slice_actor = None
        self.mri_slice_axes_actor = None
        self.stl_reader = None
        self.stl_actor = None
        self.render_window = None
        self.camera_manipulator_widget = None
        self.spline_widget = None
        self.drawn_artifacts = []
        self.tracking_data = None

    @staticmethod
    def start(SUBSCRIBE_PORT=None, accessi_ip_address=None, accessi_version=None):
        scan_suite = ScanSuiteWindow(SUBSCRIBE_PORT, accessi_ip_address, accessi_version)
        scan_suite.register()
        scan_suite.initialize_vtk()
        scan_suite.add_mri_slice_actor()
        # scan_suite.add_spline_widget()
        scan_suite.add_phantom_actor()
        scan_suite.add_axes_actor()
        scan_suite.add_image_plane_actor()
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
        self.window_interactor.CreateRepeatingTimer(300)
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

        # Extract edges from the cube source
        edges = vtk.vtkExtractEdges()
        edges.SetInputConnection(self.mri_slice_object.GetOutputPort())

        # Mapper for the edges
        mapper_edges = vtk.vtkPolyDataMapper()
        mapper_edges.SetInputConnection(edges.GetOutputPort())

        # Actor for the edges
        self.mri_slice_actor = vtk.vtkActor()
        self.mri_slice_actor.SetMapper(mapper_edges)
        self.mri_slice_actor.GetProperty().SetColor((0, 0, 0))
        self.mri_slice_actor.GetProperty().SetLineWidth(4)
        self.mri_slice_actor.GetProperty().BackfaceCullingOn()
        self.mri_slice_axes_actor = self.add_axes_actor(50, markers=False)
        self.renderer.AddActor(self.mri_slice_actor)

    def add_sphere_actor(self):
        sphere_object = vtkSphereSource()
        sphere_object.SetRadius(5)
        mapper_sphere_object = vtkPolyDataMapper()
        mapper_sphere_object.SetInputConnection(sphere_object.GetOutputPort())
        sphere_actor = vtkActor()
        sphere_actor.SetMapper(mapper_sphere_object)
        sphere_actor.GetProperty().SetColor(1, 1, 0)
        self.renderer.AddActor(sphere_actor)
        return sphere_actor

    def add_image_plane_actor(self):
        self.mri_image_plane_source = vtkPlaneSource()
        planeMapper = vtkPolyDataMapper()
        planeMapper.SetInputConnection(self.mri_image_plane_source.GetOutputPort())

        self.mri_image_plane_actor = vtkActor()
        self.mri_image_plane_actor.SetMapper(planeMapper)
        self.mri_image_plane_actor.GetProperty().SetOpacity(0.8)
        self.mri_image_plane_actor.VisibilityOff()

        self.renderer.AddActor(self.mri_image_plane_actor)
        return self.mri_image_plane_actor

    def add_phantom_actor(self):
        self.stl_reader = vtkSTLReader()
        latest_file = max(
            (os.path.join(root, file) for root, _, files in os.walk("STL_MODEL") for file in files),
            key=os.path.getmtime)
        print(f"Using STL: {latest_file}")
        self.stl_reader.SetFileName(latest_file)
        self.stl_reader.Update()
        stl_mapper = vtkPolyDataMapper()
        stl_mapper.SetInputConnection(self.stl_reader.GetOutputPort())
        self.stl_actor = vtkActor()
        self.stl_actor.SetMapper(stl_mapper)
        self.renderer.AddActor(self.stl_actor)
        self.stl_actor.GetProperty().SetOpacity(0.7)
        # self.stl_actor.GetProperty().SetEdgeVisibility(1)
        # self.stl_actor.GetProperty().SetEdgeColor(1, 1, 1)
        self.window_interactor.Render()

    def add_axes_actor(self, length=400, markers=True):
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(length, length, length)
        widget = vtk.vtkOrientationMarkerWidget()
        if not markers:
            axes.SetAxisLabels(False)
        widget.SetOrientationMarker(axes)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        rgba = [0] * 4
        vtk.vtkNamedColors().GetColor('Carrot', rgba)
        widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
        self.renderer.AddActor(axes)
        return axes

    def add_spline_widget(self):
        self.spline_widget = vtkSplineWidget()
        self.spline_widget.PlaceWidget(-2.5, 2.5, 3.5, 3.5, 0, 0, )
        self.spline_widget.SetProp3D(self.mri_slice_actor)
        self.spline_widget.AddObserver(vtkCommand.EndInteractionEvent, SplineCallback(self.spline_widget))

    @calldata_type(VTK_INT)
    def set_mri_slice_transform_callback(self, caller, timer_event, some_argument):
        if self.registered:
            position = self.Access.ParameterStandard.get_slice_position_dcs().value
            thickness = self.Access.ParameterStandard.get_slice_thickness().value
            field_of_view = self.Access.ParameterStandard.get_field_of_view_read().value
            orientation = self.Access.ParameterStandard.get_slice_orientation_degrees_dcs()

            self.mri_slice_fov = field_of_view
            self.mri_slice_actor.SetPosition(position.x, -position.y, -position.z)
            self.mri_slice_actor.SetOrientation(orientation.phase-90, orientation.read-90, orientation.normal)
            self.mri_slice_object.SetXLength(field_of_view)
            self.mri_slice_object.SetYLength(field_of_view)
            self.mri_slice_object.SetZLength(int(thickness))

            transform = vtk.vtkTransform()
            transform.SetMatrix(self.mri_slice_actor.GetMatrix())
            self.mri_slice_axes_actor.SetUserTransform(transform)
            # These points suck (╯°□°)╯︵ ┻━┻
            self.mri_image_plane_source.SetOrigin((field_of_view//2), -(field_of_view//2), 0)
            self.mri_image_plane_source.SetPoint1(-(field_of_view//2), -(field_of_view//2), 0)
            self.mri_image_plane_source.SetPoint2((field_of_view//2), (field_of_view//2), 0)
            self.mri_image_plane_actor.SetUserTransform(transform)


            self.draw_artifact_spheres()

            self.render_window.Render()

    def start_vtk(self):
        if self.SUBSCRIBE_PORT is not None and self.SUBSCRIBE_PORT != "None":
            context = zmq.Context()
            self.subscriber_socket = context.socket(zmq.SUB)
            self.subscriber_socket.setsockopt(zmq.CONFLATE, 1)
            self.subscriber_socket.connect("tcp://127.0.0.1:" + str(self.SUBSCRIBE_PORT))
            self.subscriber_socket.subscribe("")

        self.window_interactor.Render()

        self.render_window.AddRenderer(self.renderer)
        self.window_interactor.SetRenderWindow(self.render_window)
        self.camera_manipulator_widget.SetParentRenderer(self.renderer)
        self.camera_manipulator_widget.On()
        # self.spline_widget.SetInteractor(self.window_interactor)
        # self.spline_widget.On()
        self.render_window.Render()
        self.render_window.SetWindowName("3D Suite")
        self.window_interactor.AddObserver("ExitEvent", self.close_event)

        data_thread = Thread(target=self.get_coordinate_data_thread, daemon=True)
        data_thread.start()

        self.window_interactor.Start()

    def close_event(self, obj, event):
        # Cleanup operations when window is closed
        if self.registered:
            self.Access.HostControl.release_host_control()
            self.Access.Authorization.deregister()

    def draw_artifact_spheres(self):
        for actor in self.drawn_artifacts:
            self.renderer.RemoveActor(actor)
        self.drawn_artifacts.clear()

        transform = vtk.vtkTransform()
        transform.SetMatrix(self.mri_slice_actor.GetMatrix())

        if self.tracking_data is not None:
            if self.tracking_data.image is not None:
                self.mri_image_plane_actor.VisibilityOn()
                mri_image_texture = self.tracking_data.image.astype(np.uint8)
                texture = vtkImageData()
                texture.SetDimensions(mri_image_texture.shape[0], mri_image_texture.shape[1], 1)
                texture.AllocateScalars(numpy_support.get_vtk_array_type(mri_image_texture.dtype), 3)
                texture_ptr = numpy_support.numpy_to_vtk(mri_image_texture.ravel())
                texture.GetPointData().SetScalars(texture_ptr)
                mri_image_texture = vtkTexture()
                mri_image_texture.SetInputData(texture)
                mri_image_texture.InterpolateOn()
                self.mri_image_plane_actor.SetTexture(mri_image_texture)
            else:
                self.mri_image_plane_actor.VisibilityOff()
            for detected_artifact in self.tracking_data.artifact_coordinates:
                # The coordinates are in mm, measured from top-left of the slice (image reference, but in mm).
                # The Z coordinate is kept in the middle of the slice.
                sphere_actor = self.add_sphere_actor()
                sphere_actor.SetPosition(self.mri_slice_fov//2 - detected_artifact[0],
                                         -self.mri_slice_fov//2 + detected_artifact[1],
                                         0)
                sphere_actor.SetUserTransform(transform)

                self.renderer.AddActor(sphere_actor)
                self.drawn_artifacts.append(sphere_actor)

    def get_coordinate_data_thread(self):
        while True:
            time.sleep(0.3)
            try:
                if self.SUBSCRIBE_PORT is not None:
                    data = self.subscriber_socket.recv()
                    tracking_data: ImageData = pickle.loads(data)
                    tracking_data.image, metadata = convert_metadata_to_image(tracking_data.metadata)
                    self.tracking_data = tracking_data

            except Exception as error:
                print(f"Error in get_coordinate thread: {error}")


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
