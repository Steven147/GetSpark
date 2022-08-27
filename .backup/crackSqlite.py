source = """
0x60000062d6a0: 0xd7 0xe4 0xb9 0x4a 0x54 0xc7 0x4e 0x1a
0x60000062d6a8: 0xae 0xce 0xbf 0x4c 0x7e 0x20 0xd6 0x45
0x60000062d6b0: 0xac 0x45 0x39 0xcf 0xe1 0xbc 0x4d 0xc9
0x60000062d6b8: 0xa2 0x5d 0x4c 0x4b 0xe9 0x65 0x23 0x33
"""

key = '0x' + ''.join(i.partition(":")[2].replace('0x', '').replace(' ', '') for i in source.split('\n')[1:5])

print(key)
# 0xd7e4b94a54c74e1aaecebf4c7e20d645ac4539cfe1bc4dc9a25d4c4be9652333