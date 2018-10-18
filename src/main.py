# -*- coding: utf-8 -*-
import os
import traceback

from tools import float_round, find_weekday, unicode_csv_dictreader


def download_csv():
    """Download the historical daily data as a csv file."""
    import urllib
    from config import API_KEY

    function = 'DIGITAL_CURRENCY_DAILY'
    symbol = 'BTC'
    market = 'USD'
    api_key = API_KEY
    url = ('https://www.alphavantage.co/query?function={}&symbol={}&market={}&apikey={}'
           '&datatype=csv'.format(function, symbol, market, api_key))

    os.chdir('/usr/src/app/Downloads')
    urllib.urlretrieve(url, 'currency_daily_BTC_USD.csv')


def required_computation():
    """
    Compute the average price of each week, store in a csv file,
    and print the week that had the greatest relative spanself.
    """
    # read with csv reader (handle bom and unicode)
    try:
        read_data = list(unicode_csv_dictreader('currency_daily_BTC_USD.csv'))
        print 'Successfully read {} daily data.'.format(len(read_data))
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print 'Failed to read data: {}'.format(traceback.format_exc())
        read_data = []

    # set the initial values
    start_date = None
    end_date = None
    count = 0
    sum = 0
    max = 0
    min = 0
    greatest_relative_span = 0
    flagged_start_date = None
    flagged_end_date = None

    from decimal import Decimal
    from pandas import DataFrame
    report = DataFrame()

    for data in read_data:
        date_str = str(data['timestamp'])
        start_date = date_str
        if end_date is None:
            end_date = date_str
        count += 1

        price_today = Decimal(data['close (USD)'])
        sum += price_today
        if max == 0 or price_today > max:
            max = price_today
        if min == 0 or price_today < min:
            min = price_today

        if find_weekday(date_str) == 0:
            average = float_round(sum / count, 8)
            relative_span = float_round((max - min) / min, 8)
            to_be_inserted = {
                'start_date': [start_date],
                'end_date': [end_date],
                'average': [average],
                'max': [max],
                'min': [min],
                'relative_span': [relative_span]
            }
            report = report.append(DataFrame(to_be_inserted))

            if greatest_relative_span == 0 or relative_span > greatest_relative_span:
                greatest_relative_span = relative_span
                flagged_start_date = start_date
                flagged_end_date = end_date

            end_date = None
            count = 0
            sum = 0
            max = 0
            min = 0

    # make sure the last week is taken into consideration
    if find_weekday(date_str) != 0:
        average = float_round(sum / count, 8)
        relative_span = float_round((max - min) / min, 8)
        to_be_inserted = {
            'start_date': [start_date],
            'end_date': [end_date],
            'average': [average],
            'max': [max],
            'min': [min],
            'relative_span': [relative_span]
        }
        report = report.append(DataFrame(to_be_inserted))

        if relative_span > greatest_relative_span:
            greatest_relative_span = relative_span
            flagged_start_date = start_date
            flagged_end_date = end_date

    os.chdir('/usr/src/app/Reports')
    report.to_csv('week_report.csv', encoding='utf-8',
                  columns=['start_date', 'end_date', 'average', 'max', 'min', 'relative_span'])
    print ('The greatest relative span happened in the week between {} and {} '
           'with the span of {}.'.format(flagged_start_date, flagged_end_date, greatest_relative_span))


if __name__ == "__main__":
    download_csv()
    required_computation()
