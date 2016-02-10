#! /usr/bin/env python3
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
