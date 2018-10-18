import re
import xml
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from semevalabsa.datatypes import Dataset, Opinion

prettify_fix_re = re.compile("(?<=<text>)\n\s+|\n\s+(?=</text>)")


def _append_2015_2016_opinion_tag(soup, parent_tag, opinion: "Opinion"):
    target = opinion.target
    opinion_tag = soup.new_tag("Opinion", target=target)
    opinion_tag["from"] = opinion.start
    opinion_tag["to"] = opinion.end
    opinion_tag["polarity"] = opinion.polarity
    opinion_tag["category"] = opinion.category
    parent_tag.append(opinion_tag)
    return opinion


def write_2015_2016_reviews(reviews: "Dataset", output_filepath: str):
    review_soup = BeautifulSoup(features='xml')
    reviews_tag = review_soup.new_tag("Reviews")
    review_soup.append(reviews_tag)
    for review in reviews:
        review_tag = review_soup.new_tag("Review", rid=review.id)
        reviews_tag.append(review_tag)

        sentences_tag = review_soup.new_tag("sentences")
        review_tag.append(sentences_tag)
        for sentence in review:
            sentence_tag = review_soup.new_tag("sentence", id=sentence.id)
            if sentence.out_of_scope:
                sentence_tag["OutOfScope"] = "TRUE"
            sentences_tag.append(sentence_tag)

            text_tag = review_soup.new_tag("text")
            text_tag.string = sentence.text
            sentence_tag.append(text_tag)

            opinions_tag = review_soup.new_tag("Opinions")
            sentence_tag.append(opinions_tag)

            if not sentence.out_of_scope:
                for o in sentence.opinions:
                    _append_2015_2016_opinion_tag(review_soup, opinions_tag, o)

        for o in review.opinions:
            _append_2015_2016_opinion_tag(review_soup, review_tag, o)

    with open(output_filepath, "w") as f:
        review_str = review_soup.prettify()
        review_str = prettify_fix_re.sub("", review_str)
        f.write(review_str)


def write_2014_reviews(reviews: "Dataset", output_filepath: str):
    dataset_soup = BeautifulSoup(features='xml')
    sentences_tag = dataset_soup.new_tag("sentences")
    dataset_soup.append(sentences_tag)

    for review in reviews:
        for sentence in review:
            sentence_tag = dataset_soup.new_tag("sentence", id=sentence.id)
            if sentence.out_of_scope:
                sentence_tag["OutOfScope"] = "TRUE"
            sentences_tag.append(sentence_tag)

            text_tag = dataset_soup.new_tag("text")
            text_tag.string = sentence.text
            sentence_tag.append(text_tag)

            terms_tag = dataset_soup.new_tag("aspectTerms")
            sentence_tag.append(terms_tag)

            categories_tag = dataset_soup.new_tag("aspectCategories")
            sentence_tag.append(categories_tag)

            if not sentence.out_of_scope:
                for opinion in sentence:
                    if opinion.target is not None and opinion.start is not None and opinion.end is not None:
                        term_tag = dataset_soup.new_tag("aspectTerm")
                        term_tag["term"] = xml.sax.saxutils.escape(opinion.target)
                        term_tag["from"] = opinion.start
                        term_tag["to"] = opinion.end
                        term_tag["polarity"] = opinion.polarity
                        terms_tag.append(term_tag)

                    if opinion.category is not None:
                        category_tag = dataset_soup.new_tag("aspectCategory")
                        category_tag["category"] = opinion.category
                        category_tag["polarity"] = opinion.polarity
                        categories_tag.append(category_tag)

    with open(output_filepath, "w") as f:
        review_str = dataset_soup.prettify()
        review_str = prettify_fix_re.sub("", review_str)
        f.write(review_str)
