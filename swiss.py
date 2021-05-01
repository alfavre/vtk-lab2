#!/usr/bin/env python

# makes swiss
# no main, run with python3 swiss.py from terminal
# python 3.8 was used for this assignement
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
maxZ = 4783  # hard coded, but it's the max in file
minZ = 134  # hard coded, but it's the min in file
genf = 370  # that is what the teacher said, genf is at 370
climate_crisis = False

# ------------------------look up table

# ColorConst
colorConst = {
    'BLUE': (0.0, 0.5, 0.75),
    'GREEN': (0.0, 0.5, 0.0),
    'BEIGE': (0.9, 0.8, 0.7),
    'GRAY': (0.8, 0.8, 0.8),
    'WHITE': (1.0, 1.0, 1.0)
}

# LookupTable Settings
color_min = 0
color_max = 4783
color_water = color_min
nb_colors = color_max - color_min

# our color lookuptable is a vtkDiscretizableColorTransferFunction.
# it automatically makes the gradient between our fixed colors
c_lut = vtk.vtkDiscretizableColorTransferFunction()
c_lut.DiscretizeOn()
c_lut.SetNumberOfValues(nb_colors)
c_lut.AddRGBPoint(color_min, *colorConst['BLUE'])  # special case
c_lut.AddRGBPoint(color_min + 1, *colorConst['GREEN'])
c_lut.AddRGBPoint(1000, *colorConst['BEIGE'])
c_lut.AddRGBPoint(3000, *colorConst['GRAY'])
c_lut.AddRGBPoint(color_max, *colorConst['WHITE'])
c_lut.Build()

# --------------------------------------------

points = vtk.vtkPoints()
cells = vtk.vtkCellArray()

points_ids = [[0 for x in range(width)] for y in range(height)]
points_ints = [[0 for x in range(width)] for y in range(height)]

# Generate the colors for each point based on the color map
colors = vtk.vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetName('Colors')

print('get ints from file')  # we do this here and not below, because we need to know next altitude for lake
for i in range(width):
    line = f.readline().split()
    for j in range(height):
        points_ints[i][j] = int(line[j])

print('get points and color for each int')
for i in range(width):
    for j in range(height):

        # do points
        points_ids[i][j] = points.InsertNextPoint(i * factor, j * factor,
                                                  points_ints[i][j])  # earth curvature ignored for now, flat earth mode

        # do scalar color
        if (i > 0 and j > 0 and i < (width - 1) and (j < (height - 1)) and (
                points_ints[i][j] == points_ints[i - 1][j] == points_ints[i + 1][j] == points_ints[i][j - 1] ==
                points_ints[i][j + 1])):
            # this is a lake
            dcolor = 3 * [0.0]
            c_lut.GetColor(color_water, dcolor)  # we use the c_lut like this
            color = 3 * [0.0]
            for k in range(0, 3):
                color[k] = int(255.0 * dcolor[k])
            colors.InsertNextTypedTuple(color)

        else:
            if climate_crisis and points_ints[i][j] < genf:
                # this drowned
                dcolor = 3 * [0.0]
                c_lut.GetColor(color_water, dcolor)  # we use the c_lut like this
                color = 3 * [0.0]
                for k in range(0, 3):
                    color[k] = int(255.0 * dcolor[k])
                colors.InsertNextTypedTuple(color)

            else:
                dcolor = 3 * [0.0]
                c_lut.GetColor(points_ints[i][j], dcolor)
                color = 3 * [0.0]
                for k in range(0, 3):
                    color[k] = int(255.0 * dcolor[k])
                colors.InsertNextTypedTuple(color)

print('get cells')
# we could put the double for in the double for just up from here
for i in range(width - 1):
    for j in range(height - 1):
        cells.InsertNextCell(4)
        cells.InsertCellPoint(points_ids[i][j])
        cells.InsertCellPoint(points_ids[i + 1][j])
        cells.InsertCellPoint(points_ids[i + 1][j + 1])
        cells.InsertCellPoint(points_ids[i][j + 1])

print('create polydata')
# our polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetPolys(cells)
polydata.GetPointData().SetScalars(colors)  # apparently you can bind a lut instead of doing this

# ------------------------------------------------ mapper + actor

print('create mapper and actor')

# Create a mapper
polydataMapper = vtk.vtkPolyDataMapper()
polydataMapper.SetInputData(polydata)
# create actor
polydataActor = vtk.vtkActor()
polydataActor.SetMapper(polydataMapper)

# ---------------------------------------------- put things in scene

print('start rendering')

ren1 = vtk.vtkRenderer()
ren1.AddActor(polydataActor)
ren1.SetBackground(0.8, 0.5, 0.5)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(800, 800)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
