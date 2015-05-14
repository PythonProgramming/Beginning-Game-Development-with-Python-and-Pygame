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
