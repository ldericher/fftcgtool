from __future__ import annotations


class Language:
    def __init__(self, language: str):
        language = language.lower()

        # supported languages
        if language in ["de", "es", "fr", "ja", "it"]:
            self.__short = language
        else:
            # everything else is english
            self.__short = "en"

    def __repr__(self):
        return f"Language({self.__short!r})"

    def __str__(self):
        return self.__short

    def __hash__(self) -> hash:
        return hash(str(self))

    def __eq__(self, other: Language):
        return str(self) == str(other)

    @property
    def image_suffix(self):
        # supported languages for face URLs
        if self.__short in ["de", "es", "fr", "it"]:
            return self.__short
        else:
            return "eg"

    @property
    def key_suffix(self):
        # supported languages for Square API
        if self.__short in ["de", "es", "fr", "it"]:
            return f"_{self.__short.upper()}"
        elif self.__short == "ja":
            return ""
        else:
            return "_EN"
