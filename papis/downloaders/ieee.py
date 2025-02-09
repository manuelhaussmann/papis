import re
from typing import Optional, Tuple, Dict

import papis.downloaders.base


class Downloader(papis.downloaders.Downloader):

    def __init__(self, url: str):
        papis.downloaders.Downloader.__init__(self, url, name="ieee")
        self.expected_document_extension = 'pdf'

    @classmethod
    def match(cls, url: str) -> Optional[papis.downloaders.Downloader]:
        m = re.match(r"^ieee:(.*)", url, re.IGNORECASE)
        if m:
            url = "http://ieeexplore.ieee.org/document/{}".format(m.group(1))
            return Downloader(url)
        if re.match(r".*ieee.org.*", url):
            url = re.sub(r"\.pdf.*$", "", url)
            return Downloader(url)
        else:
            return None

    def get_identifier(self) -> str:
        url = self.uri
        return re.sub(r'^.*ieeexplore\.ieee\.org/document/(.*)\/', r'\1', url)

    def _get_bibtex_url(self) -> Tuple[str, Dict[str, str]]:
        identifier = self.get_identifier()
        bibtex_url = \
            'http://ieeexplore.ieee.org/xpl/downloadCitations?reload=true'
        data = {
            'recordIds': identifier,
            'citations-format': 'citation-and-abstract',
            'download-format': 'download-bibtex',
            'x': '0',
            'y': '0'
        }
        return bibtex_url, data

    def download_bibtex(self) -> None:
        import urllib.parse
        import urllib.request

        bib_url, values = self._get_bibtex_url()
        post_data = urllib.parse.urlencode(values).encode('ascii')

        self.logger.debug("bibtex url = '%s'", bib_url)

        req = urllib.request.Request(bib_url, post_data)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            text = data.decode('utf-8')
            text = text.replace('<br>', '')
            self.bibtex_data = text

    def get_document_url(self) -> Optional[str]:
        identifier = self.get_identifier()
        self.logger.debug("paper id = '%s'", identifier)
        pdf_url = "{}{}{}".format(
            "http://ieeexplore.ieee.org/",
            "stampPDF/getPDF.jsp?tp=&isnumber=&arnumber=",
            identifier)
        self.logger.debug("pdf url = '%s'", pdf_url)
        return pdf_url
