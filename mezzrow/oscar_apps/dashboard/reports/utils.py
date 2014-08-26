from oscar.apps.dashboard.reports.utils import GeneratorRepository as CoreGeneratorRepository
from site_app.reports import TicketReportGenerator


class GeneratorRepository(CoreGeneratorRepository):

    def __init__(self):
        self.generators = [TicketReportGenerator] + self.generators
