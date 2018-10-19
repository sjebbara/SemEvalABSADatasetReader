from enum import Enum
from typing import List, Iterable

import attr

from semevalabsa import persist

__author__ = 'sjebbara'


class DatasetFormat:
    SemEval2014 = "semeval2014"
    SemEval2015 = "semeval2015"
    SemEval2016 = "semeval2016"


@attr.s
class Dataset:
    reviews = attr.ib(factory=list)  # type:List["Review"]
    dataset_format = attr.ib(default=None, type=str)

    def __len__(self):
        return len(self.reviews)

    def __getitem__(self, item) -> "Review":
        return self.reviews[item]

    def __iter__(self) -> Iterable["Review"]:
        return iter(self.reviews)

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
    id = attr.ib(default=None, type=str)
    sentences = attr.ib(factory=list)  # type:List["Sentence"]
    opinions = attr.ib(factory=list)  # type:List["Opinion"]

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, item) -> "Sentence":
        return self.sentences[item]

    def __iter__(self) -> Iterable["Sentence"]:
        return iter(self.sentences)


@attr.s
class Sentence:
    review_id = attr.ib(default=None, type=str)
    id = attr.ib(default=None, type=str)
    text = attr.ib(default=None, type=str)
    out_of_scope = attr.ib(default=False, type=bool)
    opinions = attr.ib(factory=list)  # type:List["Opinion"]

    def __len__(self):
        return len(self.opinions)

    def __getitem__(self, item) -> "Opinion":
        return self.opinions[item]

    def __iter__(self) -> Iterable["Opinion"]:
        return iter(self.opinions)


@attr.s
class Opinion:
    target = attr.ib(default=None, type=str)
    category = attr.ib(default=None, type=str)
    entity = attr.ib(default=None, type=str)
    attribute = attr.ib(default=None, type=str)
    polarity = attr.ib(default=None, type=str)
    start = attr.ib(default=None, type=int)
    end = attr.ib(default=None, type=int)
