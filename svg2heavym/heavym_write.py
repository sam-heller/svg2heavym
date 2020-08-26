import pprint

from defusedxml.ElementTree import parse
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring


pp = pprint.PrettyPrinter(indent=4)
tree = parse('hm-examples/polygons.hm')
root = tree.getroot()
grp = root.find("./sequence/groups/group[@name='Group 1']")
grp.find("./faces/face[@id  = max(./faces/face/@id)]")

faces = root.find("./sequence/groups/group[@name='Group 1']/faces")
str = tostring(faces)
print(f"{str}")


group = root.find("./sequence/groups/group[@name='Group 1']")


group = root.find("./sequences/groups/group[@name='Group 1']")


max(list(map(lambda x: int(x.get('id')), all)))



root.findAll("./sequence/groups/group[@name='Group 1']/faces/face")

groups = root.findall("./sequence/groups/group")
id = max(list(map(lambda x: int(x.get('id')) + 1, groups)))
print(id)


#
# newFace = SubElement(faces, {'isLocked': '0', 'type': 1, 'id': 0, 'name': 'face 1', 'isVisible': 1, 'deltaX': 0, 'deltaY': 0} )
# point1 = SubElement(newFace, 'point', {'x':"152.26", 'y':'156.695'})
# newFace.append()


# SubElement()
# NewFace = SubElement(faces, 'face', isLocked="0", isMask="0", type="1", id="1", name="Face 2", isVisible="1", deltaX="0", deltaY="0")
# NewFace = SubElement(faces, 'point', x="1526.26", y="156.695")




root.find("./sequence/groups/group/faces/face[@id = max ./sequences/groups/group/faces/")