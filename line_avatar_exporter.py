import os, sys, re, imghdr, shutil
from PIL import Image

cache_file_pattern = r'^[0-9a-fA-F]+$'
cache_file_re = re.compile( cache_file_pattern )
dest = {
	'small': 'small/',
	'medium': 'medium/',
	'large': 'large/',
}
extension_dict = {
	'rgb' : 'rgb',
	'gif' : 'gif',
	'pbm' : 'pbm',
	'pgm' : 'pgm',
	'ppm' : 'ppm',
	'tiff': 'tiff',
	'rast': 'rast',
	'xbm' : 'xbm',
	'jpeg': 'jpg',
	'bmp' : 'bmp',
	'png' : 'png',
}

def main():
	line_root = os.path.join( os.getenv('localappdata'), r'Line\Cache' )
	copy_cnt = 0
	for size_path in dest:
		if not os.path.isdir(size_path):
			os.makedirs(size_path)
	for cache_basedir, fname, imgname in get_cache_files( line_root ):
		if imgname and (not os.path.isfile(imgname)) and shutil.copy2( os.path.join(cache_basedir, fname), imgname ):
			copy_cnt += 1
	print( 'Copied {} files from "{}".'.format(copy_cnt, line_root) )
	input()

def get_cache_files( line_root ):
	for root, _, files in os.walk(line_root):
		yield from ( detect_img_filepath(root, f) for f in files if cache_file_re.match(f) )

def detect_img_filepath( root, fname ):
	try:
		filepath = os.path.join(root, fname)
		ext = extension_dict[imghdr.what( filepath )]
		w, h = Image.open( filepath ).size
		if w<400 and h<400:
			img_dir = dest['small']
		elif w<1000 and h<1000:
			img_dir = dest['medium']
		else: img_dir = dest['large']
		return (root, fname, img_dir+fname+'.'+ext)
	except KeyError:
		print( '"{}" isn\'t image.'.format(os.path.join(root, fname) ) )
		return (root, fname, None)

if __name__ == "__main__":
	main()
