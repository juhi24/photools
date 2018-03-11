#!/usr/bin/env python
# coding: utf-8
"""License: GNU GPL v3"""
import re
import sys
import argparse


def make_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Filename friendly short version of camera model.')
    parser.add_argument('model', metavar='CAMERA_MODEL', type=str, nargs='?',
                        help='camera model string')
    return parser


def short_camera_model(m, includeCharacters='', missing=''):
    """
    Returns in shorterned string format the camera model used to record
    the image.

    Returns missing if the metadata value is not present.

    The short format is determined by the first occurrence of a digit in
    the
    camera model, including all alphaNumeric characters before and after
    that digit up till a non-alphanumeric character, but with these
    interventions:

    1. Canon "Mark" designations are shortened prior to conversion.
    2. Names like "Canon EOS DIGITAL REBEL XSi" do not have a number and
    must
        and treated differently (see below)

    Examples:
    Canon EOS 300D DIGITAL -> 300D
    Canon EOS 5D -> 5D
    Canon EOS 5D Mark II -> 5DMkII
    NIKON D2X -> D2X
    NIKON D70 -> D70
    X100,D540Z,C310Z -> X100
    Canon EOS DIGITAL REBEL XSi -> XSi
    Canon EOS Digital Rebel XS -> XS
    Canon EOS Digital Rebel XTi -> XTi
    Canon EOS Kiss Digital X -> Digital
    Canon EOS Digital Rebel XT -> XT
    EOS Kiss Digital -> Digital
    Canon Digital IXUS Wireless -> Wireless
    Canon Digital IXUS i zoom -> zoom
    Canon EOS Kiss Digital N -> N
    Canon Digital IXUS IIs -> IIs
    IXY Digital L -> L
    Digital IXUS i -> i
    IXY Digital -> Digital
    Digital IXUS -> IXUS

    The optional includeCharacters allows additional characters to appear
    before and after the digits.
    Note: special includeCharacters MUST be escaped as per syntax of a
    regular expressions (see documentation for module re)

    Examples:

    includeCharacters = '':
    DSC-P92 -> P92
    includeCharacters = '\-':
    DSC-P92 -> DSC-P92

    If a digit is not found in the camera model, the last word is returned.

    Note: assume exif values are in ENGLISH, regardless of current platform
    
    Original author: Damon Lynch
    """
    m = m.replace(' Mark ', 'Mk')
    m = m.replace('IXUS ', 'IXUS')
    if m:
        s = r"(?:[^a-zA-Z0-9%s]?)(?P<model>[a-zA-Z0-9%s]*\d+[" \
            r"a-zA-Z0-9%s]*)" \
            % (includeCharacters, includeCharacters, includeCharacters)
        r = re.search(s, m)
        if r:
            return r.group("model")
        else:
            head, space, model = m.strip().rpartition(' ')
            return model
    else:
        return missing


def main(*args, **kws):
    model = short_camera_model(*args, **kws)
    print(model)


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    if len(sys.argv)>1:
        main(args.model)
    elif not sys.stdin.isatty(): # if piped
        main(sys.stdin.read())
    else:
        parser.print_help()
