from datetime import datetime

def calculate_penalty(preferred_datetime, slot):
    penalty = abs((preferred_datetime - slot).total_seconds())
    return penalty