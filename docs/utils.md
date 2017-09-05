# Utility Package
The utils package contains modules which help implement core features to Speculator.  They provide a way to get raw data into the format that the core features require.

## Date.py
Date is used to convert dates of year, month, day, into UTC epoch time.
The Delorean package acts as an intermediary in the conversion process by creating a datetime object in UTC time, shifting the date to another one if requested, and converting to a floating point epoch.  The year, month, and day format provides an easy interface without complex parsing when using in core features.  The conversion to epochs aids in standardizing the time into something more efficient, and allows for an easy hook into the Poloniex API.

### Dependencies:
* [Delorean](http://delorean.readthedocs.io/en/latest/install.html), ` pip install delorean `

### Functions
#### date\_to\_delorean(year, month, day):
Converts a date with year, month, and day, to a Delorean object in UTC time
###### Args:
arg | type | description
--- | ---  | ---
year | int | between 1 and 9999
month | int | between 1 and 12
day | int | between 1 and 31
###### Return:
Delorean object in UTC time


