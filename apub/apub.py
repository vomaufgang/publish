#!/usr/bin/python

import markdown
from apub.extensions.markdown import delimitscene


def main():

# todo: test.chapter or text
#    with open('test.chapter', 'r') as f:
#        contents = f.read()

# todo: add a switch to expand single /n to /n/n
#       in case the input file is focuswriter-made and not
#       pure markdown
#    contents = contents.replace('\n', '\n\n')

    #
    configs = {
        'MARKER': ["++"],
        'DELIMITER': ['*']
    }

    html = markdown.markdown("""# Heading
some text

some more text

++ chapter break

text

the end
""",
                             extensions=[delimitscene.DelimitSceneExtension()])
                                 #configs=configs)])
    print(html)
    pass
    # my code here


if __name__ == "__main__":
    main()
