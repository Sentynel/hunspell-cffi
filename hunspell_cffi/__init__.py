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
        if not os.path.exists(aff) and os.path.exists(dic):
            raise FileNotFoundError("Couldn't find .aff and .dic files")
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

    def __del__(self):
        if hasattr(self, "hun"):
            if self.hun:
                lib.Hunspell_destroy(self.hun)
