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

import os

from _hunspell import ffi, lib

class HunspellError(Exception):
    pass

class Hunspell:
    def __init__(self, path, language="en_US"):
        """Initialise library. Takes a path to the .aff and .dic files, and the
        language wanted."""
        base = os.path.join(path, language)
        aff = (base + ".aff").encode("utf8")
        dic = (base + ".dic").encode("utf8")
        if not os.path.exists(aff):
            raise FileNotFoundError("Couldn't find .aff file at " + str(aff))
        if not os.path.exists(dic):
            raise FileNotFoundError("Couldn't find .dic file at " + str(dic))
        self.hun = lib.Hunspell_create(aff, dic)
        if not self.hun:
            raise HunspellError("Failed to initialise Hunspell")

    def check(self, word):
        """Returns True if the word is spelt correctly."""
        if isinstance(word, str):
            word = word.encode("utf8")
        return bool(lib.Hunspell_spell(self.hun, word))

    def suggest(self, word):
        """Returns a list of suggestions for a specified word."""
        enc = False
        if isinstance(word, str):
            word = word.encode("utf8")
            enc = True
        sl = ffi.new("char***")
        n = lib.Hunspell_suggest(self.hun, sl, word)
        if not n:
            return []
        res = [ffi.string(sl[0][i]) for i in range(n)]
        if enc:
            res = [i.decode("utf8") for i in res]
        lib.Hunspell_free_list(self.hun, sl, n)
        return res

    def add(self, word):
        """Add a word to the runtime dictionary.

        Returns True if added successfully.

        Note: this adds to the runtime dictionary *only*, it's not persistent.
        Further, the Hunspell C API we use doesn't seem to provide the
        ability to load multiple dictionaries at the moment, so you can't
        simply use a local dictionary and the system dictionary either. #todo
        """
        if isinstance(word, str):
            word = word.encode("utf8")
        return not lib.Hunspell_add(self.hun, word)

    def __del__(self):
        if hasattr(self, "hun"):
            if self.hun:
                lib.Hunspell_destroy(self.hun)
