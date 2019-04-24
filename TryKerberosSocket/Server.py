import math
import string
import random
import socket

portinfobase = {12345:"KDC", 32344:"Client", 22343:"Server"}
sessionkeys = {'Kca': 3, 'Kct': 4, 'Kts': 5}
alphabet = list(string.ascii_uppercase)
