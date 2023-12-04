import numpy as np
from SceneClasses import *
from constants import *
from multiprocessing import Pool

class Ray():
    depth = 0 # int
    s = None #vec3, starting point
    c = None #vec3, also the magnitude, direction
    def __init__(self, st, dr):
        self.s = st
        self.c = dr / np.linalg.norm(dr) # normalize the direction since rays have no magnitude

    def set_depth(self,d):
        self.depth = d


    def intersects_unit_sphere(self,s):
        '''
            Checks whether a ray intersects with the unit sphere
            after going through an inverse of the transformation of s.
        '''
        tm = s.inverse_matrix
        self.apply_transformation(tm)
        itm = s.transformation_matrix
        # print(self.c)
        A = np.linalg.norm(self.c)**2 # |c|^2
        B = np.dot(self.s, self.c) # s dot c
        C = np.linalg.norm(self.s)**2 - 1 # |s|^2 - 1
        discriminant = B**2 - A*C
        t = None
        N = None
        # print(A)
        # print(B)
        # print(C)
        # print(discriminant)
        if discriminant > NumberConstants.ZERO_OFFSET:
            t1 = (-B/A) + ( np.sqrt(discriminant) / A)
            t2 = (-B/A) - ( np.sqrt(discriminant) / A)
            if not (t1 < 0 and t2 < 0):
                # if they are both negative it hit behind img plane
                if t1 < 0 or t2 < 0:
                    # one is negative
                    t = max(t1,t2)
                else:
                    t = min(t1,t2)
                
                # get N value
                n = self.get_ray_at_point(t) # get the value of the ray at T
                N = self.apply_inverse_transpose(n,s) # apply inverse transpose to point
                N = N / np.linalg.norm(N) # normalize
                if t1 < 0 or t2 < 0:
                    N = -N
        # revert our ray
        self.apply_transformation(itm)
        return t, N
    

    def apply_inverse_transpose(self,p,s):
        '''
            Applies the inverse transpose of sphere s to a point p
        '''
        new_p = np.array([p[0],p[1],p[2],1])
        new_p = s.inverse_transpose.dot(np.vstack(new_p))
        new_p = np.ravel(new_p)
        # Cut off last part.
        return new_p[:-1]

    def apply_transformation(self,transform_matrix):
        '''
            Applies a transformation matrix to a ray.
        '''
        # Transform into 4x1 so we can apply the scale.
        new_s = np.array([self.s[0],self.s[1],self.s[2],1])
        new_s = transform_matrix.dot(np.vstack(new_s))
        new_c = np.array([self.c[0],self.c[1],self.c[2],0])
        new_c = transform_matrix.dot(np.vstack(new_c)) 
        new_s = np.ravel(new_s)
        new_c = np.ravel(new_c)
        # Save new values in array.
        self.s = new_s[:-1]
        self.c = new_c[:-1]

    def get_ray_at_point(self, pt):
        '''
            Returns the value of a ray at a point.
        '''
        return self.s + self.c * pt
    

    def __str__(self):
        return f'Start:{self.s}, Direction:{self.c}'
        


