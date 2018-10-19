from enum import Enum
from typing import List, Iterable

import attr

from semevalabsa import persist

__author__ = 'sjebbara'


class DatasetFormat(Enum):
    SemEval2014 = "semeval2014"
    SemEval2015 = "semeval2015"
    SemEval2016 = "semeval2016"


@attr.s
class Dataset:
    reviews = attr.ib(factory=list)  # type:List["Review"]
    dataset_format = attr.ib(default=None, type=DatasetFormat)

    # def __init__(self, reviews: List["Review"], dataset_format: DatasetFormat):
    #     self.reviews = reviews  # type:  List[Review]
    #     self.dataset_format = dataset_format
    #
    # def __iter__(self) -> Iterable["Review"]:
    #     return iter(self.reviews)
    #
    # def __repr__(self):
    #     return str(self.__dict__)

    def to_file(self, filepath: str, dataset_format: DatasetFormat = None):
        dataset_format = dataset_format or self.dataset_format
        if dataset_format == DatasetFormat.SemEval2014:
            persist.write_2014_reviews(self, filepath)
        elif dataset_format == DatasetFormat.SemEval2015 or dataset_format == DatasetFormat.SemEval2016:
            persist.write_2015_2016_reviews(self, filepath)
        else:
            raise ValueError("Dataset format not supported: '{}'".format(dataset_format))


@attr.s
class Review:
    review_id = attr.ib(default=None, type=str)
    sentences = attr.ib(factory=list)  # type:List["Sentence"]
    opinions = attr.ib(factory=list)  # type:List["Opinion"]

    def __iter__(self) -> Iterable["Sentence"]:
        return iter(self.sentences)

    # def __init__(self, review_id: str = None, sentences: List["Sentence"] = None, opinions: List["Opinion"] = None):
    #     self.id = review_id
    #     self.sentences = sentences or []
    #     self.opinions = opinions or []
    #
    # def __repr__(self):
    #     return str(self.__dict__)
    #
    # def __str__(self):
    #     s = u"--- Review [{}] ---".format(self.id)
    #     s += u"\nSentences:"
    #     for sentence in self.sentences:
    #         s += u"\n  " + str(sentence)
    #
    #     if self.opinions:
    #         s += u"\nText-Level Opinions:"
    #         for opinion in self.opinions:
    #             s += u"\n  " + str(opinion)
    #     return s
    #
    # def __eq__(self, other):
    #     if not isinstance(other, Review):
    #         return False
    #     elif self.id != other.id:
    #         return False
    #     elif self.id != other.id:
    #         return False
    #     elif self.id != other.id:
    #         return False
    #     return True


@attr.s
class Sentence:
    review_id = attr.ib(default=None, type=str)
    id = attr.ib(default=None, type=str)
    text = attr.ib(default=None, type=str)
    out_of_scope = attr.ib(default=False, type=bool)
    opinions = attr.ib(factory=list)  # type:List["Opinion"]

    def __iter__(self) -> Iterable["Opinion"]:
        return iter(self.opinions)

    # def __init__(self, review_id: str = None, sentence_id: str = None, text: str = None, out_of_scope: bool = False,
    #              opinions: List["Opinion"] = None):
    #     self.review_id = review_id
    #     self.id = sentence_id
    #     self.text = text
    #     self.out_of_scope = out_of_scope
    #     self.opinions = opinions or []
    #
    # def __repr__(self):
    #     return str(self.__dict__)
    #
    # def __str__(self):
    #     s = u"[{}]: '{}'".format(self.id, self.text)
    #     if self.opinions:
    #         s += u"\n  Sentence-Level Opinions:"
    #         for o in self.opinions:
    #             s += u"\n  " + str(o)
    #         s += u"\n"
    #     return s


@attr.s
class Opinion:
    target = attr.ib(default=None, type=str)
    category = attr.ib(default=None, type=str)
    entity = attr.ib(default=None, type=str)
    attribute = attr.ib(default=None, type=str)
    polarity = attr.ib(default=None, type=str)
    start = attr.ib(default=None, type=int)
    end = attr.ib(default=None, type=int)
    # def __init__(self, target: str = None, category: str = None, entity: str = None, attribute: str = None, polarity: str = None, start: int = None,
    #              end: int = None):
    #     self.target = target
    #     self.category = category
    #     self.entity = entity
    #     self.attribute = attribute
    #     self.polarity = polarity
    #     self.start = start
    #     self.end = end

    # def __repr__(self):
    #     return str(self.__dict__)

    # def __str__(self):
    #     if self.target:
    #         s = u"[{}; {}] '{}' ({}-{})".format(self.category, self.polarity, self.target, self.start, self.end)
    #     else:
    #         s = u"[{}; {}]".format(self.category, self.polarity)
    #     return s
