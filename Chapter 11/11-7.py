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
