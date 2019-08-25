import csv
import sys

HARD_COPY_JOURNAL = "{author}, '{title}' ({year}) {volume} {journal} {page}"
HARD_COPY_JOURNAL_WITH_ISSUE = "{author}, '{title}' ({year}) {volume}({issue}) {journal} {page}"
OFFICIAL_PUBLICATION = "{body}, <i>{title}</i>({year})"
CASE_WITH_NEUTRAL_CITATION = "<i>{case_name}</i> {neutral_citation}"
BOOK="{author}, <i>{title}</i> ({publisher} {year})"
BOOK_LATER_EDITION = "{author}, <i>{title}</i> ({edition} edn, {publisher} {year})"
WEBSITE = "{author}, '{title}' ({date}) &lt;{web}&gt; accessed 18 August 2019"
NEWSPAPER = "{author}, '{title}', <i>{newspaper}</i> ({location}, {date}) &lt;{web}&gt; accessed 18 August 2019"
NGO_REPORT = "{ngo}, <i>{title}</i> ({year})"
STATUTE_WITH_EXTRA = "{title} {extra}"
STATUTE = "{title}"
THESIS = "{author}, <i>{title}</i> ({year})"
PRESS_RELEASE = "{author}, <i>{title}</i> ({year})"
DEBATE = "{}"

file_name = sys.argv[1]


def abbreviate_authors(authors):
    abbreviated_authors = list()
    for author in authors.split(','):
        names = author.strip().split(' ')
        abbreviated_author = names[-1]
        for i in range(0, len(names) - 1):
            abbreviated_author = '%s %s' % (abbreviated_author, names[i][:1])
        abbreviated_authors.append(abbreviated_author)
    return ', '.join(abbreviated_authors)



def _missing(row, key):
    raise Exception("Missing '%s' from %s" % (key, str(row)))


def _get(row, key):
    if row[key] != '':
        return row[key]
    return '<font color="red">*** SOMETHING IS MISSING ***</font>'


def cite_article(row):
    if row['Issue'] == '':
        format_string = HARD_COPY_JOURNAL
    else:
        format_string = HARD_COPY_JOURNAL_WITH_ISSUE

    return format_string.format(
        author=abbreviate_authors(_get(row, 'Authors')),
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
            author=abbreviate_authors(_get(row, 'Authors')),
            title=_get(row, 'Title'),
            publisher=_get(row, 'Book Publisher'),
            year=_get(row, 'Year')
        )
    else:
        return BOOK_LATER_EDITION.format(
            author=abbreviate_authors(_get(row, 'Authors')),
            title=_get(row, 'Title'),
            edition=_get(row, 'Book Edition'),
            publisher=_get(row, 'Book Publisher'),
            year=_get(row, 'Year')
    )


def cite_blog(row):
    return WEBSITE.format(
        author=abbreviate_authors(_get(row, 'Authors')),
        title=_get(row, 'Title'),
        date=_get(row, 'Date').replace(',',''),
        web=_get(row, 'Web')
    )


def cite_newspaper(row):
    return NEWSPAPER.format(
        author=abbreviate_authors(_get(row, 'Authors')),
        title=_get(row, 'Title'),
        newspaper=_get(row, 'Source'),
        location=_get(row, 'Publication location'),
        date=_get(row, 'Date'),
        web=_get(row, 'Web')
    )


def cite_ngo(row):
    return NGO_REPORT.format(
        ngo=_get(row, 'NGO'),
        title=_get(row, 'Title'),
        year=_get(row, 'Year')
    )


def cite_statute(row):
    if '' == row['Extra']:
        return STATUTE.format(
            title=_get(row, 'Title')
        )
    else:
        return STATUTE.format(
            title=_get(row, 'Title'),
            extra=_get(row, 'Extra')
        )


def cite_thesis(row):
    return THESIS.format(
        author=abbreviate_authors(_get(row, 'Authors')),
        title=_get(row, 'Title'),
        year=_get(row, 'Year')
    )


def cite_press_release(row):
    return PRESS_RELEASE.format(
        author=abbreviate_authors(_get(row, 'Authors')),
        title=_get(row, 'Title'),
        year=_get(row, 'Year')
    )


def print_type(type):
    print('<h2>%s</h2>' % type)
    for line in sorted(lines[type]):
        print(line)


with open(file_name, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    lines = dict()
    lines['primary'] = list()
    lines['secondary'] = list()
    lines['cases'] = list()
    lines['statutes'] = list()

    print('<html>')
    for row in reader:
        type = ''
        if 'Article' == row['Type']:
            formatted = cite_article(row)
            type = 'secondary'
        elif 'Govt report' == row['Type']:
            formatted = cite_official_publication(row)
            type = 'secondary'
        elif 'Case' == row['Type']:
            formatted = cite_case(row)
            type = 'cases'
        elif 'Book' == row['Type']:
            formatted = cite_book(row)
            type = 'primary'
        elif 'Blog' == row['Type']:
            formatted = cite_blog(row)
            type = 'secondary'
        elif 'Newspaper article' == row['Type']:
            formatted = cite_newspaper(row)
            type = 'secondary'
        elif 'NGO report' == row['Type']:
            formatted = cite_ngo(row)
            type = 'secondary'
        elif 'Statute' == row['Type']:
            formatted = cite_statute(row)
            type = 'statutes'
        elif 'Thesis' == row['Type']:
            formatted = cite_thesis(row)
            type = 'secondary'
        elif 'Press statement' == row['Type']:
            formatted = cite_press_release(row)
            type = 'secondary'
        else:
            formatted = '<font color="red">Unsupported type: %s</font>' % row['Type']
            type = 'primary'
        lines[type].append('%s</br>' % formatted)

    print_type('primary')
    print_type('secondary')
    print_type('cases')
    print_type('statutes')
    print('</html>')

'''
order:

books (primary sources)
articles (secondary sources)

order by author's surname

case law list
statute list


'''