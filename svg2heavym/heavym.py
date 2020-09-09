#!/usr/bin/env python

import svgelements as svge
from defusedxml.ElementTree import parse
from xml.etree.ElementTree import ElementTree, Element as xmlElement, SubElement, tostring


class HmlGroup:
    def __init__(self, svg_element):
        self.data = {
            "color": "#ffffff",
            "id": svg_element.get('id'),
            "name": svg_element.get('name'),
            "groupPlayers": "0"
        }
        self.group_node = xmlElement('group', self.data)
        self.faces_node = xmlElement('faces')

    def add_face(self, hml_face):
        self.faces_node.append(hml_face)


class HmlFace:
    def __init__(self, svg_element):
        self.data = {
            "deltaX": "0",
            "deltaY": "0",
            "type": svg_element.get('type'),
            "id": svg_element.get('id'),
            "isMask": "0",
            "name": svg_element.get('name'),
            "isVisible": "1",
            "isLocked": "0"
        }
        self.xml_node = xmlElement('face', self.data)

    def add_point(self, x, y):
        self.xml_node.append(xmlElement('point', {"x": x, "y": y}))


class SvgElement:
    def __init__(self, values=None, svge=None):
        self.values = values
        self.svge = svge
        self.element_type = type(self).__name__

    def get(self, k):
        return self.values[k]

    def set(self, k, v):
        self.values[k] = v
        return self.values[k]

    def __repr__(self):
        return f'{self.element_type} Element(Values={self.values})'


class SvgEllipse(SvgElement):
    def __repr__(self):
        return f'SvgEllipse (Values={self.values})'


class SvgRect(SvgElement):
    def __repr__(self):
        return f'Rectangle (Values={self.values})'


class SvgTriangle(SvgElement):
    def __repr__(self):
        return f'SvgTriangle (Values={self.values})'


class SvgPolygon(SvgElement):
    def __repr__(self):
        return f'SvgPolygon (Values={self.values})'


class SvgElementFactory:
    def __init__(self, node):
        self.values = node.attrib
        self.tag = node.tag

    def build(self):
        if self.tag == 'ellipse':
            return SvgEllipse(values=self.values, svge=svge.Ellipse(self.values))
        elif self.tag == 'rect':
            return SvgRect(values=self.values, svge=svge.Rect(self.values))
        elif self.tag == 'polygon':
            if self.values['points'].count(" ") > 7:
                return SvgPolygon(values=self.values, svge=svge.Polygon(self.values))
            else:
                return SvgTriangle(values=self.values, svge=svge.Polygon(self.values))
        else:
            return None


class SvgGroup(SvgElement):
    def __init__(self, values=None):
        super().__init__(values=values)
        self.elements = []

    def __repr__(self):
        return_value = f'SvgGroup {self.values["id"]}\n'
        for el in self.elements:
            return_value += f'/t{el}'
        return return_value

    def add_element(self, element):
        self.elements.append(element)

    def id(self):
        return self.get('id')


class SvgDocument:
    def __init__(self):
        self.groups = {}

    def group(self, group_id=None, values=None):
        if group_id and group_id in self.groups:
            return self.groups.get(group_id)
        if 'id' in values:
            new_group = SvgGroup(values=values)
            self.groups[new_group.id()] = new_group
            return new_group

    def add_element(self, group_id=None, element=None):
        self.group(group_id=group_id).add_element(element)


class Converter:
    def __init__(self, svg=None, hm=None):
        self.document = None
        self.svg_path = svg
        self.heavym_path = hm
        self.next_face_id = 0
        self.next_group_id = 0

    def parse_svg(self):
        group = None
        svg_iter = svge.SVG.svg_structure_parse(self.svg_path)
        self.document = SvgDocument()
        for event, node in svg_iter:
            if event == 'start':
                if node.tag == 'g':
                    group = self.document.group(values=node.attrib)
                else:
                    el = SvgElementFactory(node).build()
                    if isinstance(el, SvgElement):
                        el.set('group_id', group.get('id'))
                        group.add_element(el)
        return self.document

    def parse_heavym(self):
        tree = parse(self.heavym_path)
        root = tree.getroot()
        groups_root = root.find('sequence').find('groups')
        groups = root.findall("./sequence/groups/group")
        self.next_group_id = max(list(map(lambda x: int(x.get('id')), groups))) + 1
        faces = root.findall(".//groups/group/faces/face")
        self.next_face_id = max(list(map(lambda x: int(x.get('id')), faces))) + 1


svg_path = '/Users/sheller/Dev/HeavyM/svg2heavym/hm-examples/layers-with-view.svg'
hm_path = '/Users/sheller/Dev/HeavyM/svg2heavym/hm-examples/existing-groups.hm'
# result = Converter().parse(svg_path)
Converter(hm=hm_path, svg=svg_path).parse_heavym()
