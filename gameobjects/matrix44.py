
from gameobjects.util import format_number
from gameobjects.vector3 import Vector3

from math import sin, cos, tan, sqrt, pi, radians

#import psyco
#psyco.full()

class Matrix44Error(Exception):

    """Matrix44 Exception class"""

    def __init__(self, code, description):
        Exception.__init__(self)
        self.code = code
        self.description = description

    def __str__(self):
        return "%s (%s)" % (self.description, self.code)


class Row(tuple):

    """Represents the contents of a row when accessed through a property.

    """

    _type_error = "A vector type must be used to do math on rows"


    def __add__(self, rhs):
        try:
            return rhs.__radd__(self[:rhs._gameobjects_vector])
        except AttributeError:
            raise TypeError(self._type_error)

    def __sub__(self, rhs):
        try:
            return rhs.__sub__(self[:rhs._gameobjects_vector])
        except AttributeError:
            raise TypeError(self._type_error)

    def __mul__(self, rhs):
        try:
            return rhs.__mul__(self[:rhs._gameobjects_vector])
        except AttributeError:
            raise TypeError(self._type_error)

    def __div__(self, rhs):
        try:
            return rhs.__div__(self[:rhs._gameobjects_vector])
        except AttributeError:
            raise TypeError(self._type_error)


    def as_vec3(self):
        """Shorthand for converting to a vector3."""
        return Vector3._from_float_sequence(self)


