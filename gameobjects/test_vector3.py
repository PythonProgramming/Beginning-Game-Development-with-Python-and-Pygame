import unittest

from .vector3 import Vector3

class TestVector3(unittest.TestCase):

    def test_add(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        self.assertEqual(v1+v2, (5, 7, 9))
        self.assertEqual((1, 2, 3)+v2, (5, 7, 9))


    def test_sub(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        self.assertEqual(v1-v2, (-3, -3, -3))
        self.assertEqual((1, 2, 3)-v2, (-3, -3, -3))


    def test_mul(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        self.assertEqual(3*v1, (3, 6, 9))
        self.assertEqual(v1*3, (3, 6, 9))
        self.assertEqual((3, 3, 3)*v1, (3, 6, 9))
        self.assertEqual(v1*(3, 3, 3), (3, 6, 9))
        v1 *= 2
        self.assertEqual(v1, (2, 4, 6))

    def test_div(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        self.assertEqual(3/v1, (3., 3./2, 1.))
        self.assertEqual(v1/3, (1./3, 2/3., 3/3.))
        self.assertEqual((3, 3, 3)/v1, (3./1., 3./2., 3./3.))
        self.assertEqual(v1/(3, 3, 3), (1./3, 2/3., 3/3.))
        v1 /= 2
        self.assertEqual(v1, (.5, 1., 1.5))

    def test_length(self):
        v1 = Vector3(3., 4., 0.)
        self.assertEqual(v1.length, 5.)
        v1.length = 10.
        self.assertEqual(v1, (6, 8, 0))
        v1.normalise()
        assert v1.length, 1

    def test_copy(self):
        v1 = Vector3(3., 4., 0.)
        assert v1.copy(), (3, 4, 0)

    def test_properties(self):
        v1 = Vector3(1, 2, 3)
        self.assertEqual(v1.x, 1)
        self.assertEqual(v1.y, 2)
        self.assertEqual(v1.z, 3)
        v1.x *= 2
        v1.y *= 2
        v1.z *= 2
        self.assertEqual(v1.x, 2)
        self.assertEqual(v1.y, 4)
        self.assertEqual(v1.z, 6)

    def test_swizzle(self):
        v1 = Vector3(1, 2, 3)
        self.assertEqual(v1('xxxyyyzzz'), (1, 1, 1, 2, 2, 2, 3, 3, 3))
        self.assertEqual(v1('yyy'), (2, 2, 2))
        self.assertEqual(v1('zyx'), (3, 2, 1))

if __name__ == '__main__':
    unittest.main()
