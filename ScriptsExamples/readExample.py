import re, os
def read_file(file):
	framesValue = {}
	pattern = re.compile("(\d+) (\d+)")
	
	fileStream = open(file)
	for line in fileStream:
		match = pattern.match(line)
		if not match is None:
			framesValue[match.group(1)] = match.group(2)
	return framesValue
			
def worker():
	files = os.listdir(objects_path)
	for file in files:
		if os.path.isfile(file):
			ob = bpy.data.objects[os.path.basename(file)]
			bpy.context.scene.objects.active = ob
			framesValues = read_file(file)
			for frame in framesValues:
				bpy.context.scene.frame_set(int(frame))
				ob.modifiers[0].thickness = int(framesValues[frame])
				ob.modifiers[0].keyframe_insert(data_path="thickness")