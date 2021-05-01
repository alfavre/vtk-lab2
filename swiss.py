#!/usr/bin/env python

#
# This example introduces the concepts of user interaction with VTK.
# First, a different interaction style (than the default) is defined.
# Second, the interaction is started.
#
#

import vtk
import math

# read file
f = open("altitudes.txt", "r")
dimensions = f.readline()  # first line should be dimensions: 3001 x 3001

# a list that contains the  2 dimensions of file
dimlist = dimensions.split()

swissFraction = 1

width = math.floor(int(dimlist[0]) / swissFraction)
height = math.floor(int(dimlist[1]) / swissFraction)

factor = 50
maxZ = 4783
minZ = 134


points = vtk.vtkPoints()
cells = vtk.vtkCellArray()

points_ids = [[0 for x in range(width)] for y in range(height)]

# Create the color map
colorLookupTable = vtk.vtkLookupTable()
colorLookupTable.SetTableRange(134, 4783)
colorLookupTable.Build()

# Generate the colors for each point based on the color map
colors = vtk.vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetName('Colors')

print('get points')
for i in range( width ):
    line=f.readline().split()
    for j in range( height ):
        currentZ = int(line[j])
        points_ids[i][j] = points.InsertNextPoint(i*factor,j*factor,currentZ) # earth curvature ignored for now, flat earth mode
        dcolor = 3*[0.0]
        colorLookupTable.GetColor(currentZ, dcolor)
        color=3*[0.0]
        for j in range(0,3):
          color[j] = int(255.0 * dcolor[j])
        colors.InsertNextTypedTuple(color)




print('get cells')
# we could put the double for in the double for just up from here
for i in range(width-1):
    for j in range(height-1):
        cells.InsertNextCell(4)
        cells.InsertCellPoint(points_ids[i][j])
        cells.InsertCellPoint(points_ids[i+1][j])
        cells.InsertCellPoint(points_ids[i+1][j+1])
        cells.InsertCellPoint(points_ids[i][j+1])


print('create polydata')
# our polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetPolys(cells)
polydata.GetPointData().SetScalars(colors)


print('points handling (might be deleted soon)')
#------------------------------- points

# this is just to see points if needed, will be deleted
glyphFilter = vtk.vtkVertexGlyphFilter()
glyphFilter.SetInputData(polydata)
glyphFilter.Update()
pointsMapper = vtk.vtkPolyDataMapper()
pointsMapper.SetInputConnection(glyphFilter.GetOutputPort())
pointsActor = vtk.vtkActor()
pointsActor.SetMapper(pointsMapper)
pointsActor.GetProperty().SetPointSize(3)
colors = vtk.vtkNamedColors()
pointsActor.GetProperty().SetColor(colors.GetColor3d("Red"))
# ------------------------------------------------ mapper + actor

print('create mapper and actor')

# Create a mapper and actor
polydataMapper = vtk.vtkPolyDataMapper()
polydataMapper.SetInputData(polydata)

polydataActor = vtk.vtkActor()
polydataActor.SetMapper(polydataMapper)

# ---------------------------------------------- put things in scene

print('start rendering')

#
# Create the Renderer and assign actors to it. A renderer is like a
# viewport. It is part or all of a window on the screen and it is responsible
# for drawing the actors it has.  We also set the background color here.
#
ren1 = vtk.vtkRenderer()
# ren1.AddActor(pointsActor)
ren1.AddActor(polydataActor)
ren1.SetBackground(0.8, 0.5, 0.5)

#
# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We also
# set the size to be 300 pixels by 300.
#
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(800, 800)


#
# The vtkRenderWindowInteractor class watches for events (e.g., keypress,
# mouse) in the vtkRenderWindow. These events are translated into
# event invocations that VTK understands (see VTK/Common/vtkCommand.h
# for all events that VTK processes). Then observers of these VTK
# events can process them as appropriate.
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#
# By default the vtkRenderWindowInteractor instantiates an instance
# of vtkInteractorStyle. vtkInteractorStyle translates a set of events
# it observes into operations on the camera, actors, and/or properties
# in the vtkRenderWindow associated with the vtkRenderWinodwInteractor.
# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

#
# Unlike the previous scripts where we performed some operations and then
# exited, here we leave an event loop running. The user can use the mouse
# and keyboard to perform the operations on the scene according to the
# current interaction style.
#

#
# Initialize and start the event loop. Once the render window appears, mouse
# in the window to move the camera. The Start() method executes an event
# loop which listens to user mouse and keyboard events. Note that keypress-e
# exits the event loop. (Look in vtkInteractorStyle.h for a summary of events, or
# the appropriate Doxygen documentation.)
#
iren.Initialize()
iren.Start()
