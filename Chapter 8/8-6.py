def perspective_project(vector3, d):
    x, y, z = vector3
    return (x * d/z, -y * d/z)
