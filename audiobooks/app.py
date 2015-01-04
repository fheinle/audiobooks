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
import subprocess

from math import floor
from operator import attrgetter
from tempfile import mkstemp

CHAPTER_TEMPLATE = """CHAPTER%(CHAPNUM)s=%(HOURS)02d:%(MINS)02d:%(SECS)02d
CHAPTER%(CHAPNUM)sNAME=%(CHAPNAME)s
"""
MERGE_COMMAND = "MP4Box"
CHAPS_COMMAND = "mp4chaps"

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

    @cached_property
    def album(self):
        """get album name"""
        track_album = self._track['album'][0]
        return track_album

    @cached_property
    def artist(self):
        """get artist name"""
        track_artist = self._track['artist'][0]
        return track_artist

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
                 track.fname,
                 track.title.encode('utf-8'),
                 track.duration,
                 ]
            )

def write_chaplist(output_fname, tracks):
    """write MP4Box compatible chapter marks file

    writes to output_fname, expects track list as input"""
    output_lines = []
    for track_number, track in enumerate(tracks):
        mins, secs = divmod(track.duration, 60)
        hours, mins = divmod(mins, 60)
        output_lines.append(
            CHAPTER_TEMPLATE % {'CHAPNUM':track_number,
                                 'HOURS':hours, 'MINS':mins, 'SECS':secs,
                                 'CHAPNAME':track.title.encode('utf-8')
                               }
        )
    with open(output_fname, 'w') as output_file:
        output_file.writelines(output_lines)
    return output_fname

def combine_files(output_fname, tracks, chaplist_fname):
    """combine m4a files to one big file

    writes to output_fname, expects track list as input"""
    merge_cmd_and_args = []
    for track in tracks:
        merge_cmd_and_args.append('-cat')
        merge_cmd_and_args.append(track.fname)
    merge_cmd_and_args.insert(0, MERGE_COMMAND)
    merge_cmd_and_args.extend(['-chap', chaplist_fname])
    merge_cmd_and_args.append(output_fname)
    merge_call = subprocess.call(merge_cmd_and_args)
    if merge_call != 0:
        raise RuntimeError('Merge unsuccessful')
    if subprocess.call(
        [CHAPS_COMMAND, '--convert', '--chapter-qt', output_fname]
    ) != 0:
        raise RuntimeError('Could not convert to QT chapter marks')
    return output_fname

def write_audio_metadata(output_fname, album, artist):
    """Write album and artist information to audiobook file

    changes output_fname on the fly, expects album and artist"""
    track = EasyMP4(output_fname)
    track['album'] = album
    track['title'] = album
    track['artist'] = artist
    track.save()


def cli_run(argv):
    """cli script"""
    arg_parser = argparse.ArgumentParser(
        prog=argv[0],
    )
    arg_parser.add_argument('dir_name', help='Directory to index')
    arg_parser.add_argument('-o', '--output',
                            help='Output filename', type=str)
    cli_args = arg_parser.parse_args(args=argv[1:])
    tracks = get_tracks(os.path.abspath(cli_args.dir_name))
    if cli_args.output:
        output_fname = cli_args.output
    else:
        output_fname = "%s.m4b" % os.path.join(
            cli_args.dir_name,
            tracks[0].album.encode('utf-8')
        )
    chapter_fname = mkstemp(prefix='chaplist')[1]
    try:
        write_chaplist(chapter_fname, tracks)
    except:
        raise
    try:
        combine_files(output_fname, tracks, chapter_fname)
    except:
        raise
    try:
        write_audio_metadata(output_fname,
                             album=tracks[0].album,
                             artist=tracks[0].artist,
        )
    except:
        raise

def main():
    """entrypoint without arguments"""
    raise SystemExit(cli_run(sys.argv))

if __name__ == '__main__':
    main()
