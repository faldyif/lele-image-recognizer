import base64
from pprint import pprint

import lib.scripts

encodings = lib.scripts.pre_encode()
# print(encodings)

lala = lib.scripts.find_face('test.jpg', encodings)
pprint(lala)

