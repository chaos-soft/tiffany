import os
import subprocess

from flask import url_for


class ImageMagickError(Exception):
    pass


def create_thumbnail(image_model, size=r'20000x440\>', name_suffix='-{}x{}',
                     watermark=None):
    s = size.replace('\\', 'x').replace('^', 'x').split('x')[:2]
    root, ext = os.path.splitext(image_model.image)
    sub_path = os.path.join('thumbnails', ''.join((root, name_suffix.format(*s), ext)))
    path = image_model.get_path().replace(image_model.image, sub_path)
    url = url_for('static', filename=sub_path)

    if os.path.isfile(path):
        return url
    else:
        head, _ = os.path.split(path)

        if not os.path.isdir(head):
            os.makedirs(head)

        command = 'convert -gravity center {} -thumbnail {} {}'

        if watermark:
            v1 = '{} {} -composite'.format(image_model.get_path(), watermark)
        else:
            v1 = image_model.get_path()

        if ext.lower() == '.jpg':
            v2 = '-quality 85 {}'.format(path)
        else:
            v2 = path

        if subprocess.call(command.format(v1, size, v2), shell=True):
            raise ImageMagickError('convert error')
    return url


def delete_thumbnail(image_model, size=r'20000x440\>', name_suffix='-{}x{}'):
    s = size.replace('\\', 'x').replace('^', 'x').split('x')[:2]
    root, ext = os.path.splitext(image_model.image)
    sub_path = os.path.join('thumbnails', ''.join((root, name_suffix.format(*s), ext)))
    path = image_model.get_path().replace(image_model.image, sub_path)

    if os.path.isfile(path):
        os.remove(path)
