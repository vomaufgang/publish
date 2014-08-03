from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


class ChapterBreakExtension(Extension):
    """ Chapter Break extension for Python-Markdown. """

    def __init__(self, *args, **kwargs):
        self.config = {
            'MARKER': ["++", 'Any block that starts with this will be ' +
                             'turned into a chapter break.'],
            'CHAPTER_BREAK': ['*', 'The text to be used as a chapter break']
        }
        super(ChapterBreakExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add Chapter Break to Markdown instance. """
        md.registerExtension(self)

        md.parser.blockprocessors.add('chapterbreak',
                                      ChapterBreakProcessor(self),
                                      '_begin')


class ChapterBreakProcessor(BlockProcessor):

    def __init__(self, extension):
        self.extension = extension

    def test(self, parent, block):
        return block.startswith(self.extension.getConfig('MARKER'))

    def run(self, parent, blocks):
        block = blocks.pop(0)

        if block.startswith(self.extension.getConfig('MARKER')):
            p = etree.SubElement(parent, 'p')
            p.set('class', 'centered chapter_break')
            p.text = self.extension.getConfig('CHAPTER_BREAK')