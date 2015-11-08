import datetime, pdb, re
import bs4

class ProcurementDocument():
    """Pass in an HTML doc for a City Council procurement. Returns a Python dictionary with procurement information."""

    def __init__(self):

        # dict template
        self.data_dict = {
            "title" : str(),
            "amount" : float(), # use regex to find any number starting with a $ and grab the biggest number since it's total
            "authorization_date" : datetime.date(2000, 1, 1),
            "document_date" : datetime.date(2000, 1, 1),
            "document" : str() # entire body tag
        }

    def to_dict(self, title, html_doc):
        """ This is the main method which is called to return the Python dictionary based on
        the procurement page's title html doc"""

        # store the passed in title
        self.data_dict['title'] = title

        # create beautifulsoup4 object
        self.soup = bs4.BeautifulSoup(html_doc, 'lxml')

        self.data_dict.update(
            {
                "amount" : self._find_amount(),
                "authorization_date" : self._find_authorization_date(),
                "document_date" : self._find_document_date(),
                "document" : self._find_document()
            }
        )

        return self.data_dict

    def _find_document_date(self):
        """Returns the document's creation date as a python date object"""

        # the pattern we'll use to find the string which contains the date
        pattern = re.compile('Item Creation Date: \d{1,2}\/\d{1,2}\/\d{4}')
        # find all items in the span tag
        items = self.soup.find_all('span')

        matches = [] # will store all matched strings
        for item in items:
            match = re.findall(pattern, str(item))
            if match:
                matches.append(match)
        # grab the actual date
        date_ls = matches[0][0].split(' ')[-1].split('/')
        year, month, day = int(date_ls[2]), int(date_ls[0]), int(date_ls[1])

        return datetime.date(year, month, day) # return date object

    def _find_authorization_date(self):
        """Returns the document's authorization date as a python date object"""

        # the pattern we'll use to find the string which contains the date
        pattern = re.compile('Meeting Date: \d{1,2}\/\d{1,2}\/\d{4}')
        # find all items in the span tag
        items = self.soup.find_all('span')

        matches = [] # will store all matched strings
        for item in items:
            match = re.findall(pattern, str(item))
            if match:
                matches.append(match)
        # grab the actual date
        date_ls = matches[0][0].split(' ')[-1].split('/')
        year, month, day = int(date_ls[2]), int(date_ls[0]), int(date_ls[1])

        return datetime.date(year, month, day) # return date object

    def _find_amount(self):
        """Finds the greatest dollar amount in the entire document"""

        pattern = re.compile('(\$(\d*\,){0,}\d{1,3}\.\d{2})')
        items = re.findall(pattern, self.soup.text)
        amounts = []
        for tup in items:
            a1 = tup[0].replace('$', '')
            a1 = a1.replace(',', '')
            amounts.append(float(a1))
        sorted_amounts = sorted(amounts)
        return sorted_amounts[-1]

    def _find_document(self):
        """Finds the body of the document"""

        bod = self.soup.find('body').text.strip()
        return bod
