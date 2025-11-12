from utils.scene_generator import generate_scene_with_trace

code = """
numbers = [1, 2, 3]
for n in numbers:
    print(n)
"""

scene = generate_scene_with_trace(code)

for s in scene:
    print(s)
