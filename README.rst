============
grg-pssedata
============

**release:**

.. image:: https://badge.fury.io/py/grg-pssedata.svg
    :target: https://badge.fury.io/py/grg-pssedata

.. image:: https://readthedocs.org/projects/grg-pssedata/badge/?version=stable
  :target: http://grg-pssedata.readthedocs.io/en/stable/?badge=stable
  :alt: Documentation Status

**dev status:**

.. image:: https://travis-ci.org/lanl-ansi/grg-pssedata.svg?branch=master
  :target: https://travis-ci.org/lanl-ansi/grg-pssedata
  :alt: Build Report
.. image:: https://codecov.io/gh/lanl-ansi/grg-pssedata/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/lanl-ansi/grg-pssedata
  :alt: Coverage Report
.. image:: https://readthedocs.org/projects/grg-pssedata/badge/?version=latest
  :target: http://grg-pssedata.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


grg-pssedata is a minimalist python package for working with PSS/E data files.

The package can be installed via::

    pip install grg-pssedata


License
------------
This package is developed at Los Alamos National Laboratory and is provided under a BSD-3 license as part of the Grid Research for Good Software Tools (C18036), see the `LICENSE` file for the full text.


Changelog
------------

**staged**

- nothing


**v0.1.4**

- Improved support for component default values
- Fixed type of xfrrat and nxfrat values (Issue #4)
- Fixed line endings in file export


**v0.1.3**

- Improved support for non-string values in class constructors
- Fixed Bus default values


**v0.1.2**

- Added support for default values in data files
- Improved error reporting when a data line does not split into an acceptable number of items


**v0.1.1**

- Drop support for python 2.7 and 3.4
- Fixed bug where parsing lines with commas or comment characters inside single quotes would fail
- Added support for FACTS Devices, Two-Terminal DC Lines, VSC DC Lines, Multi-Terminal DC Lines, Interarea Transfers, Transformer Impedance Correction Tables, Induction Machines, and Multi-Section Line Groupings


**v0.1.0**

- Initial release


**v0.0.2**

- PyPI test release


**v0.0.1**

- Initial test tag
