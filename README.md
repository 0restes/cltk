The Classical Language Toolkit
==============================

[![Build Status](https://travis-ci.org/kylepjohnson/cltk.png?branch=master)](https://travis-ci.org/kylepjohnson/cltk)

WARNING: This is an alpha-stage project. Everything should work, but expect braking changes frequently.

About 
-----
The Ancient Greek and Latin languages have not benefited from comprehensive scientific study. The goals of the Classical Language Toolkit (CLTK) are to:

*   Compile analysis-friendly corpora
*   Gather and improve linguistic data required for natural language processing
*   Develop a free, open, stable, and modern platform for generating reproducible research

This project currently consists of a compiler for the corpora of the PHI5, PHI7, and TLG_E disks. The compiler outputs into plaintext JSON files. The TLG's Beta Code is translated into Unicode. Much more functionality will be built into this project as it grows.

INSTALLATION
------------
[CLTK sources are available from PyPI](https://pypi.python.org/pypi/cltk) and installable with pip.

```bash
pip install cltk
```

USE
---
The CLTK is developed in Python 3.3. See example/ for usage.

FUTURE RELEASES
---------------
The Beta Code to Unicode translation needs improvement. This and reading of Beta Code strings within the PHI disks will come in v. 0.0.0.4.

LICENSE
-------
The MIT License (MIT)

Copyright (c) 2014 Kyle P. Johnson
