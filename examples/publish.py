from apub.book import Book, Chapter
from apub.output import EbookConvertOutput,HtmlOutput
from apub.substitution import SimpleSubstitution


def main():
    book = Book()
    book.title = 'Example'
    book.language = 'en'
    book.authors = 'Max Mustermann'

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


if __name__ == '__main__':
    main()
