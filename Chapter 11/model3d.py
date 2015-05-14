
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
import os.path

class Material(object):

    def __init__(self):

        self.name = ""
        self.texture_fname = None
        self.texture_id = None


class FaceGroup(object):

    def __init__(self):

        self.tri_indices = []
        self.material_name = ""


class Model3D(object):

    def __init__(self):
        
        self.vertices = []
        self.tex_coords = []
        self.normals = []
        self.materials = {}
        self.face_groups = []
        self.display_list_id = None

    def __del__(self):

        #Called when the model is cleaned up by Python
        self.free_resources()

    def free_resources(self):

        # Delete the display list and textures
        if self.display_list_id is not None:
            glDeleteLists(self.display_list_id, 1)            
            self.display_list_id = None

        # Delete any textures we used
        for material in self.materials.values():
            if material.texture_id is not None:                
                glDeleteTextures(material.texture_id)
                
        # Clear all the materials
        self.materials.clear()        
        
        # Clear the geometry lists
        del self.vertices[:]
        del self.tex_coords[:]
        del self.normals[:]        
        del self.face_groups[:]        
        


    def read_obj(self, fname):

        current_face_group = None

        file_in = open(fname)

        for line in file_in:

            # Parse command and data from each line
            words = line.split()
            command = words[0]
            data = words[1:]

            if command == 'mtllib': # Material library

                model_path = os.path.split(fname)[0]
                mtllib_path = os.path.join( model_path, data[0] )                                
                self.read_mtllib(mtllib_path)
                
            elif command == 'v': # Vertex
                x, y, z = data
                vertex = (float(x), float(y), float(z))
                self.vertices.append(vertex)

            elif command == 'vt': # Texture coordinate

                s, t = data
                tex_coord = (float(s), float(t))
                self.tex_coords.append(tex_coord)

            elif command == 'vn': # Normal

                x, y, z = data
                normal = (float(x), float(y), float(z))
                self.normals.append(normal)

            elif command == 'usemtl' : # Use material

                current_face_group = FaceGroup()
                current_face_group.material_name = data[0]
                self.face_groups.append( current_face_group )

            elif command == 'f':

                assert len(data) ==  3, "Sorry, only triangles are supported"

                # Parse indices from triples
                for word in data:
                    vi, ti, ni = word.split('/')
                    indices = (int(vi) - 1, int(ti) - 1, int(ni) - 1)
                    current_face_group.tri_indices.append(indices)


        for material in self.materials.values():

            model_path = os.path.split(fname)[0]
            texture_path = os.path.join(model_path, material.texture_fname)
            texture_surface = pygame.image.load(texture_path)
            texture_data = pygame.image.tostring(texture_surface, 'RGB', True)

            material.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, material.texture_id)

            glTexParameteri( GL_TEXTURE_2D,
                             GL_TEXTURE_MAG_FILTER,
                             GL_LINEAR)
            glTexParameteri( GL_TEXTURE_2D,
                             GL_TEXTURE_MIN_FILTER,
                             GL_LINEAR_MIPMAP_LINEAR)

            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            width, height = texture_surface.get_rect().size
            gluBuild2DMipmaps( GL_TEXTURE_2D,
                               3,
                               width,
                               height,
                               GL_RGB,
                               GL_UNSIGNED_BYTE,
                               texture_data)


    def read_mtllib(self, mtl_fname):

        file_mtllib = open(mtl_fname)
        for line in file_mtllib:

            words = line.split()
            command = words[0]
            data = words[1:]

            if command == 'newmtl':
                material = Material()
                material.name = data[0]
                self.materials[data[0]] = material

            elif command == 'map_Kd':
                material.texture_fname = data[0]


    def draw(self):

        vertices = self.vertices
        tex_coords = self.tex_coords
        normals = self.normals

        for face_group in self.face_groups:
        
            material = self.materials[face_group.material_name]
            glBindTexture(GL_TEXTURE_2D, material.texture_id)

            glBegin(GL_TRIANGLES)
            for vi, ti, ni in face_group.tri_indices:
                glTexCoord2fv( tex_coords[ti] )
                glNormal3fv( normals[ni] )
                glVertex3fv( vertices[vi] )
            glEnd()


    def draw_quick(self):

        if self.display_list_id is None:
            self.display_list_id = glGenLists(1)
            glNewList(self.display_list_id, GL_COMPILE)
            self.draw()
            glEndList()

        glCallList(self.display_list_id)
