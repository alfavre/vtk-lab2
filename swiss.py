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

# x = (47.5-45)/3001
# y = (7.5-5)/3001
# the two factor are the same, executive decision to use the same factor for both
factor_longitude_latitude = 0.00083305564
factor_big_swiss = 0.01
maxZ = 4783  # hard coded, but it's the max in file
minZ = 134  # hard coded, but it's the min in file, never used
genf = 370  # that is what the teacher said, genf is at 370
climate_crisis = False

latitude_base_angle = 45
longitude_base_angle = 7.5
earth_radius = 6371009

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
color_max = maxZ
color_water = color_min
nb_colors = color_max - color_min

# our color lookuptable is a vtkDiscretizableColorTransferFunction.
# it automatically makes the gradient between our fixed colors
color_lookuptable = vtk.vtkDiscretizableColorTransferFunction()
color_lookuptable.DiscretizeOn()
color_lookuptable.SetNumberOfValues(nb_colors)
color_lookuptable.AddRGBPoint(color_min, *colorConst['BLUE'])  # special case
color_lookuptable.AddRGBPoint(color_min + 1, *colorConst['GREEN'])
color_lookuptable.AddRGBPoint(1000, *colorConst['BEIGE'])
color_lookuptable.AddRGBPoint(3000, *colorConst['GRAY'])
color_lookuptable.AddRGBPoint(color_max, *colorConst['WHITE'])
color_lookuptable.Build()

# --------------------------------------------
points = vtk.vtkPoints()
cells = vtk.vtkCellArray()

points_ids = [[0 for x in range(width)] for y in range(height)]
points_ints = [[0 for x in range(width)] for y in
               range(height)]  # [0][0] point en haut a gauche [max][max] en bas a droite

# Generate the colors for each point based on the color map
colors = vtk.vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetName('Colors')

print('get ints from file')  # we do this here and not below, because we need to know next altitude for lake
# as the value in the file are rotated 90 degree left, we have to rotate back, but that mirrors the x values, so we need to unmirror the x values
for i in range(height):
    line = f.readline().split()
    for j in range(width):
        points_ints[j][i] = int(line[(
                                                 width - 1) - j])  # rotate back with the [j][i] instead of [i][j], we also mirror the width values with (width-1)-j

print('get points and color for each int')
for i in range(width):
    for j in range(height):

        pointTransform = vtk.vtkTransform()
        pointTransform.RotateY(
            longitude_base_angle + (
                        i * factor_longitude_latitude))  # to get x, we rotate around Y, we start right and go left
        pointTransform.RotateX(latitude_base_angle - (
                    j * factor_longitude_latitude))  # to get y we rotate around X, we start up and go down
        pointTransform.Translate(0, 0, (earth_radius + points_ints[i][j]))
        position = 3 * [0.0]
        position = pointTransform.GetPosition()

        # do points
        points_ids[i][j] = points.InsertNextPoint(position)  # round earth
        # points_ids[i][j] = points.InsertNextPoint(i,j,points_ints[i][j])  # flat earth

        # do scalar color
        if (i > 0 and j > 0 and i < (width - 1) and (j < (height - 1)) and (
                points_ints[i][j] == points_ints[i - 1][j] == points_ints[i + 1][j] == points_ints[i][j - 1] ==
                points_ints[i][j + 1] == points_ints[i + 1][j + 1] == points_ints[i + 1][j - 1] == points_ints[i - 1][
                    j + 1] == points_ints[i - 1][j - 1])):
            # this is a lake
            dcolor = 3 * [0.0]
            color_lookuptable.GetColor(color_water, dcolor)  # we use the color_lookuptable like this
            color = 3 * [0.0]
            for k in range(0, 3):
                color[k] = int(255.0 * dcolor[k])
            colors.InsertNextTypedTuple(color)

        else:
            if climate_crisis and points_ints[i][j] < genf:
                # this drowned
                dcolor = 3 * [0.0]
                color_lookuptable.GetColor(color_water, dcolor)  # we use the color_lookuptable like this
                color = 3 * [0.0]
                for k in range(0, 3):
                    color[k] = int(255.0 * dcolor[k])
                colors.InsertNextTypedTuple(color)

            else:
                dcolor = 3 * [0.0]
                color_lookuptable.GetColor(points_ints[i][j], dcolor)
                color = 3 * [0.0]
                for k in range(0, 3):
                    color[k] = int(255.0 * dcolor[k])
                colors.InsertNextTypedTuple(color)

print('get cells')
# we could put the double for in the double for just up from here to save computation time, but that would be complicated
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
polydata.GetPointData().SetScalars(colors)  # apparently you can bind a lookup table instead of doing this

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

# for some reason, our polydata is upside down (probably because I prefer the 0,0 point up left instead of down left)
# therefore we rotate it and everything is fixed
polydataTransform = vtk.vtkTransform()
polydataTransform.RotateZ(180)
polydataActor.SetUserTransform(polydataTransform)  # set
renWin.Render()

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()