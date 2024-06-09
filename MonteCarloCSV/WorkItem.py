class WorkItem:
    def __init__(self, closed_date):
        self.closed_date = closed_date
            
    def to_dict(self):
            return {
                'closed_date': self.closed_date.date(),
            }