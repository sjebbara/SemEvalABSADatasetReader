from bs4 import BeautifulSoup

__author__ = 'sjebbara'


class Review:
    def __init__(self):
        self.id = None
        self.sentences = []
        self.opinions = []

    def __str__(self):
        s = u"--- Review [{}] ---".format(self.id)
        s += u"\nSentences:"
        for sentence in self.sentences:
            s += u"\n  " + str(sentence)

        if self.opinions:
            s += u"\nText-Level Opinions:"
            for opinion in self.opinions:
                s += u"\n  " + str(opinion)
        return s.encode("utf-8")


class Sentence:
    def __init__(self):
        self.review_id = None
        self.id = None
        self.text = None
        self.out_of_scope = False
        self.opinions = []

    def __str__(self):
        s = u"[{}]: '{}'".format(self.id, self.text)
        if self.opinions:
            s += u"\n  Sentence-Level Opinions:"
            for o in self.opinions:
                s += u"\n  " + str(o)
            s += u"\n"
        return s.encode("utf-8")


class Opinion:
    def __init__(self):
        self.target = None
        self.category = None
        self.entity = None
        self.attribute = None
        self.polarity = None
        self.start = None
        self.end = None

    def __str__(self):
        if self.target:
            s = u"[{}; {}] '{}' ({}-{})".format(self.category, self.polarity, self.target, self.start, self.end)
        else:
            s = u"[{}; {}]".format(self.category, self.polarity)
        return s.encode("utf-8")


def read_semeval2014_task4(filepath, aspect_terms=True, aspect_categories=True):
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, "xml")
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
                        opinion.entity, opinion.attribute = opinion.category.split("#")
                    except (KeyError, ValueError):
                        opinion.category = None
                        opinion.entity = None
                        opinion.attribute = None

                    try:
                        opinion.polarity = c_tag["polarity"]
                    except (KeyError, ValueError):
                        opinion.polarity = None

                    opinion.target = None
                    opinion.start = 0
                    opinion.end = 0

                    sentence.opinions.append(opinion)

            review.sentences.append(sentence)
            reviews.append(review)
    return reviews


def read_semeval2015_task12(filepath):
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, "xml")
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
<<<<<<< HEAD
                        opinion.entity, opinion.attribute = opinion.category.split("#")
                    except (KeyError, ValueError):
=======
                    except KeyError:
>>>>>>> 56cd831b972820151a4820ba2f567e253cd3eec9
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
    return reviews


def read_semeval2016_task5_subtask1(filepath):
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, "xml")
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
                    opinion = Opinion()
                    # category
                    try:
                        opinion.category = o_tag["category"]
<<<<<<< HEAD
                        opinion.entity, opinion.attribute = opinion.category.split("#")
                    except (KeyError, ValueError):
=======
                    except KeyError:
>>>>>>> 56cd831b972820151a4820ba2f567e253cd3eec9
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

                    # target
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
    return reviews


def read_semeval2016_task5_subtask2(filepath):
    reviews = []
    with open(filepath) as f:
        soup = BeautifulSoup(f, "xml")
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
                opinion = Opinion()
                # category
                try:
                    opinion.category = o_tag["category"]
<<<<<<< HEAD
                    opinion.entity, opinion.attribute = opinion.category.split("#")
                except (KeyError, ValueError):
=======
                except KeyError:
>>>>>>> 56cd831b972820151a4820ba2f567e253cd3eec9
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
                review.opinions.append(opinion)
            reviews.append(review)
    return reviews
