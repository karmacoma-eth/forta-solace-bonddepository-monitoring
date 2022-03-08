from forta_agent import Finding, FindingType, FindingSeverity, get_web3_provider

from .constants import *

web3 = get_web3_provider()

def handle_transaction(transaction_event):
    findings = []

    # look for both TellerAdded and TellerRemoved events
    events = transaction_event.filter_log(TELLER_ADDED_EVENT_ABI)
    events.extend(transaction_event.filter_log(TELLER_REMOVED_EVENT_ABI))

    for event in events:
        if web3.toChecksumAddress(event.address) != BOND_DEPOSITORY_ADDRESS:
            continue

        findings.append(Finding({
            'name': 'BondDepository Monitoring',
            'description': f'{event.event} event detected in BondDepository',
            'alert_id': 'SOLACE-2',
            'type': FindingType.Info,
            'severity': FindingSeverity.Info,
            'metadata': {
                'bond_depository_address': event.address,
                'bond_teller_address': event.args['teller'],
                'event': event.event
            }
        }))

    return findings
