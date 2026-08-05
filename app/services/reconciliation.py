from collections import defaultdict

from models import Transaction


def reconcile_transactions(transactions):

    grouped = defaultdict(list)

    for transaction in transactions:

        grouped[
            transaction.transaction_reference
        ].append(transaction)

    matched = []

    exceptions = []

    for reference, rows in grouped.items():

        if len(rows) == 4:

            for row in rows:

                matched.append(row)

        else:

            for row in rows:

                exceptions.append(row)

    return matched, exceptions