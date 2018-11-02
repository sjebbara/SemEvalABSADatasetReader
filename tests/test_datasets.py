import os

from pytest import fixture

from semevalabsa import read_semeval2014, read_sentihood
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


@fixture
def sentihood_dataset():
    r1 = Review(id="Review_1244",
                sentences=[
                    Sentence(review_id="Review_1244", id=1244, text="  And LOCATION1 is ten mins direct on the tube to LOCATION2:  ",
                             out_of_scope=False,
                             opinions=[
                                 Opinion(target="LOCATION1", category="transit-location", polarity="Positive", start=6, end=15),
                             ])
                ])
    r2 = Review(id="Review_209",
                sentences=[
                    Sentence(review_id="Review_209", id=209,
                             text="  Another option is LOCATION1 which is very central and has tons of clubs/bars within walking distance of each other",
                             out_of_scope=False,
                             opinions=[
                                 Opinion(target="LOCATION1", category="nightlife", polarity="Positive", start=20, end=29),
                                 Opinion(target="LOCATION1", category="transit-location", polarity="Positive", start=20, end=29),
                             ])
                ])
    target_dataset = Dataset([r1, r2], dataset_format=DatasetFormat.SentiHood)
    return target_dataset


def test_parsing_sentihood(sentihood_dataset):
    parsed_dataset = read_sentihood("tests/res/sentihood.json")

    assert sentihood_dataset == parsed_dataset

# def test_persist_and_parse_sentihood(sentihood_dataset):
#     tmp_dataset_filepath = ".tmp_sentihood.json"
#     sentihood_dataset.to_file(tmp_dataset_filepath)
#     parsed_dataset = read_sentihood("tests/res/sentihood.json")
#     os.remove(tmp_dataset_filepath)
#
#     assert sentihood_dataset == parsed_dataset
