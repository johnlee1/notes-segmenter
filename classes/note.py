import sys

from classes.sentence import Sentence

class Note(object):

    def __init__(self, llsid):
        self.llsid = llsid
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def content(self):
        prev_text_offset = sys.maxint
        prev_text_content = ''
        content = ''
        for sentence in self.sentences:
            for text in sentence.texts:
                curr_text_offset = text.offset()
                if prev_text_offset + len(prev_text_content) < curr_text_offset:
                    # add white space because xml assumes it is there based on differences in offsets
                    content += (curr_text_offset - prev_text_offset - len(prev_text_content)) * ' '
                content += text.content_from_run_offset()
                prev_text_offset = text.offset()
                prev_text_content = text.content
        return content

    def content_without_extra_spacing(self):
        content = ''
        for sentence in self.sentences:
            for text in sentence.texts:
                content += text.content
        return content

    def length(self):
        last_sentence = self.sentences[-1]
        first_sentence_offset = self.sentences[0].offset()
        last_sentence_offset = last_sentence.offset()
        return last_sentence_offset - first_sentence_offset + last_sentence.length()

    def offset(self):
        return self.sentences[0].offset()

    def remove_bold_and_italics_indicators(self):
        for sentence in self.sentences:
            for text in sentence.texts:
                text.content = text.content.replace('<BOLD> ', '').replace(' BOLD_END', '').replace('<ITALICS> ', '').replace(' ITALICS_END', '')
        return
