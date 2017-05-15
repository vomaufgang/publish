from apub.book import Book, Chapter
from apub.output import EbookConvertOutput,HtmlOutput
from apub.substitution import SimpleSubstitution


def main():
    book = Book()
    book.title = 'Example'
    book.language = 'en'
    book.authors = 'Max Mustermann'
    # book.cover todo

    chapter = Chapter()
    chapter.source = 'first_chapter.md'

    book.chapters.append(chapter)

    chapter = Chapter()
    chapter.source = 'second_chapter.md'
    book.chapters.append(chapter)

    substitution = SimpleSubstitution()
    substitution.find = 'Cows'
    substitution.replace_with = 'Substitutions'

    output = HtmlOutput()
    output.path = 'example.html'
    output.css_path = 'style.css'

    output.make(book, [substitution])

    output = EbookConvertOutput()
    output.path = 'example.epub'
    output.css_path = 'style.css'

    output.make(book, [substitution])
    # todo You don't even need the project. Get rid of it.
    #      The cli can just pass the book, list of outputs and substitutions
    #      to make, no need to encapsulate 3 parameters.
    #      The json will stay the same, with the cli json.load-ing the
    #      'project' file, but simply passing the three dicts to their
    #      corresponding ctors by itself.
    #      make.make is also only needed by the cli - via the api
    #      it's plain simplet to just call my_output.make.


if __name__ == '__main__':
    main()
