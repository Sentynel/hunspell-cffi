#! /usr/bin/env python3

# Copyright (c) 2016 Sam Lade
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import platform

from cffi import FFI
ffi = FFI()

if platform.system() == "Windows":
    # require a copy of the headers, .dll and .lib here
    # (note the .dll version is required, static won't link for some reason)
    ffi.set_source("_hunspell",
            '#include "hunspell.h"',
            libraries=["libhunspell"])
else:
    ffi.set_source("_hunspell",
            "#include <hunspell/hunspell.h>",
            libraries=["hunspell"],)

ffi.cdef("""
typedef struct Hunhandle Hunhandle;

Hunhandle *Hunspell_create(const char * affpath, const char * dpath);
Hunhandle *Hunspell_create_key(const char * affpath, const char * dpath,
    const char * key);
void Hunspell_destroy(Hunhandle *pHunspell);
int Hunspell_spell(Hunhandle *pHunspell, const char *);
char *Hunspell_get_dic_encoding(Hunhandle *pHunspell);
int Hunspell_suggest(Hunhandle *pHunspell, char*** slst, const char * word);
int Hunspell_analyze(Hunhandle *pHunspell, char*** slst, const char * word);
int Hunspell_stem(Hunhandle *pHunspell, char*** slst, const char * word);
int Hunspell_stem2(Hunhandle *pHunspell, char*** slst, char** desc, int n);
int Hunspell_generate(Hunhandle *pHunspell, char*** slst, const char * word,
    const char * word2);
int Hunspell_generate2(Hunhandle *pHunspell, char*** slst, const char * word,
    char** desc, int n);
int Hunspell_add(Hunhandle *pHunspell, const char * word);
int Hunspell_add_with_affix(Hunhandle *pHunspell, const char * word, const char * example);
int Hunspell_remove(Hunhandle *pHunspell, const char * word);
void Hunspell_free_list(Hunhandle *pHunspell, char *** slst, int n);
""")
if __name__ == "__main__":
    ffi.compile()
