# coding=utf-8

import spacy
import re
import os.path

from id_heuristic_mapper import id_paragraph_heuristic_mapper
from segment_util import *


def write_notes_to_file(data_type_reference, id):
    subdirectory = 'dist'
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass
    with open(os.path.join(subdirectory, 'output-' + id + '-' + data_type_reference + '.txt'), 'w') as f:
        notes = generate_notes(data_type_reference, id)
        for note in notes:
            f.write('\t'.join(note[0:]) + '\n')
    print 'Wrote notes to file for ' + data_type_reference + ', id: ' + id
    return notes


def generate_notes(data_type_reference, id):
    notes = runs_to_notes(data_type_reference, id)
    print 'Generated notes for ' + data_type_reference + ', id: ' + id
    return notes


def runs_to_notes(data_type_reference, id):
    final_notes = []
    consolidatedRuns = consolidate_runs_for_reference(data_type_reference, id) # list of [current_offset, text]
    for consolidatedRun in consolidatedRuns:
        if 0 < len(consolidatedRun):
            texts = consolidatedRun
            sentences = texts_to_sentences(id, texts) 
            notes = sentences_to_notes(id, sentences)
            for note in notes:
                note_item = []
                note_item.append(id)
                note_item.append(str(note.offset()).encode('utf8'))
                note_item.append(str(note.length()).encode('utf8'))
                note_item.append(note.content().encode('utf8'))
                final_notes.append(note_item)

    return final_notes


def consolidate_runs_for_reference(data_type_reference, id):
    """
    :type data_type_reference: string (e.g. 'bible.62.1.1')
    :type id: string (e.g. 'LLS:FSB')
    :return: list of runs
    """
    runs = []
    for reference in ReferenceUtility.enumerate_verses(data_type_reference):
        rich_text_xml = LibraryResources.get_rich_text_for_references(id, [reference])
        documents = RichTextFormattedDocumentReader.parse(rich_text_xml)
        runs = runs + paragraphs_to_runs(documents.paragraphs, id)            
    return runs


def paragraphs_to_runs(paragraphs, id):
    if id in id_paragraph_heuristic_mapper.keys(): # notes can be made up of multiple paragraphs
        runs = []
        if id_paragraph_heuristic_mapper[id] == 'heading_text': # notes are paragraphs with same heading text
            consolidatedParagraphs = consolidate_paragraphs_by_heading_text(paragraphs)
            for consolidatedParagraph in consolidatedParagraphs:
                texts = []
                for formattedInternalNode in consolidatedParagraph:
                    consolidatedRuns = formattedInternalNode.consolidate_runs_with_heuristic(id)
                    for consolidatedRun in consolidatedRuns:
                        texts = texts + consolidatedRun
                runs.append(texts) # a run is a consolidated paragraph
        elif id_paragraph_heuristic_mapper[id] == 'milestone': # notes are paragraphs that belong to the same milestone
            consolidatedParagraphs = consolidate_paragraphs_by_milestone(paragraphs)
            for consolidatedParagraph in consolidatedParagraphs:
                texts = []
                for formattedInternalNode in paragraphs:
                    consolidatedRuns = formattedInternalNode.consolidate_runs_with_heuristic(id)
                    for consolidatedRun in consolidatedRuns:
                        texts = texts + consolidatedRun
                runs.append(texts) # a run is a consolidated paragraph
        else:
            runs = unconsolidated_paragraphs_to_runs(paragraphs, id)
    else:
        runs = unconsolidated_paragraphs_to_runs(paragraphs, id)
    return runs


def consolidate_paragraphs_by_heading_text(formattedInternalNodes):
    consolidatedParagraphs = []
    consolidatedParagraph = []
    headingText = ''
    for formattedInternalNode in formattedInternalNodes:
        currentHeadingText = formattedInternalNode.find_heading_text()
        if currentHeadingText != headingText:
            consolidatedParagraphs.append(consolidatedParagraph)
            consolidatedParagraph = []
            headingText = currentHeadingText
        consolidatedParagraph.append(formattedInternalNode)
    return consolidatedParagraphs


def consolidate_paragraphs_by_milestone(formattedInternalNodes):
    consolidatedParagraphs = []
    consolidatedParagraph = []
    for formattedInternalNode in formattedInternalNodes:
        currentMilestone = formattedInternalNode.milestone
        if currentMilestone == None:
            consolidatedParagraphs.append(consolidatedParagraph)
            consolidatedParagraph = []
        consolidatedParagraph.append(formattedInternalNode)
    return consolidatedParagraphs


def unconsolidated_paragraphs_to_runs(paragraphs, id):
    runs = []
    for formattedInternalNode in paragraphs:
        consolidatedRuns = formattedInternalNode.consolidate_runs_with_heuristic(id)
        for consolidatedRun in consolidatedRuns:
            runs.append(consolidatedRun)
    return runs
