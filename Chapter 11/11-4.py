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
