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

#### date\_to\_epoch(year, month, day):
Converts a date with year, month, and day, to an int epoch in UTC time
###### Args:
arg | type | description
--- | ---  | ---
year | int | between 1 and 9999
month | int | between 1 and 12
day | int | between 1 and 31
###### Return:
UTC int epoch

#### now\_delorean():
Creates a Delorean object in UTC time at the current datetime
###### Args:
None
###### Return:
Delorean object in UTC time

#### shift\_epoch(delorean, direction, unit, num\_shifts):
Shifts a Delorean date and converts to epoch
###### Args:
arg | type | description
--- | ---  | ---
delorean | Delorean | date to shift
direction | string | shift the date forwards ('next') or backwards ('last')
unit | int | how much to shift by ('second', 'minute', 'hour', 'day', 'week', 'month', or 'year')
num\_shifts | int | number to shift the date by units
###### Return:
int epoch

#### generate\_epochs(delorean, direction, unit, num\_shifts):
Shifts a Delorean date and generates all epochs in between the initial and shifted date
###### Args:
arg | type | description
--- | ---  | ---
delorean | Delorean | date to shift
direction | string | shift the date forwards ('next') or backwards ('last')
unit | int | how much to shift by ('second', 'minute', 'hour', 'day', 'week', 'month', or 'year')
num\_shifts | int | number to shift the date by units
###### Return:
list of int epochs

#### get\_end\_start\_epochs(year, month, day, direction, unit, num\_shifts):
Shifts a date in year, month, day and gets the initial and shifted epoch
###### Args:
arg | type | description
--- | ---  | ---
year | int | between 1 and 9999
month | int | between 1 and 12
day | int | between 1 and 31
direction | string | shift the date forwards ('next') or backwards ('last')
unit | int | how much to shift by ('second', 'minute', 'hour', 'day', 'week', 'month', or 'year')
num\_shifts | int | number to shift the date by units
###### Return:
dict of int epoch, with keys 'initial' and 'shifted'

