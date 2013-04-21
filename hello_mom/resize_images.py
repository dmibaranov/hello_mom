from PIL import Image
from PIL.ExifTags import TAGS

ORIENTATION_TAG_ID = [k for k, v in TAGS.items() if v == 'Orientation'][0]

ROTATION_ANGLES = {
    1: 0,  # 'Horizontal (normal)'
    2: 180,  # 'Mirrored horizontal',
    3: 180,  # 'Rotated 180',
    4: 0,  # 'Mirrored vertical',
    5: -90,  # 'Mirrored horizontal then rotated 90 CCW',
    6: -90,  # 'Rotated 90 CW',
    7: 90,  # 'Mirrored horizontal then rotated 90 CW',
    8: 90,  # 'Rotated 90 CCW'
}


def resize(in_filename, out_filename, width=1024, rotate=True):
    if in_filename != out_filename:
        im = Image.open(in_filename)

        exifdict = im._getexif()
        if rotate and exifdict and exifdict.get(ORIENTATION_TAG_ID):
            rotate_angle = ROTATION_ANGLES.get(exifdict[ORIENTATION_TAG_ID], 0)
            im = im.rotate(rotate_angle)

        scale = float(width) / float(im.size[0])
        im = im.resize([int(scale * s) for s in im.size], Image.ANTIALIAS)

        im.save(out_filename, "JPEG", quality=75)
    else:
        raise Exception("Stopped, resizing of originals is not allowed")
