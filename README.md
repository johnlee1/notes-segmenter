# Notes Segmenter

### What it does
Given a data type reference and a ID, the notes segmenter makes a call to a Resources Api to obtain rich text xml for the data type reference and ID. It parses the XML and segments the results into notes.

### Prereqs
- python 2.7

### How it works
- A `Text` contains an offset and and text content
- A `Sentence` is made up of `Text`s
- A `Note` is made up of `Sentence`s
- Rich xml is parsed and converted to runs. The runs are consolidated. Runs are converted to `text`s. `Text`s are converted to `sentence`s. `Sentence`s are converted to `note`s.
- By default, notes will be segmented such that each note is a consolidated runs. If the `id` being used exists in the `id_heuristic_mapper` or `id_paragraph_heuristic_mapper`, then the heuristic specified in the mapper will be used. 
- Currently the heuristics for segmenting notes are:
  - consolidated runs
  - bold text
  - italics text
  - paragraphs with same the heading text
  - paragraphs with the same milestone
  
### Developing
- Add new non-paragraph-based heuristics to `id_heuristic_mapper.py` and to the init method in `classes/rich_document.py`. 
- Add new paragraph-based heuristics to `id_heuristic_mapper.py` and to `paragraphs_to_runs` in `notes_segmenter.py`.
- If an abbreviation is interfering with sentence segmentation, add it to the list of abbreviations in `abbreviations.py`.

### Usage
- Use `write_notes_to_file` or `generate_notes` in `notes-segmenter.py`.
