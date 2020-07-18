#!/usr/bin/env python
from unittest import TestCase, main #, skip

from image_parser import parse_data
from dataio.wav import read_from_wav
from dataio.png import read_from_png


class TestDataio(TestCase):
    def test_read_radio_transmission_recording(self):
        d = read_from_wav('radio-transmission-recording.wav')
        parsed = parse_data(d)
        expected = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[]]
        assert parsed == expected

    def test_read_message1_png(self):
        d = read_from_png('img/message1.png')
        parsed = parse_data(d)
        expected = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[]]
        assert parsed == expected
