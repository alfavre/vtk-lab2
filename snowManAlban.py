#!/usr/bin/env python
#
# This code will build a snowman with proportions pifometred
# When the snowman is built, the camera will do a little dance
#
import vtk
import time


# Next we create an instance of vtkConeSource and set some of its
# properties.
cone = vtk.vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Next we create an instance of vtkSphere and set some of its
# properties.
sphere = vtk.vtkSphereSource()
sphere.SetPhiResolution(30)  # roundness but just from a side
sphere.SetThetaResolution(30)  # roundness from the other side

# We create an instance of
# vtkPolyDataMapper to map the polygonal data into graphics primitives. We
# connect the output of the cone source to the input of this mapper.
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection(cone.GetOutputPort())

# We create an instance of
# vtkPolyDataMapper to map the polygonal data into graphics primitives. We
# connect the output of the sphere source to the input of this mapper.
sphereMapper = vtk.vtkPolyDataMapper()
sphereMapper.SetInputConnection(sphere.GetOutputPort())

# Create an actor to represent the cone as the nose.
nose = vtk.vtkActor()
nose.SetMapper(coneMapper)
nose.SetScale(0.05, 0.05, 0.05)
nose.SetPosition(1, 0, 0)
nose.RotateZ(-90)
nose.GetProperty().SetColor(1, 0.5, 0.0)  # 100% red + 50% green makes orange

# Create an actor to represent the sphere as the body.
body = vtk.vtkActor()
body.SetMapper(sphereMapper)
body.SetScale(1, 1, 1)
body.SetPosition(0, 0, 0)
body.GetProperty().SetColor(1, 1, 1)

# Create an actor to represent the sphere as the head.
head = vtk.vtkActor()
head.SetMapper(sphereMapper)
head.SetScale(0.7, 0.7, 0.7)
head.SetPosition(-1, 0, 0)
head.GetProperty().SetColor(1, 1, 1)

# Create an actor to represent the sphere as the left eye.
leftEye = vtk.vtkActor()
leftEye.SetMapper(sphereMapper)
leftEye.SetScale(0.125, 0.125, 0.125)
leftEye.SetPosition(0, 0, 0)
leftEye.GetProperty().SetColor(0, 0, 0)  # absolute black eyes

# Create an actor to represent the sphere as the right eye.
rightEye = vtk.vtkActor()
rightEye.SetMapper(sphereMapper)
rightEye.SetScale(0.125, 0.125, 0.125)
rightEye.SetPosition(0, 0, 0)
rightEye.GetProperty().SetColor(0, 0, 0) # absolute black eyes

# Create a camera that will be rotated
camera = vtk.vtkCamera()
camera.SetFocalPoint(0, 0, 0)  # looks at the center
camera.SetPosition(0, 0, 10)  # is 10 from the center aback


#
# Create the Renderer and assign actors to it. A renderer is like a
# viewport. It is part or all of a window on the screen and it is
# responsible for drawing the actors it has.  We also set the background
# color here
#
ren1 = vtk.vtkRenderer()
ren1.AddActor(nose)
ren1.AddActor(body)
ren1.AddActor(head)
ren1.AddActor(leftEye)
ren1.AddActor(rightEye)
ren1.SetActiveCamera(camera)
ren1.SetBackground(1, 0.9, 0.9)  # really light pink

#
# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We also
# set the size to be usable
#
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(1000, 1000)  # this big so we can see anything


# -----------------Actors--------------------------------------------


# starting render
renWin.Render()
print("view start")
time.sleep(1)  # wait one to see three vtk actors

noseTransform = vtk.vtkTransform()
headTransform = vtk.vtkTransform()
bodyTransform = vtk.vtkTransform()
leftEyeTransform = vtk.vtkTransform()
rightEyeTransform = vtk.vtkTransform()


sleepTime = 0.02  # controls speed, smaller means faster

print("rotate head start")
for i in range(0, 90):  # for each 90 degree
    time.sleep(sleepTime)  # time
    headTransform.RotateZ(-1)  # rotate around center but clockwise
    head.SetUserTransform(headTransform)  # set
    renWin.Render()


print("glue head start")
for i in range(0, 20):  # for each distance unit beetween head and body (pifometre)
    time.sleep(sleepTime)  # time
    headTransform.Translate(0.01, 0, 0)
    head.SetUserTransform(headTransform)  # set
    renWin.Render()


print("rotate nose in front of body start")
for i in range(0, 90):  # for each 90 degree
    time.sleep(sleepTime)  # time
    noseTransform.RotateY(-1)  # rotate around center but clockwise
    nose.SetUserTransform(noseTransform)
    renWin.Render()


nereastPostionBeforeCovidLimit = 21  # 20 is too high and 20 too low, cant make it a float :(
print("approach nose to body but don't touch start")
# for each distance unit beetween nose and where we want
for i in range(0, nereastPostionBeforeCovidLimit):
    time.sleep(sleepTime)  # time
    noseTransform.Translate(-0.01, 0, 0)
    nose.SetUserTransform(noseTransform)
    renWin.Render()


print("rotate nose inside head start")
for i in range(0, 90):  # for each 90 degree
    time.sleep(sleepTime)  # time
    # secretly undo translation
    noseTransform.Translate(0.01 * nereastPostionBeforeCovidLimit, 0, 0)
    noseTransform.RotateZ(1)  # rotate around center but clockwise
    # secretly redo translation
    noseTransform.Translate(-0.01 * nereastPostionBeforeCovidLimit, 0, 0)
    nose.SetUserTransform(noseTransform)
    renWin.Render()

print("point nose start")
for i in range(0, 40):  # for each distance unit beetween nose and where we want it
    time.sleep(sleepTime)  # time
    noseTransform.Translate(0, -0.01, 0)
    nose.SetUserTransform(noseTransform)
    renWin.Render()

print("pop eyes")
leftEyeTransform.Translate(-0.12, 0.85, 0.3)
rightEyeTransform.Translate(0.12, 0.85, 0.3)

leftEye.SetUserTransform(leftEyeTransform)
rightEye.SetUserTransform(rightEyeTransform)
renWin.Render()

# --------------Cameras----------------

print("Camera does a barrel roll start")

for i in range(0, 360):
    time.sleep(sleepTime)  # time
    ren1.GetActiveCamera().Roll(1)
    renWin.Render()


print("Camera run around snowman start")
for i in range(0, 360):
    time.sleep(sleepTime)  # time
    ren1.GetActiveCamera().Azimuth(1)
    renWin.Render()


print("Camera quickly checks top of snowman's head")
for i in range(0, 80): # doesn't go the full 90, idk why
    time.sleep(sleepTime)  # time
    # Insert Camera Rotations Below
    ren1.GetActiveCamera().Elevation(1)
    renWin.Render()

print("Camera calms down and goes back to it's starting position")
for i in range(0, 80):
    time.sleep(sleepTime)  # time
    ren1.GetActiveCamera().Elevation(-1)
    renWin.Render()

print("Lab 1 over, wait 2 before quit")

time.sleep(2)  # time
