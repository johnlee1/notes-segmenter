import copy
import re

from abbreviations import abbreviations


class Text(object):

    def __init__(self, run_offset, content, distance_from_run_offset, length):
        self.run_offset = run_offset # offset of original xml run
        self.distance_from_run_offset = distance_from_run_offset # distance from beginning of run offset
        self.content = content # text
        self.length = length

    def offset(self):
        return self.run_offset + self.distance_from_run_offset

    def content_from_run_offset(self):
        content_start = self.distance_from_run_offset
        content_end = self.distance_from_run_offset + self.length
        return self.content[content_start:content_end]

    def processed_content(self):
        """
        removes abbreviations
        removes periods from entirely bolded sentences
        replaces bullet points and black circles with period
        """
        regexStr = '\. .*?<BOLD>.*?</BOLD>.*-?\.'
        content = copy.deepcopy(self.content)
        for abbrev in abbreviations:
            content = content.replace(abbrev, len(abbrev) * '^')   
        subs = re.findall(regexStr, content)
        if subs is not None:
            for sub in subs:
                content = text.content.replace(sub, sub[:-1] + ' ')
        return content.replace(u"\u2022", ".").replace(u"\u25CF", ".").replace(u"\u26AB", ".").replace(u"\u2B24", ".")
