from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
import os.path

class Material(object):

  def   init (self):

        self.name = ""
        self.texture_fname = None
        self.texture_id = None

class FaceGroup(object):

  def   init (self):

        self.tri_indices = []
        self.material_name = ""

class Model3D(object):

  def   init (self):

        self.vertices = []
        self.tex_coords = []
        self.normals = []
        self.materials = {}
        self.face_groups = []
        # Display list id for quick rendering
        self.display_list_id = None
