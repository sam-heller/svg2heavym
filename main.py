from svglib.svglib import load_svg_file
from svg2heavym.svg import Svg2HMRenderer

fpath = 'hm-examples/ellipse.svg'
# fpath = 'hm-examples/heavym-logo.svg'
svg_root = load_svg_file(fpath)
renderer = Svg2HMRenderer(fpath)
renderer.render(svg_root)
out = renderer.shapes()


print('done')
# for group in out:
#     for shape in group:
#         print(shape)
