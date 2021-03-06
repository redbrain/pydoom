import struct


# Each palette in the PLAYPAL lump contains 256 colors
# totaling 768 bytes, where each color is broken into
# three unsigned bytes. Each of these color components
# (red, green, and blue) range between 0 and 255.

kNumColors = 256


class WadPalette:
    
    @staticmethod
    def load_rgb(chunk):
        return struct.unpack("<BBB", chunk)

    @staticmethod
    def load_palette(chunk):
        elements = tuple(map(lambda i: chunk[i*3: (i+1)*3], range(kNumColors)))
        return tuple(map(lambda c: WadPalette.load_rgb(c), elements))

    
class WadPlaypal:

    def __init__(self, lump):
        self._palettes = WadPlaypal.load_palettes(lump)

    @property
    def palettes(self):
        return self._palettes

    def __getitem__(self, index):
        return self._palettes[index]

    def __len__(self):
        return len(self._palettes)

    @staticmethod
    def load_palettes(lump, element_size=768):
        data = lump.data
        number_of_elements = int(lump.size / element_size)
        elements = tuple(map(lambda i: data[i * element_size: (i + 1) * element_size],
                             range(number_of_elements)))
        return tuple(map(lambda c: WadPalette.load_palette(c), elements))
