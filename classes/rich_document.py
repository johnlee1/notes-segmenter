# coding=utf-8

from __future__ import unicode_literals

import re

from llsid_heuristic_mapper import llsid_heuristic_mapper
from text import Text


class FormattedNode(object):
    """
    A node in a tree of formatted text.
    Could be a text token or a formatted item that contains sub-nodes.
    ABSTRACT.
    """
    def __init__(self, tag, offset=None, length=0):
        self.tag = tag
        self.offset = offset
        self.length = length
        self.styles = dict()
        self.fields = []
        self.heuristic_mapper = {
            'default': self.consolidate_runs_default,
            'bold': self.consolidate_runs_using_bold_heuristic,
            'italics': self.consolidate_runs_using_italics_heuristic
        }
        self.default_run_consolidater = self.consolidate_runs_default
    
    def consolidate_runs_with_heuristic(self, llsid):
        if llsid in llsid_heuristic_mapper.keys():
                return self.heuristic_mapper[llsid_heuristic_mapper[llsid]]()
        return self.default_run_consolidater()

    def consolidate_runs(self, suppress_superscripts=True):
        """
        Combine adjacent runs as long as offset correctness can be preserved.
        Barfs if an item lacks an offset.
        :type suppress_superscripts: bool
        :return: a sequence of tuples (offset, text)
        """
        current_offset = 0 if self.offset is None else self.offset
        current_run = ''
        for item in self.enumerate_text_items():
            while current_offset + len(current_run) < item.offset < current_offset + len(current_run) + 5:
                current_run += ' '
            if item.offset is None or current_offset + len(current_run) < item.offset:
                if current_run:
                    yield current_offset, current_run
                current_run = ''
                if item.offset is None:
                    current_offset += len(current_run) + 1
                else:
                    current_offset = item.offset
            text = item.text
            if suppress_superscripts and not current_run.endswith(' ') and item.tag in ('sup', 'sub'):
                text = ' ' * len(text)
            current_run += text
        if current_run:
            yield current_offset, current_run

    def consolidate_runs_default(self, suppress_superscripts=True):
        """
        Combine adjacent runs as long as offset correctness can be preserved.
        Barfs if an item lacks an offset.
        :type suppress_superscripts: bool
        :return: a sequence of tuples (offset, text)
        """
        current_offset = 0 if self.offset is None else self.offset
        current_run = ''
        current_run_texts = []
        for item in self.enumerate_text_items():
            while current_offset + len(current_run) < item.offset < current_offset + len(current_run) + 5:
                current_run += ' '
            if item.offset is None or current_offset + len(current_run) < item.offset:
                if current_run:
                    yield current_run_texts
                current_run = ''
                if item.offset is None:
                    current_offset += len(current_run) + 1
                else:
                    current_offset = item.offset
            text = item.text
            if suppress_superscripts and not current_run.endswith(' ') and item.tag in ('sup', 'sub'):
                text = ' ' * len(text)
            current_run += text
            current_run_texts.append(Text(item.offset, text, 0, len(text)))
        if current_run:
            yield current_run_texts

    def consolidate_runs_using_bold_heuristic(self, suppress_superscripts=True):
        """
        Combine adjacent runs as long as offset correctness can be preserved.
        Barfs if an item lacks an offset.
        :type suppress_superscripts: bool
        :return: a sequence of tuples (offset, text)
        """
        current_offset = 0 if self.offset is None else self.offset
        current_run = ''
        current_run_texts = []
        for item in self.enumerate_text_items():
            while current_offset + len(current_run) < item.offset < current_offset + len(current_run) + 5:
                current_run += ' '
            if item.offset is None or current_offset + len(current_run) < item.offset:
                if current_run:
                    yield current_run_texts
                current_run = ''
                if item.offset is None:
                    current_offset += len(current_run) + 1
                else:
                    current_offset = item.offset
            # bold text -> <BOLD> bold text BOLD_END
            if item.styles.has_key('font-weight') and item.styles['font-weight'] == 'bold':
                text = "<BOLD> " + item.text + " BOLD_END"  
            else:
                text = item.text
            if suppress_superscripts and not current_run.endswith(' ') and item.tag in ('sup', 'sub'):
                text = ' ' * len(text)
            current_run += text
            current_run_texts.append(Text(item.offset, text, 0, len(text)))
        if current_run:
            yield current_run_texts

    def consolidate_runs_using_italics_heuristic(self, suppress_superscripts=True):
        """
        Combine adjacent runs as long as offset correctness can be preserved.
        Barfs if an item lacks an offset.
        :type suppress_superscripts: bool
        :return: a sequence of tuples (offset, text)
        """
        current_offset = 0 if self.offset is None else self.offset
        current_run = ''
        current_run_texts = []
        for item in self.enumerate_text_items():
            while current_offset + len(current_run) < item.offset < current_offset + len(current_run) + 5:
                current_run += ' '
            if item.offset is None or current_offset + len(current_run) < item.offset:
                if current_run:
                    yield current_run_texts
                current_run = ''
                if item.offset is None:
                    current_offset += len(current_run) + 1
                else:
                    current_offset = item.offset
            # italicized text -> <ITALICS> italicized text ITALICS_END
            if item.styles.has_key('font-style') and item.styles['font-style'] == 'italic':
                text = "<ITALICS> " + item.text + " ITALICS_END"  
            else:
                text = item.text
            if suppress_superscripts and not current_run.endswith(' ') and item.tag in ('sup', 'sub'):
                text = ' ' * len(text)
            current_run += text
            current_run_texts.append(Text(item.offset, text, 0, len(text)))
        if current_run:
            yield current_run_texts

    def get_text(self):
        segments = []
        offset = self.offset
        for item in self.enumerate_text_items():
            if offset < item.offset:
                segments.append(' ')
            segments.append(item.text)
            offset = item.offset + item.length
        return ''.join(segments)

    def _find_heading_text_core(self, field, skip_to_first_boxed):
        if field in self.fields:
            return self.get_text(), True
        return '', False

    def enumerate_internal_nodes(self):
        return []

    def enumerate_text_items(self):
        return []


