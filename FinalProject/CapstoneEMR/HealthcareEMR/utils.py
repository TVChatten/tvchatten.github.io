#Calculating the penalty for the appointment time based on what the Patient suggests against what the doctor has available.
from datetime import datetime

def calculate_penalty(preferred_datetime, slot):
    penalty = abs((preferred_datetime - slot).total_seconds())
    return penalty