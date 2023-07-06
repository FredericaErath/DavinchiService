"""
General tool methods.
"""
import logging
import os
import re
import zipfile

import qrcode

from constant import BASE_DIR, BASE_DATA_TEMP_DIR

log = logging.getLogger(__name__)


def pack_files(file_names: list):
    """
    Helper function, turn data files into zip.

    :param file_names: list of files needed to be packed
    """
    zip_name = f'files.zip'
    with zipfile.ZipFile(zip_name, 'w') as z:
        for filename in file_names:
            file = re.findall(r'[1-9][0-9].png', filename)
            print(file)
            z.write(os.path.join(BASE_DATA_TEMP_DIR, filename), file[0])
    log.info('{}压缩成功'.format(zip_name))
    z.close()
    return os.path.join(BASE_DIR, zip_name)


def generate_qrcode_pic(i_id: str):
    """
    Helper function, generate a qr_code picture.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=4,
        box_size=10
    )
    img = qrcode.make(i_id, version=4, border=4, box_size=12)
    file_path = os.path.join(BASE_DATA_TEMP_DIR, f'{i_id}.png')
    img.save(file_path)
    return file_path
