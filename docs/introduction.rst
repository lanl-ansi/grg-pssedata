============
Introduction
============

Overview
------------------------

grg-pssedata is a minimalist python package to support the reading and writing of PSSE_ network data files.

The primary entry point of the library is :class:`grg_pssedata.io` module, which contains the methods for data input and output.


Installation
------------------------

Simply run::

    pip install grg-pssedata


Testing
------------------------

grg-pssedata is designed to be a library that supports other software.  
It is not immediately useful from the terminal.
However, you can test the parsing functionality from the command line with:: 

    python -m grg_pssedata.io <path to PSSE case file>

If this command is successful, you will see a simplified plain text version of the network data printed to the terminal.

.. _PSSE: https://www.siemens.com/global/en/home/products/energy/services/transmission-distribution-smart-grid/consulting-and-planning/pss-software/pss-e.html

