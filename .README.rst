|logo|

|travis| |python| |license| |tag| |status|

Speculator predicts the price trend of cryptocurrencies like Bitcoin and
Ethereum.

Normal markets will also be added in future updates.

How to get started
------------------

.. code:: bash

    git clone https://github.com/amicks/Speculator.git
    cd Speculator/speculator
    python main.py

Yes, it is *that* easy.

**Example:**

|example|

Use the ``--help`` flag for a complete list of optional arguments.
Note: A website for a friendly user experience is in development

Dependencies
~~~~~~~~~~~~

Make sure these packages are installed before running Speculator:

- `Delorean <http://delorean.readthedocs.io/en/latest/install.html>`__, ``pip3 install delorean``

- `requests <http://docs.python-requests.org/en/latest/user/install/#install>`__, ``pip3 install requests``

- `NumPy <https://www.scipy.org/install.html>`__, ``pip3 install numpy``

- `TensorFlow <https://www.tensorflow.org/install/>`__, ``pip3 install tensorflow``

- `scikit-learn <http://scikit-learn.org/stable/install.html>`__, ``pip3 install scikit-learn``

- `pandas <https://pandas.pydata.org/pandas-docs/stable/install.html>`__, ``pip3 install pandas``

Or just use a one-liner:

.. code:: bash

    pip3 install delorean requests numpy tensorflow scikit-learn pandas

API
~~~

Speculator is available as a package on PyPi.

::

    pip3 install speculator

If you want to use or thoroughly understand Speculator’s API, I
recommend checking out the `docs <https://github.com/amicks/Speculator/tree/master/docs/>`__, which features a fully
documented example.

Project Structure
~~~~~~~~~~~~~~~~~

::

    LICENSE
    README.md

    docs
        \_ CONTRIBUTING.md
        \_ analysis.md
        \_ example.md
        \_ example.py
        \_ utils.md

    speculator
        \_ main.py
        \_ market.py
        \_ features
                    \_ rsi.py
                    \_ sma.py
                    \_ so.py
        \_ models
                 \_ deep_neural_network.py
                 \_ random_forest.py
        \_ tests
                \_ integration
                              \_ test_poloniex.py
                \_ unit
                       \_ test_date.py
                       \_ test_poloniex.py
                       \_ test_rsi.py
                       \_ test_sma.py
                       \_ test_so.py
                       \_ test_stats.py
        \_ utils
                \_ date.py
                \_ poloniex.py
                \_ stats.py

Contact for Feedback, Questions, or Issues
------------------------------------------

Feel free to send me a message on Reddit at
`/u/shneap <https://www.reddit.com/message/compose?to=shneap>`__. I am
happy to hear any concerns, good or bad, in order to progress the
development of this project.

Contributing
~~~~~~~~~~~~

Please read the detailed `contributing doc <https://github.com/amicks/Speculator/blob/master/docs/CONTRIBUTING.md>`__.

.. |logo| image:: https://i.imgur.com/klemIi5.png
.. |travis| image:: https://img.shields.io/travis/amicks/Speculator.svg
   :target: https://travis-ci.org/amicks/Speculator
.. |python| image:: https://img.shields.io/pypi/pyversions/Speculator.svg
.. |license| image:: https://img.shields.io/pypi/l/Speculator.svg
   :target: https://github.com/amicks/Speculator/blob/master/LICENSE
.. |tag| image:: https://img.shields.io/github/tag/amicks/speculator.svg
   :target: https://github.com/amicks/Speculator/archive/0.1.tar.gz
.. |status| image:: https://img.shields.io/pypi/status/Speculator.svg
.. |example| image:: https://i.imgur.com/5tB8zvJ.png
