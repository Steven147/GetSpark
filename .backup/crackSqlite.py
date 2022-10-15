source = """
0x600002657ce0: 0xd9 0x27 0xf6 0x90 0xcd 0x39 0x43 0xa7
0x600002657ce8: 0xa9 0xcd 0x53 0x76 0x5e 0xca 0x2a 0xd6
0x600002657cf0: 0x1d 0x54 0xa2 0x86 0xd8 0xca 0x4d 0xa4
0x600002657cf8: 0xa3 0x4b 0x16 0x1a 0x36 0xbe 0xf0 0x5a
"""

key = '0x' + ''.join(i.partition(":")[2].replace('0x', '').replace(' ', '') for i in source.split('\n')[1:5])

print(key)
# 0xd927f690cd3943a7a9cd53765eca2ad61d54a286d8ca4da4a34b161a36bef05a