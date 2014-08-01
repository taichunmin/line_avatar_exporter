import os, sys, re, imghdr, shutil

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
	for cache_basedir, fname, imgname in get_cache_files( line_root ):
		if imgname and (not os.path.isfile(imgname)) and shutil.copy2( os.path.join(cache_basedir, fname), imgname ):
			copy_cnt += 1
	print( 'Copied {} files from "{}".'.format(copy_cnt, line_root) )
	input()

def get_cache_files( line_root ):
	for root, _, files in os.walk(line_root):
		yield from ( detect_img_extension(root, f) for f in files if cache_file_re.match(f) )

def detect_img_extension( root, fname ):
	try:
		ext = extension_dict[imghdr.what( os.path.join(root, fname) )]
		return (root, fname, fname+'.'+ext)
	except:
		print( '"{}" isn\'t image.'.format(os.path.join(root, fname) ) )
		return (root, fname, None)

if __name__ == "__main__":
	main()
