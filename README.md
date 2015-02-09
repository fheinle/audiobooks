Audiobooks
====
**Audiobooks** allows creation of *m4b* audiobooks from single *m4a* files.

Cover images and album metadata such as artist, album name and chapter markings are supported.

## Current status

Currently it works but you'll have to be careful to fully satisfy all requirements, e.g. software dependencies and correct file metadata on your source material. In the future, those edges will be a little less rough.

## Requirements

 * python-mutagen
 * MP4Box from gpac
 * mp4chaps from mp4v2-utils
 * cached_property python module

## Installation

This works for Ubuntu:

    $ sudo apt-get install python-mutagen gpac mp4v2-utils
    $ git clone https://github.com/fheinle/audiobooks.git
    $ cd audiobooks
    $ sudo python setup.py install

## Usage

Currently, Audiobooks requires your files already ripped from CD as mp4 audio,
no conversion is done. Also, those files need to be tagged proplery, i.e. with
album name, artist name, disc number, track title and track number. You can use
ExFalso from QuodLibet if you don't have proper tags.


    $ audiobooks /path/to/m4a/files

You should receive an *album name*.m4b file with chapters and album metadata.

If you want to add a cover image to your audiobook file, that image must already be available as PNG or JPG. You can either name it ``cover.jpg`` and place it in the same directory as your audio files, where it will be found automatically or pass its filename explicitly:

    $ audiobooks --cover /path/to/cover.jpg /path/to/m4/files

## Contributors

 * Florian Heinle <launchpad@planet-tiax.de>

## License

[Gnu General Public License (GPL), Version 2 or later](https://www.gnu.org/licenses/gpl-2.0.html#SEC1)
