#!/usr/bin/env python
"""

============
Installation
============
Please use a Python virtualenv.

Prerequsites
------------
::

    None

Python packages
---------------
::

    pip3 install pandas fastparquet

====
Data
====
Data acquisition examples.
::

    wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet

=====
Usage
=====

Synopsis::

    python parquet-to-influxdb-all.py <parquetfile> <external-ip-influxdb> <database> <measurement>

Example::

    python parquet-to-influxdb-all.py yellow_tripdata_2022-01.parquet <external-ip-influxdb> exercise passenger

"""
import sys
import pandas as pd
from influxdb import DataFrameClient


def read_parquet_file(filename):
    """
    """
    df = pd.read_parquet(filename)

    df.set_index(pd.DatetimeIndex(df.tpep_pickup_datetime), inplace=True)
    df.drop('tpep_pickup_datetime',axis=1,inplace=True)
    del df['tpep_dropoff_datetime']
    df.sort_index(inplace=True, ascending=True)

    return df


def dataframe_to_influxdb(host='None', port=8086, dbname=None, measurement=None, df=None):
    # https://github.com/influxdata/influxdb-python/blob/master/examples/tutorial_pandas.py
    client = DataFrameClient(host=host, port=port, database=dbname)
    client.create_database(dbname)

    tag_columns = ['VendorID', 'RatecodeID', 'payment_type']
    client.write_points(df, measurement=measurement, tag_columns=tag_columns, tags=None, batch_size=10240)


if __name__ == '__main__':
    df = read_parquet_file(sys.argv[1])
    #print(df)
    dataframe_to_influxdb(host-sys.argv[2], dbname=sys.argv[3], measurement=sys.argv[4], df=df)