class Matrix44(object):

    _identity = ( (1.0, 0.0, 0.0, 0.0),
                  (0.0, 1.0, 0.0, 0.0),
                  (0.0, 0.0, 1.0, 0.0),
                  (0.0, 0.0, 0.0, 1.0) )

    __slots__ = ('_m',)

    def __init__(self, *args):

        """If no parameteres are given, the Matrix44 is initialised to identity.
        If 1 parameter is given it should be an iterable with the 16 components
        of the matrix.
        If 4 parameters are given they should be 4 sequences of up to 4 values.
        Missing values in each row are padded out with values from the identity matix
        (so you can use Vector3's or tuples of 3 values).

        """


        if not args:
            self._m = [1.,0.,0.,0., 0.,1.,0.,0., 0.,0.,1.,0., 0.,0.,0.,1.]
            return


        elif len(args) == 4:
            self._m = [1.,0.,0.,0., 0.,1.,0.,0., 0.,0.,1.,0., 0.,0.,0.,1.]

            row_0, row_1, row_2, row_3 = self._setters
            r1, r2, r3, r4 = args

            row_0(self, r1)
            row_1(self, r2)
            row_2(self, r3)
            row_3(self, r4)

        else:
            raise TypeError("Matrix44.__init__() takes 0, or 4 arguments (%i given)"%len(args))


    def _get_row_0(self):
        return Row(self._m[0:4])

    def _get_row_1(self):
        return Row(self._m[4:8])

    def _get_row_2(self):
        return Row(self._m[8:12])

    def _get_row_3(self):
        return Row(self._m[12:16])

    def _set_row_0(self, values):
        values = tuple(values)[:4]
        self._m[0:len(values)] = list(map(float, values))

    def _set_row_1(self, values):
        values = tuple(values)[:4]
        self._m[4:4+len(values)] = list(map(float, values))

    def _set_row_2(self, values):
        values = tuple(values)[:4]
        self._m[8:8+len(values)] = list(map(float, values))

    def _set_row_3(self, values):
        values = tuple(values)[:4]
        self._m[12:12+len(values)] = list(map(float, values))

    _getters = (_get_row_0, _get_row_1, _get_row_2, _get_row_3)
    _setters = (_set_row_0, _set_row_1, _set_row_2, _set_row_3)

    _row0 = property(_get_row_0, _set_row_0, None, "Row 0")
    _row1 = property(_get_row_1, _set_row_1, None, "Row 1")
    _row2 = property(_get_row_2, _set_row_2, None, "Row 2")
    _row3 = property(_get_row_3, _set_row_3, None, "Row 3")

    x_axis = _row0
    right = _row0
    y_axis = _row1
    up = _row1
    z_axis = _row2
    forward = _row2
    translate = _row3


    def to_opengl(self):

        """Converts the matrix in to a list of values, suitable for using
        with glLoadMatrix*

        """

        return self._m[:]


    def set(self, row1, row2, row3, row4):

        """Sets all four rows of the matrix,

        @type row1: sequence
        @param row1: First row
        @type row2: sequence
        @param row2: Second row
        @type row3: sequence
        @param row3: Third row
        @type row4: sequence
        @param row4: Fourth row
        @return: None

        """

        set_row_0, set_row_1, set_row_2, set_row_3 = self._setters

        set_row_0(self, row1)
        set_row_1(self, row2)
        set_row_2(self, row3)
        set_row_3(self, row4)


    def get_row(self, row_no):
        """Gets a row of the matrix as a tuple

        row_no -- Index of row

        """
        try:
            return self._getters[row_no](self)
        except IndexError:
            raise IndexError("Row must be 0, 1, 2 or 3")


    @classmethod
    def from_iter(cls, iterable):
        """Creates a Matrix44 from an iterable of 16 values."""

        m = cls.__new__(cls, object)
        m._m = list(map(float, iterable))
        if len(m._m) != 16:
            raise ValueError("Iterable must have 16 values")
        return m


    @classmethod
    def clone(cls, copy_Matrix44):
        """Creates a Matrix44 that is a copy of another."""

        m = cls.__new__(cls, object)
        m._m = copy_Matrix44._m[:]
        return m


    @classmethod
    def blank(cls):
        """Creates a blank Matrix44 (with no information). This is rarely
        required, you may want to use an identity Matrix44,
        see Matrix44.identity()

        """

        m = cls.__new__(cls, object)
        m._m = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,]
        return m


    @classmethod
    def identity(cls):
        """Creates and identity Matrix44."""

        m = cls.__new__(cls, object)
        m._m = [1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.]
        return m


    @classmethod
    def scale(cls, scale_x, scale_y= None, scale_z= None):
        """Creates a scale Matrix44.
        If one parameter is given the scale is uniform,
        if three parameters are give the scale is different (potentialy) on each x axis.

        """

        m = cls.__new__(cls, object)
        return m.make_scale(scale_x, scale_y, scale_z)


    @classmethod
    def translation(cls, x, y, z):
        """Creates a translation Matrix44 to (x, y, z).

        x -- X Coordinate
        y -- Y Coordinate
        z -- Z Coordinate

        """

        m = cls.__new__(cls, object)
        return m.make_translation(x, y, z)


    @classmethod
    def x_rotation(cls, angle):
        """Creates a Matrix44 that does a rotation about the x axis.

        angle -- Angle of rotation (in radians)

        """

        m = cls.__new__(cls, object)
        return m.make_x_rotation(angle)


    @classmethod
    def y_rotation(cls, angle):
        """Creates a Matrix44 that does a rotation about the y axis.

        angle -- Angle of rotation (in radians)

        """

        m = cls.__new__(cls, object)
        return m.make_y_rotation(angle)


    @classmethod
    def z_rotation(cls, angle):
        """Creates a Matrix44 that does a rotation about the z axis.

        angle -- Angle of rotation (in radians)

        """

        m = cls.__new__(cls, object)
        return m.make_z_rotation(angle)


    @classmethod
    def rotation_about_axis(cls, axis, angle):
        """Creates a Matrix44 that does a rotation about an axis.

        axis -- A vector of the axis
        angle -- Angle of rotation

        """

        m = cls.__new__(cls, object)
        return m.make_rotation_about_axis(axis, angle)


    @classmethod
    def xyz_rotation(cls, angle_x, angle_y, angle_z):
        """Creates a Matrix44 that does a rotation about each axis.

        angle_x -- Angle of rotation, about x
        angle_y -- Angle of rotation, about y
        angle_z -- Angle of rotation, about z

        """

        m = cls.__new__(cls, object)
        return m.make_xyz_rotation(angle_x, angle_y, angle_z)


    @classmethod
    def perspective_projection(cls, left, right, top, bottom, near, far):
        """Creates a Matrix44 that projects points in to 2d space.

        left -- Coordinate of left of screen
        right -- Coordination of right of screen
        top -- Coordination of the top of the screen
        bottom -- Coordination of the borrom of the screen
        near -- Coordination of the near clipping plane
        far -- Coordinate of the far clipping plane

        """

        m = cls.__new__(cls, object)
        return m.make_perspective_projection( left,
                                              right,
                                              top,
                                              bottom,
                                              near,
                                              far)


    @classmethod
    def perspective_projection_fov(cls, fov, aspect, near, far):
        """Creates a Matrix44 that projects points in to 2d space

        fov -- The field of view (in radians)
        aspect -- The aspect ratio of the screen (width / height)
        near -- Coordinate of the near clipping plane
        far -- Coordinate of the far clipping plane

        """

        m = cls.__new__(cls, object)
        return m.make_perspective_projection_fov(fov, aspect, near, far)


    def __str__(self):
        """'Pretty' formatting of the Matrix44."""

        # Pretty printing generates a lot of ugly code - oh the irony!
        # Changed in release 0.0.3 so that the decimal point is always
        # line up on the columns

        cols = [ list(map(format_number, col)) for col in self.columns() ]

        def decimal_pos(n):
            if '.' in n:
                return n.index('.')
            return len(n)

        for col_no, col in enumerate(cols[:]):

            decimal = max( decimal_pos(format_number(c)) for c in col )
            cols[col_no] = [" "*(decimal-decimal_pos(c))+c for c in col]

        max_col_lengths = [ max(len(c) for c in col) for col in cols ]
        rows = [[], [], [], []]
        for row_no in range(4):

            for col_no in range(4):

                v = cols[col_no][row_no]
                rows[row_no].append( v.ljust(max_col_lengths[col_no]) )

        rows = [" ".join(row).rstrip() for row in rows]
        return "\n".join("[ %s ]"%row for row in rows)

        return str(cols)


    def __repr__(self):

        def format_row(row):
            return "(%s)" % ", ".join( format_number(value) for value in row )

        return "Matrix44(%s)" % \
            ", ".join(format_row(row) for row in self.rows())


    def __hash__(self):

        """Allows matrices to be used as keys in a dictionary."""

        return hash(tuple(self._m))


    def __setitem__(self, coord, value):
        """Sets an individual element in the Matrix44.
        coord is a tuple of (row, column)

        eg. Matrix44[2,3] = 3.

        """

        try:
            row, col = coord
            self._m[row * 4 + col] = 1.0 * value
        except IndexError:
            raise IndexError( "Row and Column should be 0, 1, 2 or 3" )
        except TypeError:
            raise TypeError( "Must be a number" )


    def __getitem__(self, coord):
        """Gets an individual element in the Matrix44.
        coord is a tuple of (row, column)

        eg. print Matrix44[2,3]

        """

        try:
            row, col = coord
            return self._m[row * 4 + col]
        except IndexError:
            raise IndexError( "Row and Column should be 0, 1, 2 or 3" )
        except TypeError:
            raise TypeError( "index should be two values containing"\
                            " the row and column" )


    def __iter__(self):
        """Iterates over all 16 values in the Matrix44."""

        return iter(self._m[:])


    def __neg__(self):
        """Returns the inverse of the matrix."""

        return self.get_inverse()


    def __mul__(self, rhs):
        """Returns the result of multiplying this Matrix44 by another, called
        by the * (multiply) operator."""

        m1_0,  m1_1,  m1_2,  m1_3, \
        m1_4,  m1_5,  m1_6,  m1_7, \
        m1_8,  m1_9,  m1_10, m1_11, \
        m1_12, m1_13, m1_14, m1_15 = self._m

        m2_0,  m2_1,  m2_2,  m2_3, \
        m2_4,  m2_5,  m2_6,  m2_7, \
        m2_8,  m2_9,  m2_10, m2_11, \
        m2_12, m2_13, m2_14, m2_15 = rhs._m

        retm =  [ m2_0 * m1_0 + m2_1 * m1_4 + m2_2 * m1_8 + m2_3 * m1_12,
                  m2_0 * m1_1 + m2_1 * m1_5 + m2_2 * m1_9 + m2_3 * m1_13,
                  m2_0 * m1_2 + m2_1 * m1_6 + m2_2 * m1_10 + m2_3 * m1_14,
                  m2_0 * m1_3 + m2_1 * m1_7 + m2_2 * m1_11 + m2_3 * m1_15,

                  m2_4 * m1_0 + m2_5 * m1_4 + m2_6 * m1_8 + m2_7 * m1_12,
                  m2_4 * m1_1 + m2_5 * m1_5 + m2_6 * m1_9 + m2_7 * m1_13,
                  m2_4 * m1_2 + m2_5 * m1_6 + m2_6 * m1_10 + m2_7 * m1_14,
                  m2_4 * m1_3 + m2_5 * m1_7 + m2_6 * m1_11 + m2_7 * m1_15,

                  m2_8 * m1_0 + m2_9 * m1_4 + m2_10 * m1_8 + m2_11 * m1_12,
                  m2_8 * m1_1 + m2_9 * m1_5 + m2_10 * m1_9 + m2_11 * m1_13,
                  m2_8 * m1_2 + m2_9 * m1_6 + m2_10 * m1_10 + m2_11 * m1_14,
                  m2_8 * m1_3 + m2_9 * m1_7 + m2_10 * m1_11 + m2_11 * m1_15,

                  m2_12 * m1_0 + m2_13 * m1_4 + m2_14 * m1_8 + m2_15 * m1_12,
                  m2_12 * m1_1 + m2_13 * m1_5 + m2_14 * m1_9 + m2_15 * m1_13,
                  m2_12 * m1_2 + m2_13 * m1_6 + m2_14 * m1_10 + m2_15 * m1_14,
                  m2_12 * m1_3 + m2_13 * m1_7 + m2_14 * m1_11 + m2_15 * m1_15 ]

        ret = self.__new__(self.__class__, object)
        ret._m = retm

        return ret


    def __imul__(self, rhs):

        """Multiplies this Matrix44 by another, called by the *= operator."""

        m1_0,  m1_1,  m1_2,  m1_3, \
        m1_4,  m1_5,  m1_6,  m1_7, \
        m1_8,  m1_9,  m1_10, m1_11, \
        m1_12, m1_13, m1_14, m1_15 = self._m

        m2_0,  m2_1,  m2_2,  m2_3, \
        m2_4,  m2_5,  m2_6,  m2_7, \
        m2_8,  m2_9,  m2_10, m2_11, \
        m2_12, m2_13, m2_14, m2_15 = rhs._m


        self._m = [ m2_0 * m1_0 + m2_1 * m1_4 + m2_2 * m1_8 + m2_3 * m1_12,
                    m2_0 * m1_1 + m2_1 * m1_5 + m2_2 * m1_9 + m2_3 * m1_13,
                    m2_0 * m1_2 + m2_1 * m1_6 + m2_2 * m1_10 + m2_3 * m1_14,
                    m2_0 * m1_3 + m2_1 * m1_7 + m2_2 * m1_11 + m2_3 * m1_15,

                    m2_4 * m1_0 + m2_5 * m1_4 + m2_6 * m1_8 + m2_7 * m1_12,
                    m2_4 * m1_1 + m2_5 * m1_5 + m2_6 * m1_9 + m2_7 * m1_13,
                    m2_4 * m1_2 + m2_5 * m1_6 + m2_6 * m1_10 + m2_7 * m1_14,
                    m2_4 * m1_3 + m2_5 * m1_7 + m2_6 * m1_11 + m2_7 * m1_15,

                    m2_8 * m1_0 + m2_9 * m1_4 + m2_10 * m1_8 + m2_11 * m1_12,
                    m2_8 * m1_1 + m2_9 * m1_5 + m2_10 * m1_9 + m2_11 * m1_13,
                    m2_8 * m1_2 + m2_9 * m1_6 + m2_10 * m1_10 + m2_11 * m1_14,
                    m2_8 * m1_3 + m2_9 * m1_7 + m2_10 * m1_11 + m2_11 * m1_15,

                    m2_12 * m1_0 + m2_13 * m1_4 + m2_14 * m1_8 + m2_15 * m1_12,
                    m2_12 * m1_1 + m2_13 * m1_5 + m2_14 * m1_9 + m2_15 * m1_13,
                    m2_12 * m1_2 + m2_13 * m1_6 + m2_14 * m1_10 + m2_15 * m1_14,
                    m2_12 * m1_3 + m2_13 * m1_7 + m2_14 * m1_11 + m2_15 * m1_15]

        return self

    def fast_mul(self, rhs):

        """Multiplies this matrix by another. Assumes that both matrices have
        a right column of (0, 0, 0, 1). This is true for matrices composed
        of rotations, translations and scales. fast_mul is approximately 25%
        quicker than the *= operator.

        rhs -- A matrix

        """

        m1_0,  m1_1,  m1_2,  m1_3, \
        m1_4,  m1_5,  m1_6,  m1_7, \
        m1_8,  m1_9,  m1_10, m1_11, \
        m1_12, m1_13, m1_14, m1_15 = self._m

        m2_0,  m2_1,  m2_2,  m2_3, \
        m2_4,  m2_5,  m2_6,  m2_7, \
        m2_8,  m2_9,  m2_10, m2_11, \
        m2_12, m2_13, m2_14, m2_15 = rhs._m


        self._m = [ m2_0 * m1_0 + m2_1 * m1_4 + m2_2 * m1_8,
                    m2_0 * m1_1 + m2_1 * m1_5 + m2_2 * m1_9,
                    m2_0 * m1_2 + m2_1 * m1_6 + m2_2 * m1_10,
                    0.0,

                    m2_4 * m1_0 + m2_5 * m1_4 + m2_6 * m1_8,
                    m2_4 * m1_1 + m2_5 * m1_5 + m2_6 * m1_9,
                    m2_4 * m1_2 + m2_5 * m1_6 + m2_6 * m1_10,
                    0.0,

                    m2_8 * m1_0 + m2_9 * m1_4 + m2_10 * m1_8,
                    m2_8 * m1_1 + m2_9 * m1_5 + m2_10 * m1_9,
                    m2_8 * m1_2 + m2_9 * m1_6 + m2_10 * m1_10,
                    0.0,

                    m2_12 * m1_0 + m2_13 * m1_4 + m2_14 * m1_8 + m1_12,
                    m2_12 * m1_1 + m2_13 * m1_5 + m2_14 * m1_9 + m1_13,
                    m2_12 * m1_2 + m2_13 * m1_6 + m2_14 * m1_10 + m1_14,
                    1.0 ]

        return self

    def copy(self):
        """Returns a copy of this matrix."""
        return self.clone(self)
    __copy__ = copy


    def components(self):
        """Returns an iterator for the components in the Matrix44. ie
        returns all 16 values."""

        return iter(self._m[:])


    def transposed_components(self):
        """Returns an iterator for the components in the Matrix44 in
        transposed order."""

        m00, m01, m02, m03, \
        m10, m11, m12, m13, \
        m20, m21, m22, m23, \
        m30, m31, m32, m33 = self._m

        return iter( ( m00, m10, m20, m30,
                       m01, m11, m21, m31,
                       m02, m12, m22, m32,
                       m03, m13, m23, m33 ) )


    def rows(self):
        """Returns an iterator for the rows in the Matrix44 (yields 4 tuples
        of 4 values)."""

        m = self._m
        return iter(( tuple(m[0:4]),
                      tuple(m[4:8]),
                      tuple(m[8:12]),
                      tuple(m[12:16]) ))



    def columns(self):
        """Returns an iterator for the columns in the Matrix44 (yields 4
        tuples of 4 values)."""

        col = self.get_column
        return iter((col(0), col(1), col(2), col(3)))



    def get_row_vec3(self, row_no):
        """Returns a Vector3 for a given row.

        row_no -- The row index

        """

        try:
            r = row_no*4
            x, y, z = self._m[r:r+3]
            return Vector3.from_floats(x, y, z)
        except IndexError:
            raise IndexError( "Row and Column should be 0, 1, 2 or 3" )


    def get_column(self, col_no):
        """Returns a column as a tuple of 4 values.

        col_no -- The column index

        """

        try:
            m = self._m
            return ( m[col_no],
                     m[col_no+4],
                     m[col_no+8],
                     m[col_no+12] )
        except IndexError:
            raise IndexError( "Column should be 0, 1, 2 or 3" )


    def set_row(self, row_no, row):
        """Sets the values in a row.

        row_no -- The index of the row
        row -- An container containing the new values

        """

        try:
            self._setters[row_no](self, row)
        except IndexError:
            raise IndexError( "Row should be 0, 1, 2 or 3" )


    def set_column(self, col_no, col):
        """Sets the values in a column.

        col_no -- The index of the column
        col -- An sequence of 4 values

        """

        try:
            col_iter = iter(col)
            m = self._m
            a, b, c, d = col
            m[col_no] = float(a)
            m[col_no+4] = float(b)
            m[col_no+8] = float(c)
            m[col_no+12] = float(d)

        except IndexError:
            raise IndexError( "Column should be 0, 1, 2 or 3" )


    def transform_vec3(self, v):
        """Transforms a vector and returns the result as a Vector3.

        v -- Vector to transform

        """

        m = self._m
        x, y, z = v
        return Vector3.from_floats( x * m[0] + y * m[4] + z * m[8]  + m[12],
                                    x * m[1] + y * m[5] + z * m[9]  + m[13],
                                    x * m[2] + y * m[6] + z * m[10] + m[14] )

    def transform(self, v):
        """Transforms a Vector3 and returns the result as a tuple.

        v -- Vector to transform

        """

        m = self._m
        x, y, z = v
        return ( x * m[0] + y * m[4] + z * m[8]  + m[12],
                 x * m[1] + y * m[5] + z * m[9]  + m[13],
                 x * m[2] + y * m[6] + z * m[10] + m[14] )


    def transform4(self, v):
        """Transforms a 4d vector and returns the result as a tuple.

        v -- Vector to transform

        """

        m = self._m
        x, y, z, w = v
        return ( x * m[0] + y * m[4] + z * m[8]  + w * m[12],
                 x * m[1] + y * m[5] + z * m[9]  + w * m[13],
                 x * m[2] + y * m[6] + z * m[10] + w * m[14] )


    def transform_sequence(self, points):

        m_0,  m_1,  m_2,  m_3, \
        m_4,  m_5,  m_6,  m_7, \
        m_8,  m_9,  m_10, m_11, \
        m_12, m_13, m_14, m_15 = self._m

        return [ ( x * m_0 + y * m_4 + z * m_8  + m_12,
                   x * m_1 + y * m_5 + z * m_9  + m_13,
                   x * m_2 + y * m_6 + z * m_10 + m_14 )
                   for x,y,z in points ]


    def transform_sequence_vec3(self, points):

        m_0,  m_1,  m_2,  m_3, \
        m_4,  m_5,  m_6,  m_7, \
        m_8,  m_9,  m_10, m_11, \
        m_12, m_13, m_14, m_15 = self._m

        return [ Vector3.from_floats
                 ( x * m_0 + y * m_4 + z * m_8  + m_12,
                   x * m_1 + y * m_5 + z * m_9  + m_13,
                   x * m_2 + y * m_6 + z * m_10 + m_14 )
                   for x,y,z in points ]


    def iter_transform_vec3(self, points):

        """Transforms a sequence of points, and yields the result as Vector3s

        points -- A sequence of vectors

        """

        m_0,  m_1,  m_2,  m_3, \
        m_4,  m_5,  m_6,  m_7, \
        m_8,  m_9,  m_10, m_11, \
        m_12, m_13, m_14, m_15 = self._m

        for x, y, z in points:

            yield Vector3.from_floats( x * m_0 + y * m_4 + z * m_8  + m_12,
                                       x * m_1 + y * m_5 + z * m_9  + m_13,
                                       x * m_2 + y * m_6 + z * m_10 + m_14 )


    def iter_transform(self, points):

        """Transforms a sequence of points and yields the result as tuples.

        points -- A sequence of vectors

        """

        m_0, m_1, m_2, m_3, \
        m_4, m_5, m_6, m_7, \
        m_8, m_9, m_10, m_11, \
        m_12, m_13, m_14, m_15 = self._m

        for x, y, z in points:

            yield ( x * m_0 + y * m_4 + z * m_8  + m_12,
                    x * m_1 + y * m_5 + z * m_9  + m_13,
                    x * m_2 + y * m_6 + z * m_10 + m_14 )

    iter_transform3 = iter_transform


    def iter_transform4(self, points):

        """Transforms a sequence of points and yields the result as tuples.

        points -- A sequence of vectors

        """

        m_0, m_1, m_2, m_3, \
        m_4, m_5, m_6, m_7, \
        m_8, m_9, m_10, m_11, \
        m_12, m_13, m_14, m_15 = self._m

        for x, y, z, w in points:

            yield ( x * m_0 + y * m_4 + z * m_8  + w * m_12,
                    x * m_1 + y * m_5 + z * m_9  + w * m_13,
                    x * m_2 + y * m_6 + z * m_10 + w * m_14 )


    def rotate_vec3(self, v):
        """Rotates a Vector3 and returns the result.
        The translation part of the Matrix44 is ignored.

        v -- Vector to rotate

        """

        m = self._m
        x, y, z = v
        return Vector3.from_floats( x * m[0] + y * m[4] + z * m[8],
                                    x * m[1] + y * m[5] + z * m[9],
                                    x * m[2] + y * m[6] + z * m[10] )


    def rotate(self, v):
        """Rotates a Vector3 and returns the result as a tuple
        The translation part of the Matrix44 is ignored.

        v -- Vector to rotate

        """

        m = self._m
        x, y, z = v
        return ( x * m[0] + y * m[4] + z * m[8],
                 x * m[1] + y * m[5] + z * m[9],
                 x * m[2] + y * m[6] + z * m[10] )


    def inverse_transform(self, v):
        """Inverse trasforms a Vector3 and returns the result.
        Warning: This is expensive, pre-calculate an inverse Matrix44 if you
        can.

        v -- Vector to transform

        """

        return self.get_inverse().transform(v)


    def make_identity(self):
        """Makes an identity Matrix44."""

        self._m = [1., 0., 0., 0.,
                   0., 1., 0., 0.,
                   0., 0., 1., 0.,
                   0., 0., 0., 1.]
        return self


    def make_copy(self, other):
        """Makes a copy of another Matrix44."""

        self._m = other._m[:]
        return self


    def make_scale(self, scale_x, scale_y= None, scale_z= None):
        """Makes a scale Matrix44.

        If the scale_y and scale_z parameters are not given they default to the same as scale_x.

        """
        if scale_y is None:
            scale_y = scale_x
        if scale_z is None:
            scale_z = scale_x

        self._m =   [float(scale_x), 0.,             0.,             0.,
                     0.,             float(scale_y), 0.,             0.,
                     0.,             0.,             float(scale_z), 0.,
                     0.,             0.,             0.,             1.]
        return self


    def make_translation(self, x, y, z):
        """Makes a translation Matrix44."""

        self._m =   [1.,       0.,       0.,       0.,
                     0.,       1.,       0.,       0.,
                     0.,       0.,       1.,       0.,
                     float(x), float(y), float(z), 1.]
        return self


    def make_x_rotation(self, angle):
        """Makes a rotation Matrix44 around the x axis."""

        cos_a = cos(angle)
        sin_a = sin(angle)

        self._m =  [1.,  0.,      0.,     0.,
                    0.,  cos_a,   sin_a,  0.,
                    0., -sin_a,   cos_a,  0.,
                    0.,  0.,      0.,     1.]
        return self

    def make_y_rotation(self, angle):
        """Makes a rotation Matrix44 around the y axis."""

        cos_a = cos(angle)
        sin_a = sin(angle)

        self._m =  [ cos_a,  0., -sin_a,  0.,
                     0.,     1.,  0.,     0.,
                     sin_a,  0.,  cos_a,  0.,
                     0.,     0.,  0.,     1.]
        return self


    def make_z_rotation(self, angle):
        """Makes a rotation Matrix44 around the z axis."""

        cos_a = cos(angle)
        sin_a = sin(angle)

        self._m =  [  cos_a,   sin_a,  0.,  0.,
                     -sin_a,   cos_a,  0.,  0.,
                      0.,      0.,     1.,  0.,
                      0.,      0.,     0.,  1.]
        return self


    def make_rotation_about_axis(self, axis, angle):
        """Makes a rotation Matrix44 around an axis.

        axis -- An iterable containing the axis (three values)
        angle -- The angle to rotate (in radians)

        """

        c = cos(angle)
        s = sin(angle)
        omc = 1. - c
        x, y, z = axis

        self._m = [x*x*omc+c,   y*x*omc+z*s, x*z*omc-y*s, 0.,
                   x*y*omc-z*s, y*y*omc+c,   y*z*omc+x*s, 0.,
                   x*z*omc+y*s, y*z*omc-x*s, z*z*omc+c,   0.,
                   0.,          0.,          0.,          1.]
        return self


    def make_xyz_rotation(self, angle_x, angle_y, angle_z):
        """Makes a rotation Matrix44 about 3 axis."""

        cx = cos(angle_x)
        sx = sin(angle_x)
        cy = cos(angle_y)
        sy = sin(angle_y)
        cz = cos(angle_z)
        sz = sin(angle_z)

        sxsy = sx*sy
        cxsy = cx*sy

        # http://web.archive.org/web/20041029003853/http:/www.j3d.org/matrix_faq/matrfaq_latest.html#Q35
        #A = cos(angle_x)
        #B = sin(angle_x)
        #C = cos(angle_y)
        #D = sin(angle_y)
        #E = cos(angle_z)
        #F = sin(angle_z)

    #     |  CE      -CF       D   0 |
    #M  = |  BDE+AF  -BDF+AE  -BC  0 |
    #     | -ADE+BF   ADF+BE   AC  0 |
    #     |  0        0        0   1 |

        self._m = [ cy*cz,  sxsy*cz+cx*sz,  -cxsy*cz+sx*sz, 0.,
                    -cy*sz, -sxsy*sz+cx*cz, cxsy*sz+sx*cz,  0.,
                    sy,     -sx*cy,         cx*cy,          0.,
                    0.,     0.,             0.,             1.]

        return self


    def make_perspective_projection(self, left, right, top, bottom, near, far):
        """Makes a perspective projection Matrix44.

        left -- Coordinate of left of screen
        right -- Coordination of right of screen
        top -- Coordination of the top of the screen
        bottom -- Coordination of the borrom of the screen
        near -- Coordination of the near clipping plane
        far -- Coordinate of the far clipping plane

        """

        self._m = [(2.*near)/(right-left),    0.,                        0.,                          0.,
                   0.,                        (2.*near)/(top-bottom),    0.,                          0.,
                   (right+left)/(right-left), (top+bottom)/(top-bottom), -((far+near)/(far-near)),   -1.,
                   0.,                        0.,                        -((2.*far*near)/(far-near)), 0.]
        return self


    def make_perspective_projection_fov(self, fov, aspect, near, far):
        """Creates a Matrix44 that projects points in to 2d space

        fov -- The field of view (in radians)
        aspect -- The aspect ratio of the screen (width / height)
        near -- Coordinate of the near clipping plane
        far -- Coordinate of the far clipping plane

        """

        assert fov < pi, "The field of view should be less than pi radians"\
        " (180 degrees)"

        range = near*tan(fov/2.);
        left = -range*aspect
        right = range*aspect
        bottom = -range
        top = range

        #right = tan( fov/2. ) * near
        #left = - right
        #top = right / aspect
        #bottom = -top
        self.make_perspective_projection(left, right, bottom, top, near, far)
        return self


    def transpose(self):
        """Swaps the rows for columns."""

        m00, m01, m02, m03, \
        m10, m11, m12, m13, \
        m20, m21, m22, m23, \
        m30, m31, m32, m33 = self._m

        self._m = [ m00, m10, m20, m30,
                    m01, m11, m21, m31,
                    m02, m12, m22, m32,
                    m03, m13, m23, m33 ]


    def get_transpose(self):
        """Returns a Matrix44 that is a copy of this, but with rows and
        columns swapped."""

        m00, m01, m02, m03, \
        m10, m11, m12, m13, \
        m20, m21, m22, m23, \
        m30, m31, m32, m33 = self._m

        ret = self.__new__(self.__class__, object)

        ret._m = [ m00, m10, m20, m30,
                   m01, m11, m21, m31,
                   m02, m12, m22, m32,
                   m03, m13, m23, m33 ]

        return ret


    def get_inverse_rot_trans(self):
        """Returns the inverse of a Matrix44 with only rotation and
        translation. This is faster than the general get_inverse method."""

        ret = self.copy()
        m = ret._m

        i0,  i1,  i2,  i3, \
        i4,  i5,  i6,  i7, \
        i8,  i9,  i10, i11, \
        i12, i13, i14, i15 = self._m

        m[1] = i4
        m[4] = i1
        m[2] = i8
        m[8] = i2
        m[6] = i9
        m[9] = i6

        m[12] = ( m[0] * -i12 +
                  m[4] * -i13 +
                  m[8] * -i14 )

        m[13] = ( m[1] * -i12 +
                  m[5] * -i13 +
                  m[9] * -i14 )

        m[14] = ( m[2] * -i12 +
                  m[6] * -i13 +
                  m[10] * -i14 )

        return ret


    def get_inverse(self):

        """Returns the inverse (matrix with the opposite effect) of this
        matrix."""

        ret = self.__new__(self.__class__, object)
        i = self._m

        i0,  i1,  i2,  i3, \
        i4,  i5,  i6,  i7, \
        i8,  i9,  i10, i11, \
        i12, i13, i14, i15 = i

        negpos=[0., 0.]
        temp = i0 * i5 * i10
        negpos[temp > 0.] += temp

        temp = i1 * i6 * i8
        negpos[temp > 0.] += temp

        temp = i2 * i4 * i9
        negpos[temp > 0.] += temp

        temp = -i2 * i5 * i8
        negpos[temp > 0.] += temp

        temp = -i1 * i4 * i10
        negpos[temp > 0.] += temp

        temp = -i0 * i6 * i9
        negpos[temp > 0.] += temp

        det_1 = negpos[0]+negpos[1]

        if (det_1 == 0.) or (abs(det_1 / (negpos[1] - negpos[0])) < \
                             (2. * 0.00000000000000001) ):
            raise Matrix44Error("notivertable", "This Matrix44 can not be inverted")

        det_1 = 1. / det_1

        ret._m = [ (i5*i10 - i6*i9)*det_1,
                  -(i1*i10 - i2*i9)*det_1,
                   (i1*i6 - i2*i5 )*det_1,
                   0.0,
                  -(i4*i10 - i6*i8)*det_1,
                   (i0*i10 - i2*i8)*det_1,
                  -(i0*i6 - i2*i4)*det_1,
                   0.0,
                  (i4*i9 - i5*i8 )*det_1,
                  -(i0*i9 - i1*i8)*det_1,
                   (i0*i5 - i1*i4)*det_1,
                   0.0,
                   0.0, 0.0, 0.0, 1.0 ]

        m = ret._m
        m[12] = - ( i12 * m[0] + i13 * m[4] + i14 * m[8] )
        m[13] = - ( i12 * m[1] + i13 * m[5] + i14 * m[9] )
        m[14] = - ( i12 * m[2] + i13 * m[6] + i14 * m[10] )

        return ret


    def invert(self):

        """Inverts this matrix."""

        self._m[:] = self.get_inverse()._m


    def move(self, forward=None, right=None, up=None):

        """Changes the translation according to a direction vector.
        To move in opposite directions (i.e back, left and down), first
        negate the vector.

        forward -- Units to move in the 'forward' direction
        right -- Units to move in the 'right' direction
        up -- Units to move in the 'up' direction

        """

        if forward is not None:
            self.translate = Vector3(self.translate) + \
                Vector3(self.forward) * forward

        if right is not None:
            self.translate = Vector3(self.translate) + \
                Vector3(self.right) * right

        if up is not None:
            self.translate = Vector3(self.translate) + \
                Vector3(self.up) * up



