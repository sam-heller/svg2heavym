"""Library to insert SVG files into an Existing HeavyM Scene (https://heavym.net)

Reading is handled by a wrapper around svglib (https://github.com/deeplook/svglib), essentially reducing conversion
tasks to the bare minimum needed.
"""
from svglib.svglib import SvgRenderer, Svg2RlgShapeConverter, Svg2RlgAttributeConverter, NodeTracker


class Svg2HMRenderer(SvgRenderer):
    """
    Significantly paired down extension of the base svglib.SvgRenderer class.
    Avoids as much of the ReportLab tasks as possible. Restricts shapes handled
    to polygons and circles, and saves to a custom HMShape object.
    """

    def __init__(self, path):
        super().__init__(path, color_converter=None, parent_svgs=None)
        self.attrConverter = Svg2HmAttributeConverter(color_converter=None)
        self.shape_converter = Svg2HmShapeConverter(path, self.attrConverter)
        self.handled_shapes = ['rect', 'circle', 'ellipse', 'polygon', 'result']
        self.groups = []

    def render(self, svg_node):
        node = NodeTracker(svg_node)
        main_group = self.renderSvg(node, outermost=True)
        for node in main_group.getContents():
            if type(node).__name__ == "Group":
                current_group = []
                for item in node.contents:
                    current_group.append(HMShape(item))
                self.groups.append(current_group)

    def shapes(self):
        return self.groups


class HMShape:
    """
    Model for holding shapes to be imported into HeavyM
    """

    def __init__(self, shape_data):
        self.shape_data = shape_data
        self.original_name = type(shape_data).__name__.lower()

    @property
    def points(self) -> list:
        return self.shape_data.points

    @property
    def shape_id(self) -> int:
        if self.original_name in ['rectangle', 'square', 'polygon']:
            return 1
        elif self.original_name in ['ellipse, circle']:
            return 3
        else:
            return 0

    @property
    def shape_name(self) -> str:
        if self.original_name in ['rectangle', 'square']:
            return 'square'
        elif self.original_name in ['ellipse, circle']:
            return 'circle'
        elif self.original_name == 'polygon':
            if len(self.points) == 6:
                return 'triangle'
            else:
                return 'polygon'
        else:
            return 'unknown'


class Svg2HmAttributeConverter(Svg2RlgAttributeConverter):
    """
    No styling or attributes are being imported, this overrides the
    standard attribute converter to make sure they don't accidentally
    get caught up in the mix
    """

    def convertColor(self, *args): return None

    def convertFontFamily(self, *args): return ''

    def convertOpacity(self, *args): return float(1)


class Svg2HmShapeConverter(Svg2RlgShapeConverter):
    """
    No images included in HeavyM Scene Config
    """

    def convertImage(self, *args): return None
