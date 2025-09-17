CLI Interface
=============

The ``hts-synth`` command-line interface provides a simple way to generate synthetic high-throughput sequencing (HTS) read data from a reference sequence. This tool is designed for testing and exploration purposes, allowing you to simulate realistic sequencing errors and generate reads in various output formats.

Installation
------------

Install the package to make the CLI tool available:

.. code-block:: bash

   pip install -e .

Basic Usage
-----------

The basic syntax for the ``hts-synth`` command is:

.. code-block:: bash

   hts-synth [OPTIONS] [NREADS] REF

Where:

* ``NREADS`` is the number of reads to generate (default: 1)
* ``REF`` is the reference sequence from which to generate reads

Quick Start
-----------

Generate a single read from a reference sequence:

.. code-block:: bash

   hts-synth ATCGATCGATCG

Generate 5 reads:

.. code-block:: bash

   hts-synth 5 ATCGATCGATCG

Generate reads with custom error probabilities:

.. code-block:: bash

   hts-synth --insertion-probability 0.05 --deletion-probability 0.03 10 ATCGATCGATCG

Command Options
---------------

Position Options
~~~~~~~~~~~~~~~~

``-p, --reference-position INTEGER``
   The starting position within the reference genome where this read originates.

   * **Default:** 0
   * **Example:** ``--reference-position 1000``

Error Probability Options
~~~~~~~~~~~~~~~~~~~~~~~~~

``--insertion-probability FLOAT``
   The probability that the generated read will include an insertion.

   * **Default:** 0.01 (1%)
   * **Range:** 0.0 to 1.0
   * **Example:** ``--insertion-probability 0.05``

``--deletion-probability FLOAT``
   The probability that the generated read will include a deletion.

   * **Default:** 0.01 (1%)
   * **Range:** 0.0 to 1.0
   * **Example:** ``--deletion-probability 0.03``

``--substitution-probability FLOAT``
   The probability that the generated read will include a substitution.

   * **Default:** 0.02 (2%)
   * **Range:** 0.0 to 1.0
   * **Example:** ``--substitution-probability 0.04``

Output Format Options
~~~~~~~~~~~~~~~~~~~~~

``-f, --out-format [fq|seq|qual]``
   Specify the format of the output.

   * **Default:** ``fq`` (FASTQ format)
   * **Options:**

     * ``fq`` - FASTQ format (includes header, sequence, separator, and quality scores)
     * ``seq`` - Sequence only
     * ``qual`` - Quality scores only

   * **Example:** ``--out-format seq``

Help Option
~~~~~~~~~~~

``-h, --help``
   Show help message and exit.

Arguments
---------

``NREADS``
   Number of reads to generate (optional, default: 1).

   * **Type:** Integer
   * **Default:** 1
   * **Example:** ``10`` (generates 10 reads)

``REF``
   Reference sequence from which to generate synthetic reads (required).

   * **Type:** String
   * **Format:** DNA sequence using standard nucleotide letters (A, T, C, G)
   * **Example:** ``ATCGATCGATCGATCG``

Output Formats
--------------

FASTQ Format (``fq``)
~~~~~~~~~~~~~~~~~~~~~

The default output format includes all components of a FASTQ record:

.. code-block:: text

   @read-1a2b3c4d5e6f7890
   ATCGATCGATCG
   +
   IIIIIIIIIIII

Where:

* Line 1: Header line starting with ``@`` followed by a unique read identifier
* Line 2: The DNA sequence
* Line 3: Separator line (``+``)
* Line 4: Quality scores in ASCII format

Sequence Only (``seq``)
~~~~~~~~~~~~~~~~~~~~~~~

Outputs only the generated DNA sequence:

.. code-block:: text

   ATCGATCGATCG

Quality Only (``qual``)
~~~~~~~~~~~~~~~~~~~~~~~

Outputs only the quality scores:

.. code-block:: text

   IIIIIIIIIIII

Examples
--------

Basic Examples
~~~~~~~~~~~~~~

Generate a single read:

.. code-block:: bash

   hts-synth ATCGATCGATCGATCG

Generate 10 reads:

.. code-block:: bash

   hts-synth 10 ATCGATCGATCGATCG

Advanced Examples
~~~~~~~~~~~~~~~~~

Generate reads with high error rates:

.. code-block:: bash

   hts-synth --insertion-probability 0.1 \
             --deletion-probability 0.08 \
             --substitution-probability 0.15 \
             5 ATCGATCGATCGATCG

Generate reads starting from a specific reference position:

.. code-block:: bash

   hts-synth --reference-position 1000 10 ATCGATCGATCGATCG

Output only sequences (useful for piping):

.. code-block:: bash

   hts-synth --out-format seq 5 ATCGATCGATCGATCG

Combine with shell commands:

.. code-block:: bash

   # Count the number of reads generated
   hts-synth --out-format seq 100 ATCGATCGATCGATCG | wc -l

   # Save to file
   hts-synth 1000 ATCGATCGATCGATCG > synthetic_reads.fastq

Error Simulation
----------------

The tool simulates three types of sequencing errors:

**Insertions**
   Additional nucleotides inserted into the read that are not present in the reference.

**Deletions**
   Nucleotides from the reference that are missing in the read.

**Substitutions**
   Nucleotides in the read that differ from the corresponding position in the reference.

Each error type has an independent probability that can be configured using the respective command-line options. The error probabilities are applied during read generation to create realistic synthetic sequencing data.

Quality Scores
--------------

The tool automatically generates quality scores for each nucleotide in the synthetic reads. These scores follow standard FASTQ quality encoding and represent the confidence in each base call, simulating the quality scores produced by real sequencing instruments.

Using the NaiveQualModel with WelfordsRunningMean against publicly available data provides the following quality score distribution. The animation below shows the cumulatice mean of the quality sscores showing both the short term variation and the long term trend.

.. image:: ../images/mean-quality-scores.gif
   :alt: Quality score distribution animation
   :align: center

Use Cases
---------

The CLI tool is particularly useful for:

* **Testing sequencing analysis pipelines** with controlled synthetic data
* **Benchmarking alignment algorithms** with reads containing known variants
* **Educational purposes** to understand sequencing errors and their effects
* **Method development** where specific error patterns need to be tested
* **Quality control** by generating reads with known properties
