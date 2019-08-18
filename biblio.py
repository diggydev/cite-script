import csv
import sys

HARD_COPY_JOURNAL = "{author}, '{title}' ({year}) {volume} {journal} {page}"
HARD_COPY_JOURNAL_WITH_ISSUE = "{author}, '{title}' ({year}) {volume}({issue}) {journal} {page}"
OFFICIAL_PUBLICATION = "{body}, <i>{title}</i>({year})"
CASE_WITH_NEUTRAL_CITATION = "<i>{case_name}</i> [{year}] {neutral_citation}, [{year}] {volume} {report_abbreviation} {page}</i>"
BOOK="{author}, <i>{title}</i> ({publisher} {year})"
BOOK_LATER_EDITION = "{author}, <i>{title}</i> ({edition} edn, {publisher} {year})"
WEBSITE = "{author}, '{title}' ({date}) &lt;{web}&gt; accessed 18 August 2019"
NEWSPAPER = "{author}, '{title}', <i>{newspaper}</i> ({location}, {date}) &lt;{web}&gt; accessed 18 August 2019"

file_name = sys.argv[1]


def _missing(row, key):
    raise Exception("Missing '%s' from %s" % (key, str(row)))


def _get(row, key):
    if row[key] != '':
        return row[key]
    return '*** SOMETHING IS MISSING ***'


def cite_article(row):
    if row['Issue'] == '':
        format_string = HARD_COPY_JOURNAL
    else:
        format_string = HARD_COPY_JOURNAL_WITH_ISSUE

    return format_string.format(
        author=_get(row, 'Authors'),
        title=_get(row, 'Title'),
        year=_get(row, 'Year'),
        volume=_get(row, 'Volume'),
        issue=_get(row, 'Issue'),
        journal=_get(row, 'Source'),
        page=_get(row, 'Start Page')
    )


def cite_official_publication(row):
    return OFFICIAL_PUBLICATION.format(
        body=_get(row, 'Authors'),
        title=_get(row, 'Title'),
        year=_get(row, 'Year')
    )


def cite_case(row):
    return CASE_WITH_NEUTRAL_CITATION.format(
        case_name=_get(row, 'Title'),
        year=_get(row, 'Year'),
        neutral_citation=_get(row, 'Source Details'),
        volume=_get(row, 'Volume'),
        report_abbreviation=_get(row, 'Source Details'),
        page=_get(row, 'Start Page')
    )


def cite_book(row):
    if '1st' == _get(row, 'Book Edition'):
        return BOOK.format(
            author=_get(row, 'Authors'),
            title=_get(row, 'Title'),
            publisher=_get(row, 'Book Publisher'),
            year=_get(row, 'Year')
        )
    else:
        return BOOK_LATER_EDITION.format(
            author=_get(row, 'Authors'),
            title=_get(row, 'Title'),
            edition=_get(row, 'Book Edition'),
            publisher=_get(row, 'Book Publisher'),
            year=_get(row, 'Year')
    )


def cite_blog(row):
    return WEBSITE.format(
        author=_get(row, 'Authors'),
        title=_get(row, 'Title'),
        date=_get(row, 'Date').replace(',',''),
        web=_get(row, 'Web')
    )


def cite_newspaper(row):
    return NEWSPAPER.format(
        author=_get(row, 'Authors'),
        title=_get(row, 'Title'),
        newspaper=_get(row, 'Source'),
        location=_get(row, 'Publication location'),
        date=_get(row, 'Date'),
        web=_get(row, 'Web')
    )


with open(file_name, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    print('<html>')
    for row in reader:
        if 'Article' == row['Type']:
            formatted = cite_article(row)
        elif 'Govt report' == row['Type']:
            formatted = cite_official_publication(row)
        elif 'Case' == row['Type']:
            formatted = cite_case(row)
        elif 'Book' == row['Type']:
            formatted = cite_book(row)
        elif 'Blog' == row['Type']:
            formatted = cite_blog(row)
        elif 'Newspaper article' == row['Type']:
            formatted = cite_newspaper(row)
        else:
            formatted = 'Unsupported type: %s' % row['Type']
        print('%s</br>' % formatted)

    print('</html>')
