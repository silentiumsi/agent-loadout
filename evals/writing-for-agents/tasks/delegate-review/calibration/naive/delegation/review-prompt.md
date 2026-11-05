Review the billing code as we discussed. Look at the proration logic in src/billing/ and
tell me what you find. I suspect the int() truncation in prorate at invoice.py:6 loses
cents, so check that first. See the session notes for the rest. Don't change anything.
