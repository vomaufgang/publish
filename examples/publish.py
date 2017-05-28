from apub.book import Book, Chapter
from apub.output import EbookConvertOutput, HtmlOutput
from apub.substitution import SimpleSubstitution


def main():
    book = Book(
        title='Example',
        authors='Max Mustermann',
        language='en')

    book.chapters.extend(
        [Chapter(source='first_chapter.md'),
         Chapter(source='second_chapter.md')])

    substitution = SimpleSubstitution(
        find='Cows',
        replace_with='Substitutions')

    output = HtmlOutput(
        path='example.html',
        css_path='style.css')
    output.make(book, [substitution])

    output = EbookConvertOutput(
        path='example.epub',
        css_path='style.css')
    output.make(book, [substitution])


if __name__ == '__main__':
    main()
