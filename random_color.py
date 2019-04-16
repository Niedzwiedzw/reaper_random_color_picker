from pprint import pformat
from random import randint

try:
    from reaper_python import *

    def rprint(message):
        RPR_ShowConsoleMsg(pformat(message))

except ImportError:
    print('could not import `reaper_python` module...')

    def rprint(message):
        print(pformat(message))

from itertools import islice
import colorsys


def take(iterable, count): return islice(iterable, count)


class HLSColor(object):
    def __init__(self, hue, lightness, saturation):
        self.hue = int(hue/360.)
        self.lightness = int(lightness/100.)
        self.saturation = int(saturation/100.)

    def values(self):
        return self.hue, self.lightness, self.saturation

    def as_rgb(self):
        return map(lambda c: c*255, colorsys.hls_to_rgb(*self.values()))

    def as_native(self):
        return RPR_ColorToNative(*self.as_rgb())


GOLDEN_RATIO = (1 + 5**0.5)/2.0
MAX_HUE = 360

MAX_LIGHTNESS = 90
MIN_LIGHTNESS = 30
MAX_SATURATION = 100
MIN_SATURATION = 20


def nth_ratio_series_element(n, maximal, minimal=0):
    maximal = maximal - minimal
    return minimal + int((minimal + GOLDEN_RATIO * maximal * n) % maximal)


def nth_hue(n): return nth_ratio_series_element(n, MAX_HUE)


def nth_saturation(n): return nth_ratio_series_element(n, MAX_SATURATION, MIN_SATURATION)


def nth_lightness(n): return nth_ratio_series_element(n, MAX_LIGHTNESS, MIN_LIGHTNESS)


def random_colors():
    i = 0
    while True:
        yield HLSColor(nth_hue(i), nth_lightness(i), nth_saturation(i))
        i += 1


def selected_tracks():
    return map(lambda x: RPR_GetSelectedTrack(0, x), range(RPR_CountSelectedTracks(0)))


def main():
    for track, color in zip(selected_tracks(), random_colors()):
        rprint(track)
        rprint(color.as_native())
        RPR_SetTrackColor(track, color.as_native())


if __name__ == '__main__':
    main()
