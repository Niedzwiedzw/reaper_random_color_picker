from pprint import pformat
from random import randint
from collections import defaultdict

try:
    from reaper_python import *

    def rprint(message=''):
        RPR_ShowConsoleMsg(pformat(message) + "\n")

except ImportError:
    print('could not import `reaper_python` module...')

    def rprint(message=''):
        print(pformat(message))

from itertools import islice
import colorsys


def take(iterable, count): return islice(iterable, count)


class HLSColor(object):
    def __init__(self, hue, lightness, saturation):
        self.hue = hue/360.
        self.lightness = lightness/100.
        self.saturation = saturation/100.

    def values(self):
        return self.hue, self.lightness, self.saturation

    def as_rgb(self):
        return map(lambda c: int(c*255), colorsys.hls_to_rgb(*self.values()))

    def as_native(self):
        return RPR_ColorToNative(*self.as_rgb())

    def __repr__(self):
        return 'hls({}, {}, {})'.format(self.hue, self.lightness, self.saturation)


GOLDEN_RATIO = (1 + 5**0.5)/2.0
MAX_HUE = 360

MAX_LIGHTNESS = 60
MIN_LIGHTNESS = 40
MAX_SATURATION = 70
MIN_SATURATION = 100

SEED = randint(0, MAX_HUE)


MASTER_TRACK = RPR_GetMasterTrack(0)
NULL_TRACK = '(MediaTrack*)0x0000000000000000'


def nth_ratio_series_element(n, maximal, minimal=0):
    maximal = maximal - minimal
    return minimal + int((minimal + SEED + GOLDEN_RATIO * maximal * n) % maximal)


def nth_hue(n): return nth_ratio_series_element(n, MAX_HUE)


def nth_saturation(n): return nth_ratio_series_element(n, MAX_SATURATION, MIN_SATURATION)


def nth_lightness(n): return nth_ratio_series_element(n, MAX_LIGHTNESS, MIN_LIGHTNESS)


def random_colors():
    i = 0
    while True:
        yield HLSColor(nth_hue(i), nth_lightness(i), nth_saturation(i))
        i += 1


def topmost_parent(track):
    parent = track
    safety_count = 1
    while RPR_GetParentTrack(parent) != NULL_TRACK and safety_count:
        parent = RPR_GetParentTrack(parent)
        safety_count -= 1
    return parent


def selected_tracks():
    tracks = map(lambda x: RPR_GetSelectedTrack(0, x), range(RPR_CountSelectedTracks(0)))
    hierarchy = defaultdict(list)

    for track in tracks:
        hierarchy[topmost_parent(track)].append(track)
    return hierarchy


def main():
    for tracks, color in zip(selected_tracks().values(), random_colors()):
        for track in tracks:
            RPR_SetTrackColor(track, color.as_native())


if __name__ == '__main__':
    main()
