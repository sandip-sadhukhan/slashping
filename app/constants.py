from enum import Enum
from lib.decorators import forDjango

@forDjango
class CustomerTabs(Enum):
    PENDING_TODAY = 'pending_today'
    PENDING_TOMORROW = 'pending_tomorrow'
    ALL_CLIENTS = 'all_clients'