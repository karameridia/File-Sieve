import os
from itertools import count

from abstract.file_finder import FileFinder
from util.file_data_util import write_to_file


BMP_START = b'BM'

_id_counter = count()


def create_bmp_finder(output_path):
    out_dir = os.path.join(output_path, 'BMP')
    return BMPFinder(out_dir, 'bmp')


class BMPFinder(FileFinder):
    def __init__(self, out_dir, ext, make_new=True):
        super().__init__(out_dir, ext, make_new=make_new)

    def _check_signature(self, sector) -> bool:
        return sector[:len(BMP_START)] == BMP_START
    
    def _find_file(self, f, sector):
        start_position = f.tell() - 512
        sig_length = len(BMP_START)
        file_size = int.from_bytes(
            sector[sig_length:sig_length + 4], byteorder='little')
        if file_size > 20_000_000:
            return False
        id = next(_id_counter)
        file_path = os.path.join(self.out_dir, f'file{id}.{self.ext}')
        write_to_file(f, start_position, file_size, file_path)
        f.seek(start_position + 512)
        return True