import argparse
import os
import sys
import webbrowser
import zipfile

from pystache.renderer import Renderer

from hello_mom.resize_images import resize


def gen_album(args):
    source_dir = os.path.abspath(args.source_dir)
    dest_dir = os.path.abspath(args.dest_dir)

    if not os.path.exists(source_dir):
        raise Exception('Source path not exists')

    if os.path.exists(dest_dir):
        raise Exception('Destination path exists')

    source_photos_dir = os.path.join(dest_dir, 'photos')
    os.makedirs(source_photos_dir)

    resized_images = []
    for root, dirs, files in os.walk(source_dir):
        dest_sub_dir = root.replace(source_dir, source_photos_dir)
        if not os.path.exists(dest_sub_dir):
            os.makedirs(dest_sub_dir)
        print 'Resizing {0} files in {1}'.format(len(files), root)
        for filename in sorted(files):
            try:
                dest_filename = os.path.join(dest_sub_dir, filename)
                resize(os.path.join(root, filename), dest_filename)
                resized_images.append(
                    {
                        'rel_path': dest_filename.replace(dest_dir, '')[1:],
                    }
                )
            except IOError:
                print 'Skipped {0}'.format(filename)

    template = os.path.join(os.path.dirname(__file__), 'templates', 'base')
    context = {'images': resized_images}

    index_html_file = os.path.join(dest_dir, 'index.html')
    with open(index_html_file, 'wt') as index_html:
        index_html.write(Renderer().render_name(template, context))
    webbrowser.open(index_html_file)


def zip_album(args):
    zipfile


parser = argparse.ArgumentParser(description='Set a tools for generation '
                                             'html album from directory '
                                             'with photos')
subparsers = parser.add_subparsers()

parser_gen = subparsers.add_parser('gen', help='Generating album')
parser_gen.add_argument('source_dir', help='Source folder with photos')
parser_gen.add_argument('dest_dir', help='Output folder for album')
parser_gen.set_defaults(func=gen_album)

parser_zip = subparsers.add_parser('zip', help='Zipping existing album')
parser_zip.add_argument('source_dir', help='Source folder with album')
parser_zip.add_argument('--album_name', help='Album name', default='album')
parser_zip.set_defaults(func=zip_album)


if __name__ == '__main__':
    args = parser.parse_args()
    sys.exit(args.func(args))
