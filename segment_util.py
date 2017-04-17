# coding=utf-8

import re
import copy

from classes.text import Text
from classes.sentence import Sentence
from classes.note import Note


def texts_to_sentences(id, texts):
    """
    Converts texts into sentences
    :type texts: list of texts
    :return: list of sentences
    """
    sentences = []
    sentence = Sentence()
    distance_from_run_offset = 0
    for text in texts:
        content = ''
        beginningOfSentenceOffset = text.run_offset
        chars = text.processed_content()
        for char in chars:
            content = content + char
            distance_from_run_offset += 1

            # if content is only bolded or italicized text, it should not be its own sentence
            contentCopy = copy.deepcopy(content)
            result = re.search('(BOLD_END.*<BOLD>)|(ITALICS_END.*<ITALICS>)', contentCopy)
            final = False
            if result is not None and len(result.group()) > 14:
                final = True

            # if reach a period
            if '.' in char and (('<BOLD>' not in contentCopy[:7] or final) and ('<ITALICS>' not in contentCopy[:10] or final)) or content.count('.') == 2:
                sentence.add_text(Text(text.run_offset, text.content, beginningOfSentenceOffset - text.run_offset, len(content)))
                sentences.append(sentence)
                sentence = Sentence()
                content = ''
                beginningOfSentenceOffset = text.run_offset + distance_from_run_offset

        sentence.add_text(Text(text.run_offset, text.content, beginningOfSentenceOffset - text.run_offset, len(content)))
        distance_from_run_offset = 0

    if content != '':
        sentences.append(sentence)
    return sentences


def sentences_to_notes(id, sentences):
    """
    Sentence segmentation with a sentence that contains bold or italics starting a new note.
    Converts sentences into notes
    :type sentences: list of Sentences
    :return: list of Notes
    """
    notes = []
    note = Note(id)
    boldSeen = False
    italicsSeen = False
    lastItem = sentences[-1].content()
    for sentence in sentences:
        if sentence.content() == ' .' or sentence.content() == ' . ':
            if 0 < len(note.sentences):
                notes.append(note)
            note = Note(id)                       
        if '<BOLD>' in sentence.content() and boldSeen or '<ITALICS>' in sentence.content() and italicsSeen:
            if 0 < len(note.sentences):
                notes.append(note)
            note = Note(id)   
        note.add_sentence(sentence)
        if '<BOLD>' in sentence.content():
            boldSeen = True
        if '<ITALICS>' in sentence.content():
            italicsSeen = True
        elif sentence.content() == lastItem:
            if 0 < len(note.sentences):
                notes.append(note)
            note = Note(id)
    for note in notes:
        note.remove_bold_and_italics_indicators()
    return notes
