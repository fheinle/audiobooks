#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""create a tracklist

write track titles and play time for chapter marks to csv file"""

from mutagen.easymp4 import EasyMP4
from cached_property import cached_property

import csv
import os
import sys
import glob
import argparse

from math import floor
from operator import attrgetter

class Track(object):
    """single audio file"""
    def __init__(self, fname):
        self.fname = fname
        self._track = EasyMP4(self.fname)

    @cached_property
    def duration(self):
        """get track duration in seconds"""
        track_duration = int(floor(self._track.info.length) + 1)
        return track_duration

    @cached_property
    def title(self):
        """get track title as uncide string"""
        track_title = self._track['title'][0]
        return track_title

    @cached_property
    def disc_track(self):
        """get disc and track number as tuple"""
        discnumber = int(self._track['discnumber'][0])
        tracknumber = int(self._track['tracknumber'][0])
        return (discnumber, tracknumber)

    def __unicode__(self):
        """text representation"""
        return "<Track '%s'>" % self.title

    def __repr__(self):
        """utf-8 formatted text representation"""
        return self.__unicode__().encode('utf-8')

def get_tracks(dir_name='.'):
    """get track titles and lengths

    track file extensions *must* end with .m4a"""
    track_files = glob.glob(os.path.join(dir_name, '*.m4a'))
    track_list = [Track(track_file) for track_file in track_files]
    return sorted(track_list, key=attrgetter('disc_track'))

def write_csv(output_fname, tracks):
    """write csv file with track numbers and title

    writes to output_fname, expects track list as input"""
    with open(output_fname, 'w') as csv_file:
        track_writer = csv.writer(csv_file)
        for track in tracks:
            track_writer.writerow(
                [track.disc_track[0], track.disc_track[1],
                 track.title.encode('utf-8'), track.duration]
            )

def cli_run(argv):
    """cli script"""
    arg_parser = argparse.ArgumentParser(
        prog=argv[0],
    )
    arg_parser.add_argument('dir_name', help='Directory to index')
    cli_args = arg_parser.parse_args(args=argv[1:])
    output_fname = os.path.join(cli_args.dir_name, 'tracks.csv')
    tracks = get_tracks(os.path.abspath(cli_args.dir_name))
    write_csv(output_fname, tracks)

def main():
    """entrypoint without arguments"""
    raise SystemExit(cli_run(sys.argv))

if __name__ == '__main__':
    main()
