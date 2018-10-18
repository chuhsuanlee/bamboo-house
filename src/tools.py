# -*- coding: utf-8 -*-

import codecs
import csv
from decimal import Decimal, ROUND_DOWN


def float_round(num, places=0, rounding=ROUND_DOWN):
    places = Decimal(10) ** (-1 * places)
    return Decimal(str(num)).quantize(places, rounding=rounding)


def find_weekday(date_str):
    from pandas import Timestamp as ts
    date = ts.strptime(date_str, "%Y-%m-%d")
    return ts.weekday(date)


def unicode_csv_dictreader(path, *args, **kwargs):
    """Create a csv dict reader that copes with encoding correctly."""
    # utf-8-sig strips off a BOM if it's present
    stream = codecs.open(path, encoding='utf-8-sig')
    return UnicodeCSVDictReader(stream, *args, **kwargs)


class UnicodeCSVDictReader(csv.DictReader):
    def __init__(self, unicode_csvfile, *args, **kwargs):
        decoder = codecs.getdecoder('utf-8')
        self.decoder = lambda v: decoder(v)[0]
        utf8_csvfile = codecs.iterencode(unicode_csvfile, encoding='utf-8')
        # bollicks to csv.DictReader being an oldstyle class
        csv.DictReader.__init__(self, utf8_csvfile, *args, **kwargs)
        self.fieldnames = [self.decoder(f) for f in self.fieldnames]

    def next(self):
        data = csv.DictReader.next(self)
        return {k: self.decoder(v) for (k, v) in data.iteritems()}
