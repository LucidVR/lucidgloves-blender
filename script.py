import serial
import time
import bpy
import math

ser = serial.Serial('COM4', '115200')
time.sleep(3)
ser.write(b'READ_VALUES\n')
#start = float(ser.readline()) / 200
#cube = bpy.context.selected_objects[0]
       
ob = bpy.data.objects['Armature']
#bpy.context.scene.objects.active = ob
bpy.ops.object.mode_set(mode='POSE')
pbone = ob.pose.bones["thumb.02.R"]
pbone.rotation_mode = 'XYZ'

lowLimit =  [0 , 0 , 0 , 0 , 0]
highLimit = [1023 , 1023 , 1023 , 1023 , 1023]
axis = ['X', 'X', 'X', 'X', 'Z']

actuationAngle = [100, 100, 100, 100, 150]

fingerBones = [
    ob.pose.bones["finger_pinky.01.L"],
    ob.pose.bones["finger_ring.01.L"],
    ob.pose.bones["finger_middle.01.L"],
    ob.pose.bones["finger_index.01.L"],
    ob.pose.bones["thumb.02.L"]
]

for fing in range(5):
    fingerBones[fing].rotation_mode = 'XYZ'

last = [0,0,0,0,0]
for x in range(3):
    for y in range(100):
        ser.write(b'READ_VALUES\n')
        read = ser.readline()
        print(read)
        lineTable = read.decode().split(',')
        for fing in range(5):
            thisVal = float(lineTable[fing].rstrip())
            current = ((highLimit[fing] - thisVal) * actuationAngle[fing]/ (highLimit[fing]-lowLimit[fing]))
            if (current < 0):
                current = 0 
            #cube.location.z = start-current
            fingerBones[fing].rotation_euler.rotate_axis(axis[fing], math.radians(current - last[fing]))
            last[fing] = current
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations = 1)
    
for fing in range(5):
    pbone.rotation_euler.rotate_axis(axis[fing], math.radians(-last[fing]))

bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations = 1)
ser.close()