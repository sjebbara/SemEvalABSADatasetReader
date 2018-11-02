import json

from bs4 import BeautifulSoup

from semevalabsa.datatypes import Review, Sentence, Opinion, Dataset, DatasetFormat

__author__ = 'sjebbara'


def read_sentihood(filepath: str) -> Dataset:
    reviews = []
    with open(filepath) as f:
        json_dataset = json.load(f)

        for json_sentence in json_dataset:
            sentence = Sentence()
            sentence.id = json_sentence["id"]

            # dummy review
            review = Review()
            review.id = "Review_{}".format(sentence.id)
            sentence.review_id = review.id

            sentence.text = json_sentence["text"]

            for json_opinion in json_sentence["opinions"]:
                opinion = Opinion()

                opinion.polarity = json_opinion["sentiment"]

                opinion.category = json_opinion["aspect"]
                opinion.entity = None
                opinion.attribute = None

                opinion.target = json_opinion["target_entity"]

                try:
                    opinion.start = sentence.text.index(opinion.target)
                    opinion.end = opinion.start + len(opinion.target)
                except ValueError as e:
                    opinion.start = None
                    opinion.end = None

                sentence.opinions.append(opinion)

            review.sentences.append(sentence)
            reviews.append(review)
    return Dataset(reviews, DatasetFormat.SentiHood)


def read_semeval2014(filepath: str, aspect_terms: bool = True, aspect_categories: bool = True) -> Dataset:
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, features="xml")
        sentence_tags = soup.find_all("sentence")
        for s_tag in sentence_tags:
            sentence = Sentence()
            sentence.id = s_tag["id"]

            # dummy review
            review = Review()
            review.id = "Review_" + sentence.id

            sentence.review_id = review.id
            sentence.text = s_tag.find("text").get_text()

            if aspect_terms:
                aspect_term_tags = s_tag.find_all("aspectTerm")
                for a_tag in aspect_term_tags:
                    opinion = Opinion()

                    opinion.category = None
                    opinion.entity = None
                    opinion.attribute = None

                    try:
                        opinion.polarity = a_tag["polarity"]
                    except (KeyError, ValueError):
                        opinion.polarity = None

                    try:
                        opinion.target = a_tag["term"]
                        if opinion.target == "NULL":
                            opinion.target = None
                        else:
                            opinion.start = int(a_tag["from"])
                            opinion.end = int(a_tag["to"])
                    except (KeyError, ValueError):
                        pass
                    sentence.opinions.append(opinion)

            if aspect_categories:
                aspect_category_tags = s_tag.find_all("aspectCategory")
                for c_tag in aspect_category_tags:
                    opinion = Opinion()

                    try:
                        opinion.category = c_tag["category"]
                    except (KeyError, ValueError):
                        opinion.category = None

                    try:
                        opinion.entity, opinion.attribute = opinion.category.split("#")
                    except (KeyError, ValueError):
                        opinion.entity = None
                        opinion.attribute = None

                    try:
                        opinion.polarity = c_tag["polarity"]
                    except (KeyError, ValueError):
                        opinion.polarity = None

                    opinion.target = None
                    opinion.start = None
                    opinion.end = None

                    sentence.opinions.append(opinion)

            review.sentences.append(sentence)
            reviews.append(review)
    return Dataset(reviews, DatasetFormat.SemEval2014)


def read_semeval2015(filepath: str) -> Dataset:
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, features="xml")
        review_tags = soup.find_all("Review")
        for j, r_tag in enumerate(review_tags):
            review = Review()
            review.id = r_tag["rid"]
            sentence_tags = r_tag.find_all("sentence")
            for s_tag in sentence_tags:
                sentence = Sentence()
                sentence.review_id = review.id
                sentence.id = s_tag["id"]
                sentence.text = s_tag.find("text").get_text()
                opinion_tags = s_tag.find_all("Opinion")
                for o_tag in opinion_tags:
                    opinion = Opinion()

                    # category
                    try:
                        opinion.category = o_tag["category"]
                        opinion.entity, opinion.attribute = opinion.category.split("#")
                    except (KeyError, ValueError):
                        opinion.category = None

                    # entity + attribute
                    if opinion.category and "#" in opinion.category:
                        opinion.entity, opinion.attribute = opinion.category.split("#")
                    else:
                        opinion.entity = None
                        opinion.attribute = None

                    # polarity
                    try:
                        opinion.polarity = o_tag["polarity"]
                    except (KeyError, ValueError):
                        opinion.polarity = None

                    try:
                        opinion.target = o_tag["target"]
                        if opinion.target == "NULL":
                            opinion.target = None
                        else:
                            opinion.start = int(o_tag["from"])
                            opinion.end = int(o_tag["to"])
                    except (KeyError, ValueError):
                        pass
                    sentence.opinions.append(opinion)
                review.sentences.append(sentence)
            reviews.append(review)
    return Dataset(reviews, DatasetFormat.SemEval2015)