def test():

    m = Matrix44.xyz_rotation(radians(45), radians(20), radians(0))

    #m.translate += (1, 2, 3)
    print(m.right)
    print(m.right.as_vec3())

    n = m.copy()

    r = Matrix44.z_rotation(radians(32))
    m *= r
    print(m)
    n.fast_mul( r )

    print(n)

    print("--Transpose")

    print(m.get_transpose())

    print("--")

    print(m.get_row(2))

    m.transpose()
    print(m)

    print()

    #print (10, 20, 30) + Vector3(1,2,3)

    m.translate = (m.translate[:3]) + Vector3(10, 20, 30)
        

    print(m)

    print()

    v = (1., 2., 3.)
    print(v)
    vt = m.transform(v)
    print(vt)

    vit = m.get_inverse().transform(vt)

    print(vit)


    print(m.inverse_transform(vt))
    m[1,2] = 3.

    print()

    print(m.x_axis)
    print(m.translate)
    m.translate = (1, 2, 3)

    print(m)

    identity = Matrix44()
    #identity.set_row(0, (1, 2, 3, 4))
    print(identity)

    identity[3, 1] = 456
    #identity *= Matrix44.scale(20.32, 764.2323, -23)

    print(identity)
    print(eval(repr(identity)))

    print(m)

    print(m.translate + Vector3(1, 2, 3))

    print(m)

    m.translate = (0, 0, 0)

if __name__ == "__main__":

    test()
