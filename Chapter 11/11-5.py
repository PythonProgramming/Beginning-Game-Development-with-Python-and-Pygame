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
