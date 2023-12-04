import numpy as np
from constants import *
from FileClasses import *
from SceneClasses import *
from RayTracingClasses import *
import sys

def main():
    '''
        Main function
    '''
    if len(sys.argv) < 2:
        print('Error - too few args')
        return
    filename = sys.argv[1]
    input_file = InputFile(filename)
    scene, output_name = input_file.read_file()
    rt = RayTracer(scene)
    p = rt.trace_rays()
    o = OutputFile(scene,output_name,p)
    o.write_to_pp3_file()


if __name__ == "__main__":
    main()