class RayTracer():
    scene = None # Scene object
    colored_pixels = None # nxm array representing the colors where n is the width m is the height
    def __init__(self,s:Scene):
        self.scene = s

    def pool_func(self,row,col,count):
        print(f'drawing pixel {count}....')
        eye_pos = np.array([0,0,0])
        ray = self.calc_ray_through_pixel(eye_pos,row,col)
        ray.set_depth(1)
        color = self.raytrace(ray)
        return Pixel(color)

        
    def trace_rays(self):
        '''
            The "main" in the psuedocode.
            Begins raytracing and calls the raytrace recursive function.
        '''
        eye_pos = np.array([0,0,0])
       
        pixels = [] # These save the RGB values of each pixel
        count = 0
        # start at top left - hence weird for loop!
        # NEW
        try:
            args = []
            for row in range(self.scene.resolution[RayConstants.ROWS]-1,-1,-1):
                # pixel_row = []
                for col in range(self.scene.resolution[RayConstants.COLS]):
                    count+=1
                    args.append((row,col,count))
            with Pool() as pool:
                print('creating pool....')
                p = pool.starmap(self.pool_func,args)
                pool.close()
                pool.join()
            np_p = np.array(p)
            pixels = np_p.reshape(600,600)
        except:
            # if multithreading doesnt work, use manual fallback
            print('multiprocessing failed, restarting using single thread....')
            pixels = [] # These save the RGB values of each pixel
            count = 0
            for row in range(self.scene.resolution[RayConstants.ROWS]-1,-1,-1):
                pixel_row = []
                for col in range(self.scene.resolution[RayConstants.COLS]):
                    print(f'drawing pixel: {count}')
                    ray = self.calc_ray_through_pixel(eye_pos,row,col)
                    ray.set_depth(1)
                    color = self.raytrace(ray)
                    pixel_row.append(Pixel(color))
                    count+=1
                pixels.append(pixel_row)
        
        return pixels
    
    


    def calc_camera_coord_of_pixel(self,rows,cols):
        '''
            Converts the pixel coordinates to camera coordinates.
        '''
        nRows = self.scene.resolution[RayConstants.ROWS]
        nCols = self.scene.resolution[RayConstants.COLS]
        w = self.scene.plane.get_width() / 2 # scene is 2W wide
        h = self.scene.plane.get_height() / 2 # scene is 2C tall
        uc = (-1 * w) + (w * 2 * cols) / nCols
        vr = (-1 * h) + (h * 2 * rows) / nRows
        n =  -1 *self.scene.plane.near
        return np.array([uc,vr,n])

    def calc_ray_through_pixel(self,eye,row,col):
        '''
            Calculates a ray going from the eye through a pixel.
        '''
        p = self.calc_camera_coord_of_pixel(row,col)
        prc = p
        ray_direction = p
        ray = Ray(prc,ray_direction)
        return ray
    

    def find_closest_intersection(self, r):
        '''
            Finds closest intersection sphere.
            Returns said sphere and the closest intersection point.
        '''
        intersection_sphere = None # sphere intersects with
        min_t = 1000000000 # intersection 
        N = None # normal
        for s in self.scene.spheres:
            t,n = r.intersects_unit_sphere(s)
            if t and t < min_t:
                # Get closest intersection
                intersection_sphere = s
                min_t = t
                N = n
        return (intersection_sphere, min_t, N)

    def raytrace(self,r):
        '''
            Function for tracing the rays
            Input is r, a Ray
            Output is a Color
        '''
        intersection_color = self.scene.bg_color
        reflection_color = Color(0,0,0)
        if r.depth > RayConstants.MAX_DEPTH:
            return Color(0,0,0)


        # N: normal vector - from slides
        intersection_sphere, min_t, N = self.find_closest_intersection(r)
        
        if intersection_sphere:
            # Get intersection
            intersection_point = r.get_ray_at_point(min_t)

            # Initialize return color to sphere's color
            intersection_color = Color(intersection_sphere.color[0],intersection_sphere.color[1],intersection_sphere.color[2])

            # Ambience
            ambience = self.scene.ambience * intersection_sphere.ka
            sphere_color = intersection_sphere.color * ambience
            intersection_color = Color(sphere_color[0],sphere_color[1],sphere_color[2])

            diffuse_specular = np.array([0,0,0])

            # V - from point on sphere going back to eye
            # from assign 2: V = normalize(-pos)
            V = - 1 * intersection_point / np.linalg.norm(intersection_point) 

            for l in self.scene.light_sources:
                # from light position to intersection
                direction = l.position - intersection_point

                # not sure why but multiplying direction by the offset works???
                r_from_sphere = Ray(intersection_point + direction * NumberConstants.RAY_START_OFFSET, direction)
                r_from_sphere.set_depth(r.depth+1)
                shadow_inter_sphere, t, _ = self.find_closest_intersection(r_from_sphere)
                if shadow_inter_sphere:
                    shadow_inter_point = r.get_ray_at_point(t)
                if not shadow_inter_sphere or np.linalg.norm(shadow_inter_point - intersection_point) > np.linalg.norm(direction):
                    # shadow ray didnt intersect with any sphere
                    # or ray is light that is inside sphere
                    
                    # L - from point on sphere to light
                    # from assing 2: L = normalize(lpos - pos)
                    L = r_from_sphere.c

                    # V - calculated above for efficiency

                    # N - already given
                    
                    # R - from slides
                    R = (2 * N.dot(L) * N) - L

                    # from A2 and slides
                    diffuse_product = l.intensity * intersection_sphere.color * intersection_sphere.kd
                    light_dot_normal = max( L.dot(N),0.0)
                    diffuse = diffuse_product * light_dot_normal

                    # from assignment 2
                    specular_product = l.intensity * intersection_sphere.ks
                    reflected_dot_view_shiny = max(R.dot(V),0.0)
                    reflected_dot_view_shiny = reflected_dot_view_shiny ** intersection_sphere.n
                    
                    if (L.dot(N) < 0):
                        specular = np.array([0,0,0])
                    else:
                        specular = specular_product * reflected_dot_view_shiny

                    # add the effect of diffuse and specular 
                    diffuse_specular = diffuse_specular + diffuse + specular
                    
            sphere_color = sphere_color + diffuse_specular
            intersection_color = Color(sphere_color[0],sphere_color[1],sphere_color[2])
            
            # reflected ray - formula from slides
            reflected_ray_dir = -2 * N.dot(r.c) * N + r.c
            reflected_ray = Ray(intersection_point + NumberConstants.RAY_START_OFFSET * reflected_ray_dir,reflected_ray_dir)
            reflected_ray.set_depth(r.depth+1)
            reflection = self.raytrace(reflected_ray)
            if reflection != self.scene.bg_color:
                # ie there is something to reflect!
                reflection_color = reflection.apply_scalar(intersection_sphere.kr)
            
               
        # if it does not pass any of the if statements, no intersection
        return intersection_color + reflection_color
    
        
        
        