def read_semeval2016(filepath: str) -> Dataset:
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, features="xml")
        review_tags = soup.find_all("Review")
        for j, r_tag in enumerate(review_tags):
            review = Review()
            review.id = r_tag["rid"]
            sentence_tags = r_tag.find_all("sentence")
            for s_tag in sentence_tags:
                sentence = Sentence()
                sentence.review_id = review.id
                sentence.id = s_tag["id"]
                sentence.text = s_tag.find("text").get_text()
                try:
                    sentence.out_of_scope = s_tag["OutOfScope"]
                except (KeyError, ValueError):
                    sentence.out_of_scope = False

                sentence_opinion_tags = s_tag.find("Opinions", recursive=False)
                sentence_opinion_tags = sentence_opinion_tags.find_all("Opinion", recursive=False) if sentence_opinion_tags else []

                for o_tag in sentence_opinion_tags:
                    opinion = _build_opinion(o_tag)
                    sentence.opinions.append(opinion)
                review.sentences.append(sentence)

            review_opinion_tags = r_tag.find("Opinions", recursive=False)
            review_opinion_tags = review_opinion_tags.find_all("Opinion", recursive=False) if review_opinion_tags else []
            for o_tag in review_opinion_tags:
                opinion = _build_opinion(o_tag)
                review.opinions.append(opinion)

            reviews.append(review)
    return Dataset(reviews, DatasetFormat.SemEval2016)


def read_semeval2016_task5_subtask1(filepath: str) -> Dataset:
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, features="xml")
        review_tags = soup.find_all("Review")
        for j, r_tag in enumerate(review_tags):
            review = Review()
            review.id = r_tag["rid"]
            sentence_tags = r_tag.find_all("sentence")
            for s_tag in sentence_tags:
                sentence = Sentence()
                sentence.review_id = review.id
                sentence.id = s_tag["id"]
                sentence.text = s_tag.find("text").get_text()
                try:
                    sentence.out_of_scope = s_tag["OutOfScope"]
                except (KeyError, ValueError):
                    sentence.out_of_scope = False

                opinion_tags = s_tag.find_all("Opinion")
                for o_tag in opinion_tags:
                    opinion = _build_opinion(o_tag)
                    sentence.opinions.append(opinion)
                review.sentences.append(sentence)
            reviews.append(review)
    return Dataset(reviews, DatasetFormat.SemEval2016)


def read_semeval2016_task5_subtask2(filepath: str) -> Dataset:
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, features="xml")
        review_tags = soup.find_all("Review")
        for j, r_tag in enumerate(review_tags):
            review = Review()
            review.id = r_tag["rid"]
            sentence_tags = r_tag.find_all("sentence")
            for s_tag in sentence_tags:
                sentence = Sentence()
                sentence.review_id = review.id
                sentence.id = s_tag["id"]
                sentence.text = s_tag.find("text").get_text()
                review.sentences.append(sentence)

            opinion_tags = r_tag.find_all("Opinion")
            for o_tag in opinion_tags:
                opinion = _build_opinion(o_tag)
                review.opinions.append(opinion)
            reviews.append(review)
    return Dataset(reviews, DatasetFormat.SemEval2016)


def _build_opinion(opinion_tag) -> Opinion:
    opinion = Opinion()
    # category
    try:
        opinion.category = opinion_tag["category"]
        opinion.entity, opinion.attribute = opinion.category.split("#")
    except (KeyError, ValueError):
        opinion.category = None

    # entity + attribute
    if opinion.category and "#" in opinion.category:
        opinion.entity, opinion.attribute = opinion.category.split("#")
    else:
        opinion.entity = None
        opinion.attribute = None

    # polarity
    try:
        opinion.polarity = opinion_tag["polarity"]
    except (KeyError, ValueError):
        opinion.polarity = None

    # target
    try:
        opinion.target = opinion_tag["target"]
        if opinion.target == "NULL":
            opinion.target = None
        else:
            opinion.start = int(opinion_tag["from"])
            opinion.end = int(opinion_tag["to"])
    except (KeyError, ValueError):
        pass

    return opinion
