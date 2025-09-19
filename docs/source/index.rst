.. hts-synth documentation master file, created by
   sphinx-quickstart on Tue Sep 16 09:07:54 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to hts-synth Documentation
=======================
**hts-synth** is a Python library for generating synthetic high-throughput sequencing (HTS) data. It provides constrained generators that create realistic sequencing reads with configurable error profiles, making it ideal for testing bioinformatics pipelines and exploring genomic analysis workflows.

.. note::
   **hts-synth** is currently in pre-alpha.
   This means the library is still under active development, and its API, features, and behaviour may change without notice.
   While the core functionality is usable for experimentation and prototyping, it is not yet considered stable for production use.
   Users are encouraged to try it out, report issues, and provide feedback to help guide development, but should expect possible breaking changes in future releases.

Quick Start
-----------

Install hts-synth and generate your first synthetic read:

.. code-block:: bash

   pip install hts-synth
   hts-synth --substitution-probability 0.02 ATCGATCG

.. image:: /images/hts-synth-fastq-gen2.gif
   :alt: Example command line usage
   :width: 600px
   :align: center


The library can be used both as a command-line tool for quick data generation; as a Python library for integration into larger bioinformatics applications or as a faker provider for testing data generation

User Guides
-----------

Learn how to use hts-synth in different contexts:

.. toctree::
   :maxdepth: 2
   :caption: User Documentation:

   user_docs/users_docs

API Usage as a Package
----------------------

For programmatic use and advanced integration:

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/hts_synth

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
