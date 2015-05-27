
from .locals import WRAP_REPEAT, WRAP_CLAMP, WRAP_ERROR
from .util import saturate

class Grid(object):

    def __init__( self,  node_factory,
                         width,
                         height,
                         x_wrap = WRAP_ERROR,
                         y_wrap = WRAP_ERROR ):

        """Create a grid object.

        node_factory -- Callable that takes the x and y coordinate of the node
        and returns a node object. x_wrap and y_wrap parameters should be
        one of (WRAP_REPEAT, WRAP_CLAMP, WRAP_ERROR).

        width -- Width of the grid.
        height -- Height of the grid.
        x_wrap -- How to handle out of range x coordinates
        y_wrap -- How to handle out of range y coordinates

        """

        self.node_factory = node_factory
        self.width = width
        self.height = height

        self.nodes = [ [node_factory(x, y) for x in range(width)] \
                                           for y in range(height)]

        self._x_wrap = x_wrap
        self._y_wrap = y_wrap

        self._wrap_functions = [ self._make_wrap(self._x_wrap, self.width),
                                 self._make_wrap(self._y_wrap, self.height) ]


    def _get_x_wrap(self):
        return self._x_wrap
    def _set_x_wrap(self, x_wrap):
        self._x_wrap = x_wrap
        self._wrap_functions[0] = self._make_wrap(x_wrap, self.width)
    x_wrap = property(_get_x_wrap, _set_x_wrap, None, "X wrap")

    def _get_y_wrap(self):
        return self._y_wrap
    def _set_y_wrap(self, y_wrap):
        self._y_wrap = y_wrap
        self._wrap_functions[1] = self._make_wrap(y_wrap, self.height)
    y_wrap = property(_get_y_wrap, _set_y_wrap, None, "Y wrap")


    def _make_wrap(self, wrap, edge):

        if wrap == WRAP_NONE:
            def do_wrap(value):
                return value

        elif wrap == WRAP_REPEAT:
            def do_wrap(value):
                return value % edge

        elif wrap == WRAP_CLAMP:
            def do_wrap(value):
                if value < 0:
                    return 0
                if value >= edge:
                    value = edge
                return value

        elif wrap == WRAP_ERROR:
            def do_wrap(value):
                if value < 0 or value >= edge:
                    raise IndexError("coordinate out of range")

        else:
            raise ValueError("Unknown wrap mode")

        return do_wrap


    def wrap(self, coord):

        x, y = coord
        wrap_x, wrap_y = self._wrap_functions
        return ( wrap_x(x), wrap_y(y) )


    def wrap_x(self, x):
        """Wraps an x coordinate.

        x -- X Coordinate

        """

        return self._wrap_functions[0](x)

    def wrap_y(self, y):
        """Wraps a y coordinate.

        y -- Y Coordinate.

        """

        return self._wrap_functions[1](y)


    def get_size(self):

        """Retrieves the size of the grid as a tuple (width, height)."""

        return self.width, self.height


    def __getitem__(self, coord):

        x, y = coord

        if isinstance(x, slice) or isinstance(y, slice):
            if isinstance(x, slice):
                x_indices = x.indices(self.width)
            else:
                x_indices = [x]

            if isinstance(y, slice):
                y_indices = y.indices(self.height)
            else:
                y_indices = [y]

            try:
                wrap_x, wrap_y = self._wrap_functions

                ret = []

                for y_index in range(*y_indices):
                    nodes_y = self.nodes[ wrap_y(y_index) ]

                    for x_index in range(*x_indices):
                        ret.append( nodes_y[ wrap_x(x_index) ] )

            except IndexError:
                raise IndexError("Slice out of range")

            return ret


        x, y = self.wrap(coord)

        if x < 0 or y < 0:
            raise IndexError("coordinate out of range")

        try:
            return self.nodes[y][x]
        except IndexError:
            raise IndexError("coordinate out of range")


    def __iter__(self):

        for row in self.nodes:
            for node in row:
                yield node


    def __contains__(self, value):

        for row in self.nodes:
            if node in row:
                return True

        return False


    def clear(self):

        """Resets the grid."""

        node_factory = self.node_factory

        self.nodes[:] = [ [node_factory(x, y) for x in range(width)] \
                                              for y in range(height)]


    def get(self, coord, default=None):

        """Retrieves a node from the grid.

        coord -- Coordinate to retrieve
        default -- Default value to use if coord is out of range

        """

        x, y = self.wrap(coord)

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            if default is not None:
                return default
            else:
                raise IndexError("coordinate out of range")

        return self.nodes[y][x]


    def get_nodes(self, coord, size, wrap=False):

        width = self.width
        height = self.height

        x1, y1 = coord
        x1 = saturate(x1, 0, width)
        y1 = saturate(y1, 0, height)
        w, h = size
        x2, y2 = (x+w, y+h)
        x = saturate(x, 0, width)
        y = saturate(y, 0, height)

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        wrap_x, wrap_y = self._wrap_functions

        nodes = self.nodes
        return [self.nodes[y_coord][x1:x2] for y_coord in range(y1, y2)]




if __name__ == "__main__":

    class Square(object):
        def __init__(self, x, y):
            self.coord = (x, y)
        def __str__(self):
            return str(self.coord)
        def __repr__(self):
            return str(self.coord)

    g = Grid(Square, 100, 100, x_wrap = WRAP_REPEAT)

    for square in g:
        print(str(square))

    print(g[10:20, 10:20])
    print(g.get_nodes((-2, 0), (5, 5)))
