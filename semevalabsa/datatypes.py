from enum import Enum
from typing import List, Optional, Iterable

from semevalabsa import persist

__author__ = 'sjebbara'


class DatasetFormat(Enum):
    SemEval2014 = "semeval2014"
    SemEval2015 = "semeval2015"
    SemEval2016 = "semeval2016"


class Dataset:
    def __init__(self, reviews: List["Review"], dataset_format: DatasetFormat):
        self.reviews = reviews  # type:  List[Review]
        self.dataset_format = dataset_format

    def __iter__(self) -> Iterable["Review"]:
        return iter(self.reviews)

    def __repr__(self):
        return str(self.__dict__)

    def to_file(self, filepath: str, dataset_format: DatasetFormat = None):
        dataset_format = dataset_format or self.dataset_format
        if dataset_format == DatasetFormat.SemEval2014:
            persist.write_2014_reviews(self, filepath)
        elif dataset_format == DatasetFormat.SemEval2015 or dataset_format == DatasetFormat.SemEval2016:
            persist.write_2015_2016_reviews(self, filepath)
        else:
            raise ValueError("Dataset format not supported: '{}'".format(dataset_format))


class Review:
    def __init__(self):
        self.id = None  # type: str
        self.sentences = []  # type:  List[Sentence]
        self.opinions = []  # type:  List[Opinion]

    def __iter__(self) -> Iterable["Sentence"]:
        return iter(self.sentences)

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        s = u"--- Review [{}] ---".format(self.id)
        s += u"\nSentences:"
        for sentence in self.sentences:
            s += u"\n  " + str(sentence)

        if self.opinions:
            s += u"\nText-Level Opinions:"
            for opinion in self.opinions:
                s += u"\n  " + str(opinion)
        return s


class Sentence:
    def __init__(self):
        self.review_id = None  # type:  str
        self.id = None  # type:  str
        self.text = None  # type:  str
        self.out_of_scope = False  # type:  bool
        self.opinions = []  # type:  List[Opinion]

    def __iter__(self) -> Iterable["Opinion"]:
        return iter(self.opinions)

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        s = u"[{}]: '{}'".format(self.id, self.text)
        if self.opinions:
            s += u"\n  Sentence-Level Opinions:"
            for o in self.opinions:
                s += u"\n  " + str(o)
            s += u"\n"
        return s


class Opinion:
    def __init__(self):
        self.target = None  # type:  Optional[str]
        self.category = None  # type:  Optional[str]
        self.entity = None  # type:  Optional[str]
        self.attribute = None  # type:  Optional[str]
        self.polarity = None  # type:  Optional[str]
        self.start = None  # type:  int
        self.end = None  # type:  int

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        if self.target:
            s = u"[{}; {}] '{}' ({}-{})".format(self.category, self.polarity, self.target, self.start, self.end)
        else:
            s = u"[{}; {}]".format(self.category, self.polarity)
        return s
