# from svglib.svglib import load_svg_file
from svg2heavym.svg_read import Svg2HMRenderer


sv = Svg2HMRenderer('hm-examples/grouped.svg')
print(sv.get_hm_shapes())