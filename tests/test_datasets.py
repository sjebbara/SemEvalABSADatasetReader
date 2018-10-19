from semevalabsa import read_semeval2014
from semevalabsa.datatypes import Dataset, Review, Sentence, Opinion, DatasetFormat


def test_semeval2014():
    parsed_dataset = read_semeval2014("tests/res/semeval2014.xml", aspect_terms=True, aspect_categories=True)

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

    assert parsed_dataset == target_dataset
