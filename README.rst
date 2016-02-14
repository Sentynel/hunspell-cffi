Hunspell-CFFI
=============

A CFFI-based binding for the Hunspell library. Currently only provides the
basic ability to check spelling and provide suggestions. No built-in dictionary
management either - this is up to you. Compatible dictionaries can be retrieved
from LibreOffice, Firefox, Chrome, etc.

On Linux or OSX, this links against the system provided Hunspell (you'll need
-dev packages or equivalent installed). Windows expects a copy of
libhunspell.dll, libhunspell.lib, and hunspell.h in the build directory; you'll
have to build this yourself. Checking out the git repo and building with Visual
Studio should do the trick; be aware you need the dll build configuration
selected.
