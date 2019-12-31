"""
Engorgio
========

Architecture
------------

Engorgio is made of a list of entities that run concurrently and exchange
messages among them.

Those entities are started and configured by the module `master`.

Entities
~~~~~~~~

* `scanner`: Find files and directories to be expanded.
* `decompressor`: Expands archives and compressed files.
* `replacer`: Move decompressed files to their final destination.
* `feedbacker`: Provides feedback for the user.
* `metadater`: Generate a file with the metadata lost from the decompression.
* `logger`: Generate a log stream for the user.
* `stopper`: Signal other entities to finish when there is nothing else to do.

"""
