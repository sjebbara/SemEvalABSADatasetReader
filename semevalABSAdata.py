from bs4 import BeautifulSoup

__author__ = 'sjebbara'


class Review:
	def __init__(self):
		self.id = None
		self.sentences = []
		self.opinions = []

	def __str__(self):
		s = "--- Review [{}] ---".format(self.id)
		s += "\nSentences:"
		for sentence in self.sentences:
			s += "\n  " + str(sentence)

		if self.opinions:
			s += "\nText-Level Opinions:"
			for opinion in self.opinions:
				s += "\n  " + str(opinion)
		return s


class Sentence:
	def __init__(self):
		self.review_id = None
		self.id = None
		self.text = None
		self.opinions = []

	def __str__(self):
		s = "[{}]: '{}'".format(self.id, self.text)
		if self.opinions:
			s += "\n  Sentence-Level Opinions:"
			for o in self.opinions:
				s += "\n  " + str(o)
			s += "\n"
		return s


class SentenceLevelOpinion:
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
			return "[{}; {}] '{}' ({}-{})".format(self.category, self.polarity, self.target, self.start, self.end)
		else:
			return "[{}; {}]".format(self.category, self.polarity)


class TextLevelOpinions:
	def __init__(self):
		self.category = None
		self.entity = None
		self.attribute = None
		self.polarity = None

	def __str__(self):
		return "[{}; {}]".format(self.category, self.polarity)


def read_semeval2015_task12(filename):
	reviews = []
	with open(filename) as f:
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
					opinion = SentenceLevelOpinion()
					opinion.category = o_tag["category"]
					opinion.entity, opinion.attribute = opinion.category.split("#")
					opinion.polarity = o_tag["polarity"]

					try:
						opinion.target = o_tag["target"]
						if opinion.target == "NULL":
							opinion.target = None
						else:
							opinion.start = int(o_tag["from"])
							opinion.end = int(o_tag["to"])
					except KeyError as e:
						pass
					sentence.opinions.append(opinion)
				review.sentences.append(sentence)
			reviews.append(review)
	return reviews


def read_semeval2016_task5_subtask1(filename):
	reviews = []
	with open(filename) as f:
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
					opinion = SentenceLevelOpinion()
					opinion.category = o_tag["category"]
					opinion.entity, opinion.attribute = opinion.category.split("#")
					opinion.polarity = o_tag["polarity"]

					try:
						opinion.target = o_tag["target"]
						if opinion.target == "NULL":
							opinion.target = None
						else:
							opinion.start = int(o_tag["from"])
							opinion.end = int(o_tag["to"])
					except KeyError as e:
						pass
					sentence.opinions.append(opinion)
				review.sentences.append(sentence)
			reviews.append(review)
	return reviews


def read_semeval2016_task5_subtask2(filename):
	reviews = []
	with open(filename) as f:
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
				opinion = SentenceLevelOpinion()
				opinion.category = o_tag["category"]
				opinion.entity, opinion.attribute = opinion.category.split("#")
				opinion.polarity = o_tag["polarity"]
				review.opinions.append(opinion)
			reviews.append(review)
	return reviews
