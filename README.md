<p align="center">
  <img src="https://i.imgur.com/AmrHhZV.png" width="425" height="200">
</p>

<div align="center">

[![travis build](https://img.shields.io/travis/AllstonMickey/Speculator.svg)](://travis-ci.org/AllstonMickey/Speculator)
![python version](https://img.shields.io/pypi/pyversions/Speculator.svg)
[![license](https://img.shields.io/pypi/l/Speculator.svg)](https://github.com/amicks/Speculator/blob/master/LICENSE)
[![tag](https://img.shields.io/github/tag/amicks/speculator.svg)](https://github.com/amicks/Speculator/archive/0.1.tar.gz)
![status](https://img.shields.io/pypi/status/Speculator.svg)

</div>

<br/>

Speculator predicts the price trend of cryptocurrencies like Bitcoin and Ethereum.

Normal markets will also be added in future updates.

## How to get started
``` bash
git clone https://github.com/amicks/Speculator.git
cd Speculator/speculator
python main.py
```
Yes, it is _that_ easy.

**Example:**
<p>
  <img src="https://i.imgur.com/c6JdDWt.png" width="700" height="180">
</p>

Use the `--help` flag for a complete list of optional arguments.
###### Note: A website for a friendly user experience is in development

### Dependencies
Make sure these packages are installed before running Speculator:
* [Delorean](http://delorean.readthedocs.io/en/latest/install.html), `pip3 install delorean`
* [requests](http://docs.python-requests.org/en/latest/user/install/#install) `pip3 install requests`
* [NumPy](https://www.scipy.org/install.html), `pip3 install numpy`
* [TensorFlow](https://www.tensorflow.org/install/), `pip3 install tensorflow`
* [scikit-learn](http://scikit-learn.org/stable/install.html), `pip3 install scikit-learn`
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), `pip3 install pandas`

Or just use a one-liner:
``` bash
pip3 install delorean requests numpy tensorflow scikit-learn pandas
```

### API
Speculator is available as a package on PyPi.
```
pip3 install speculator
```

If you want to use or thoroughly understand Speculator's API, I recommend checking out the [docs](docs/), which features a fully documented example.

### Project Structure
`docs/` Documentation overview for packages, modules, and others.

`speculator/`  Project source files.

`speculator/main.py`  Main file to run Speculator with arguments.  Predicts the next trend of a ticker like USDT to BTC.

`speculator/market.py`  Module with market technical analysis features and their setup to a machine learning model.

`speculator/models/` Package of machine learning models.

`speculator/examples/`  Package of python script examples of Speculator's API and their related documentation/walkthrough/how-to. **This is important to understand Speculator's API**

`speculator/features/`  Package of market technical analysis indicators.

`speculator/utils/` Package with modules for basic functions like getting market data from an API or converting dates to epochs.

## Contact for Feedback, Questions, or Issues
Feel free to send me a message on Reddit at [/u/shneap](https://www.reddit.com/message/compose?to=shneap).  I am happy to hear any concerns, good or bad, in order to progress the development of this project.

### Contributing
Please read the detailed [contributing doc](docs/CONTRIBUTING.md).

