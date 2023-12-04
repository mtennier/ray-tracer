import numpy as np
from constants import *
from SceneClasses import *
import re
'''
    Classes for the input and output file.
'''

class InputFile():
    filename = None #str
    def __init__(self, fn):
        self.filename = fn

    def read_file(self):
        '''
            Reads in the input file, returns a Scene and str.
            The Scene is the scene from the file, the str is
            the name for the output file.
        '''
        plane = Plane()
        resolution = np.array([])
        spheres = []
        light_sources = []
        background = np.array([])
        ambience = np.array([])
        output_name = ''
        try:
            with open(self.filename,'r') as file_handle:
                lines = file_handle.readlines()
        except:
            print('ERROR OPENING FILE')
            return
        for line in lines:
            line = line.strip()
            if line == '':
                # Empty space put to test my patience.
                continue
            section = re.search(FileSections.SECTION_REGEX,line)
            section_match = section.group()
            if section_match == FileSections.NEAR:
                near = re.search(FileSections.INT_REGEX,line)
                plane.set_near(float(near.group()))
            elif section_match ==  FileSections.LEFT:
                left = re.search(FileSections.INT_REGEX,line)
                plane.set_left(float(left.group()))
            elif section_match == FileSections.RIGHT:
                right = re.search(FileSections.INT_REGEX,line)
                plane.set_right(float(right.group()))
            elif section_match == FileSections.BOTTOM:
                bottom = re.search(FileSections.INT_REGEX,line)
                plane.set_bottom(float(bottom.group()))
            elif section_match == FileSections.TOP:
                top = re.search(FileSections.INT_REGEX,line)
                plane.set_top(float(top.group()))
            elif section_match == FileSections.RES:
                r = re.findall(FileSections.INT_REGEX,line)
                resolution = [int(r[0]),int(r[1])]
            elif section_match == FileSections.SPHERE:
                sname = re.findall(FileSections.NAME_REGEX,line)
                sphere_name = sname[1]
                line = line.replace(sphere_name,'') # So regex possibly wont pick up on sphere name.
                rest = re.findall(FileSections.NUM_REGEX,line)
                lst_to_float = [float(num) for num in rest]
                s = Sphere(sphere_name,lst_to_float) 
                spheres.append(s)
            elif section_match == FileSections.LIGHT:
                lname= re.findall(FileSections.NAME_REGEX,line)
                light_name = lname[1]
                line = line.replace(light_name, '')
                rest = re.findall(FileSections.NUM_REGEX,line)
                lst_to_float = [float(num) for num in rest]
                l = LightSource(light_name,lst_to_float)
                light_sources.append(l)
            elif section_match == FileSections.BACK:
                back = re.findall(FileSections.NUM_REGEX,line)
                lst_to_float = [float(num) for num in back]
                background = Color(lst_to_float[0],lst_to_float[1],lst_to_float[2])
            elif section_match == FileSections.AMBIENT:
                amb = re.findall(FileSections.NUM_REGEX,line)
                lst_to_float = [float(num) for num in amb]
                ambience = np.array([lst_to_float[0],lst_to_float[1],lst_to_float[2]])
            elif section_match == FileSections.OUTPUT:
                o = re.findall(FileSections.NAME_REGEX,line)
                output_name = o[1] + '.' + o[2]
            else:
                print('ERROR - INVALID FLAG')
                return
        scene = Scene(plane,resolution,spheres,light_sources,background,ambience)
        return scene, output_name


class OutputFile():
    scene = None # scene object
    filename = None # str
    pixels = None # list of pixel objects
    def __init__(self, scene, filename, pixels):
        self.scene = scene
        self.filename = filename
        self.pixels = pixels

    def write_to_pp3_file(self):
        '''
            A modified port of C++ code to write to a ppm file.
        '''
        print('Writing to file in P3 format.')
        width = self.scene.resolution[RayConstants.ROWS]
        height = self.scene.resolution[RayConstants.COLS]
        with open(self.filename, 'w') as fp:
            fp.write('P3\n')
            fp.write(f'{width} {height}\n')
            fp.write(f'{ColorConstants.MAX_COLOR_VAL}\n')
            k = 0

            for r in self.pixels:
                for p in r:
                    fp.write(f' {int(p.color.r)} {int(p.color.g)} {int(p.color.b)}')
                fp.write('\n')