class FormattedTextNode(FormattedNode):
    """
    A TEXT node in a tree of formatted text.
    """
    def __init__(self, text, tag='span', offset=None, length=0, language=None):
        super(FormattedTextNode, self).__init__(tag=tag, offset=offset, length=length)
        self.text = text
        self.language = language
    
    def enumerate_text_items(self):
        yield self


class FormattedInternalNode(FormattedNode):
    """
    An internal node in a tree of formatted text.
    """
    def __init__(self, tag, offset=None, length=0, milestone=None, anchor=None):
        super(FormattedInternalNode, self).__init__(tag, offset=offset, length=length)
        self.items = []
        self.href = None
        self.milestone = milestone
        self.anchor = anchor

    def enumerate_text_items(self):
        for item in self.items:
            for sub_item in item.enumerate_text_items():
                yield sub_item

    def enumerate_internal_nodes(self):
        for item in self.items:
            if isinstance(item, FormattedInternalNode):
                yield item
                for sub_item in item.enumerate_internal_nodes():
                    yield sub_item

    def _find_heading_text_core(self, field, skip_to_first_boxed):
        text, more = '', True
        if self.get_length() == 0:
            return text, more
        if field in self.fields:
            text = self.get_text()
            return text, more
        for item in self.items:
            part, more = item._find_heading_text_core(field, skip_to_first_boxed=skip_to_first_boxed)
            text = concatenate_with_space(text, part)
            if more:
                if text:
                    skip_to_first_boxed[0] = False
                continue
            if not skip_to_first_boxed[0]:
                break
            if len(text) == 0:
                continue
            skip_to_first_boxed[0] = False
            text, more = '', True
        return text, more

    def find_heading_text(self, field='heading', skip_to_first=False):
        text, more = self._find_heading_text_core(field, skip_to_first_boxed=[bool(skip_to_first)])
        return text
