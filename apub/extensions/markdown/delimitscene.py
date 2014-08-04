from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


class DelimitSceneExtension(Extension):
    """ Chapter Break extension for Python-Markdown. """

    def __init__(self, configs=None):
        default_configs = {
            'MARKUP': ['++',
                       'Any block that starts with this string will be '
                       'turned into a scene break. All further content of'
                       'such a block will be discarded.'],
            'DELIMITER': ['*',
                          'The text to be used as the scene delimiter'],
            'CSS_CLASS': ['scene_delimiter',
                          'The class[es] applied to the scene delimiter'
                          'html element'],
            'HTML_ELEMENT': ['p',
                             'The html element used for the scene delimiter']
        }

        if configs is None:
            configs = default_configs
        else:
            configs = default_configs.copy().update(configs)

        super(DelimitSceneExtension, self).__init__(configs)

    def extendMarkdown(self, md, md_globals):
        """ Add delimit scene processor to Markdown instance. """
        processor = DelimitSceneProcessor(md.parser)
        processor.config = self.getConfigs()
        md.parser.blockprocessors.add('delimitscene', processor, '_begin')

        md.registerExtension(self)


class DelimitSceneProcessor(BlockProcessor):
    def test(self, parent, block):
        return block.startswith(self.config['MARKUP'])

    def run(self, parent, blocks):
        block = blocks.pop(0)

        if block.startswith(self.config['MARKUP']):
            p = etree.SubElement(parent, 'p')
            p.set('class', 'scene_delimiter')
            p.text = self.config['DELIMITER']