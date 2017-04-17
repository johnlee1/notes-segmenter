class Sentence(object):

    def __init__(self):
        self.texts = []

    def add_text(self, text):
        self.texts.append(text)

    def content(self):
        content = ''
        for text in self.texts:
            content += text.content_from_run_offset()
        return content

    def length(self):
        first_text = self.texts[0]
    	last_text = self.texts[-1]
        first_text_offset = first_text.offset()
        last_text_offset = last_text.offset()
        return last_text_offset - first_text_offset + len(last_text.content_from_run_offset())

    def offset(self):
        first_text = self.texts[0]
    	return first_text.offset()
