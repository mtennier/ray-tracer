import numpy as np
from constants import *

'''
    Classes for various scene objects.  
'''

class Plane():
    near = None # float
    left = None # float
    right = None # float
    bottom = None # float
    top = None # float
    def __init__(self):
        pass
    def set_near(self, near):
        self.near = near
    def set_left(self,left):
        self.left = left
    def set_right(self,right):
        self.right = right
    def set_bottom(self,bottom):
        self.bottom = bottom
    def set_top(self,top):
        self.top = top

    def get_width(self):
        return self.right - self.left

    def get_height(self):
        return self.top - self.bottom
    
    def __str__(self):
        s = f'Near plane: {self.near}\n'
        s += f'Left:{self.left}\n'
        s += f'Right:{self.right}\n'
        s += f'Bottom:{self.bottom}\n'
        s += f'Top:{self.top}'
        return s


class Sphere():
    name = None # str
    position = None # vec 3
    scale = None # vec 3
    color = None # vec 4
    ka = None # float
    kd = None # float
    ks = None # float
    kr = None # float
    n = None # float
    def __init__(self,name,vals):
        self.name = name
        self.position = np.array([vals[0],vals[1],vals[2]])
        self.scale = np.array(vals[3:6])
        self.color = np.array(vals[6:9])
        self.ka = vals[9]
        self.kd = vals[10]
        self.ks = vals[11]
        self.kr = vals[12]
        self.n = vals[13]
        self.transformation_matrix = self.get_transformation_matrix()
        self.inverse_matrix = self.get_inverse_matrix()
        self.inverse_transpose = self.get_inverse_transpose_matrix()

    def get_transformation_matrix(self):
        '''
            Gets the transformation matrix for a sphere.
        '''
        m = np.array([[self.scale[0],0,0,self.position[0]],
                      [0,self.scale[1],0,self.position[1]],
                      [0,0,self.scale[2],self.position[2]],
                      [0,0,0,1]])
        return m
    
    def get_inverse_matrix(self):
        '''
            Gets the inverse transformation matrix for a sphere.
        '''
        return np.linalg.inv(self.transformation_matrix)
    
    def get_inverse_transpose_matrix(self):
        '''
            Gets the inverse transpose matrix of a sphere.
        '''
        return np.transpose(self.inverse_matrix)

    def __str__(self):
        s = ''
        s += f'Sphere name:{self.name}\n'
        s += f'Position:{self.position}\n'
        s += f'Scale:{self.scale}\n'
        s += f'Color:{self.color}\n'
        s += f'Ka:{self.ka}, Ks:{self.ks}, Kr:{self.kr}, N:{self.n}'
        return s


class LightSource():
    name = None # str
    position = None # vec 3
    intensity = None # vec 3
    def __init__(self,name,vals):
        self.name = name
        self.position = np.array([vals[0],vals[1],vals[2]])
        self.intensity = np.array([vals[3],vals[4],vals[5]])

    def __str__(self):
        s = ''
        s+= f'Light source name: {self.name}\n'
        s+= f'Light source position:{self.position}\n'
        s+= f'Light source intensity:{self.intensity}'
        return s

class Color():
    '''
        Color class - for pixels.
        If I was smart I would've stored both the decimal RGB and 
        the 255 RGB!
    '''
    r = 0
    g = 0
    b = 0
    def __init__(self,red,green,blue):
        self.r = min(int(255*red),255)
        self.g = min(int(255*green),255)
        self.b = min(int(255*blue),255)
    
    def __str__(self):
        return f'{self.r},{self.g},{self.b}'
    
    def __mul__(self,other):
        r = self.r * other.r
        g = self.g * other.g
        b = self.b * other.b
        return Color(r,g,b)
    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __add__(self,other):
        return Color((self.r + other.r)/255,(self.g + other.g)/255, (self.b + other.b)/255)
    
    def __eq__(self,other):
        return self.r == other.r and self.g == other.g and self.b == other.b
    
    def apply_scalar(self, scalar):
        '''
            Applies a scalar to self,
            and then returns a new Color which
            has been multiplied by the scalar.
        '''
        r = (self.r * scalar)/255
        g = (self.g * scalar)/255
        b = (self.b * scalar)/255
        return Color(r,g,b)


    def to_np_array(self):
        '''
            Converts a color to a NP array.
        '''
        return np.array([self.r,self.g,self.b])


class Pixel():
    color = None
    def __init__(self,c):
        self.color = c


class Scene():
    plane = None # Plane object
    resolution = None # array of 2
    spheres = None # list of Sphere object
    light_sources = None # list of LightSource object
    bg_color = None # vec3
    ambience = None # vec3
    def __init__(self, plane,resolution,spheres,light_sources,bg_color,ambience):
        self.plane = plane
        self.resolution = resolution
        self.spheres = spheres
        self.light_sources = light_sources
        self.bg_color = bg_color
        self.ambience = ambience
    def __str__(self):
        s = ''
        s += f'Plane:\n{self.plane}\n'
        s += f'Resolution:{self.resolution}\n'
        s += f'++++++++++\n'
        s += 'Spheres:\n'
        for sp in self.spheres:
            s+=f'{str(sp)}\n'
            s+= f'----------\n'
        s += f'++++++++++\n'
        s+= 'Light sources:\n'
        for l in self.light_sources:
            s+=f'{str(l)}\n'
            s += f'----------\n'
        s += f'+++++++++++\n'
        s+=f'BG color:{self.bg_color}\n'
        s+=f'Ambience:{self.ambience}'
        return s
