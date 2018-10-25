import os

from pytest import fixture

from semevalabsa import read_semeval2014
from semevalabsa.datatypes import Dataset, Review, Sentence, Opinion, DatasetFormat


@fixture
def semeval2014_dataset():
    r1 = Review(id="Review_1",
                sentences=[
                    Sentence(review_id="Review_1", id="1", text="This is a test sentence.", out_of_scope=False,
                             opinions=[
                                 Opinion(target="sentence", polarity="neutral", start=15, end=23),
                                 Opinion(category="TEST", polarity="negative"),
                             ])
                ])
    r2 = Review(id="Review_2",
                sentences=[
                    Sentence(review_id="Review_2", id="2", text="Another sentence for testing purposes", out_of_scope=False,
                             opinions=[
                                 Opinion(target="sentence", polarity="positive", start=8, end=16),
                                 Opinion(target="purposes", polarity="positive", start=29, end=37),
                                 Opinion(category="PURPOSE", polarity="positive"),
                                 Opinion(category="ANOTHER", polarity="negative"),
                             ])
                ])
    target_dataset = Dataset([r1, r2], dataset_format=DatasetFormat.SemEval2014)
    return target_dataset


def test_parsing_semeval2014(semeval2014_dataset):
    parsed_dataset = read_semeval2014("tests/res/semeval2014.xml", aspect_terms=True, aspect_categories=True)

    assert semeval2014_dataset == parsed_dataset


def test_persist_and_parse_semeval2014(semeval2014_dataset):
    tmp_dataset_filepath = ".tmp_semeval2014.xml"
    semeval2014_dataset.to_file(tmp_dataset_filepath)
    parsed_dataset = read_semeval2014(tmp_dataset_filepath, aspect_terms=True, aspect_categories=True)
    os.remove(tmp_dataset_filepath)

    assert semeval2014_dataset == parsed_dataset
