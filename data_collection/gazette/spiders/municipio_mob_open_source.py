from datetime import datetime, date
from scrapy import Request
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

class UFMunicipioSpider(BaseGazetteSpider):
    name = "municipio_mob_open_source"
    TERRITORY_ID = ""
    allowed_domains = ["api-lagoadotocantins.barcodigital.com.br"]
    # start_urls = ["https://api-lagoadotocantins.barcodigital.com.br/api/publico/diario/calendario"]
    start_urls = ["https://api-recursolandia.barcodigital.com.br/api/publico/diario/calendario"]
    start_date = date(year=2024, month=6, day=1)
    # ToDo: mudar pra 2020
    EDITION_TYPE_NORMAL = 1
    EDITION_TYPE_EXTRA = 2
    EDITION_TYPE_SUPPLEMENT = 3
    

    def start_requests(self):
        initial_date = date(self.start_date.year, self.start_date.month, 1)
        end_date = self.end_date

        periods_of_interest = [
            (date.year, date.month)
            for date in rrule(freq=MONTHLY, dtstart=initial_date, until=end_date)
        ]

        for year, month in periods_of_interest:
            # url = f"https://api-lagoadotocantins.barcodigital.com.br/api/publico/diario/calendario?mes={month}&ano={year}"
            url = f"https://api-recursolandia.barcodigital.com.br/api/publico/diario/calendario?mes={month}&ano={year}"
            yield Request(url)



    def parse(self, response):
        for documents in response.json().values():
            for document in documents:
                yield Gazette(
                    date = datetime.strptime(document.get('data'), "%Y-%m-%d").date(),
                    edition_number = document.get('edicao'),
                    is_extra_edition = document.get('tipo_edicao_id') != self.EDITION_TYPE_NORMAL,
                    # file_urls = [f"https://api-lagoadotocantins.barcodigital.com.br/arquivo/{document.get('url')}"],
                    file_urls = [f"https://api-recursolandia.barcodigital.com.br/arquivo/{document.get('url')}"],
                    power = "executive",
                )