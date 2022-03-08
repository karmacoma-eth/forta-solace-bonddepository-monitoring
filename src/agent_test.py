from unittest.mock import Mock
from forta_agent import create_transaction_event
from .constants import BOND_DEPOSITORY_ADDRESS
from .agent import handle_transaction
from dataclasses import dataclass, field

EXPECTED_BOND_TELLER = '0x0000000000000000000000000000000000001234'

def event_args(_teller = EXPECTED_BOND_TELLER):
    return {
        'teller': _teller,
    }

@dataclass
class TellerAddedEvent:
    address: str = BOND_DEPOSITORY_ADDRESS
    blockNumber: int = 42
    args: dict = field(default_factory=event_args)
    event: str = 'TellerAdded'

@dataclass
class TellerRemovedEvent:
    address: str = BOND_DEPOSITORY_ADDRESS
    blockNumber: int = 42
    args: dict = field(default_factory=event_args)
    event: str = 'TellerRemoved'

mock_tx_event = create_transaction_event({})
mock_tx_event.filter_log = Mock()

class TestBondDepositoryMonitoring:
    def test_finds_bond_teller_added(self):
        mock_tx_event.filter_log.side_effect = [[TellerAddedEvent()], []]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 1
        assert findings[0].metadata['event'] == 'TellerAdded'
        assert findings[0].metadata['bond_teller_address'] == EXPECTED_BOND_TELLER

    def test_finds_bond_teller_removed(self):
        mock_tx_event.filter_log.side_effect = [[], [TellerRemovedEvent()]]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 1
        assert findings[0].metadata['event'] == 'TellerRemoved'
        assert findings[0].metadata['bond_teller_address'] == EXPECTED_BOND_TELLER

    def test_finds_both_added_and_removed(self):
        mock_tx_event.filter_log.side_effect = [[TellerAddedEvent()], [TellerRemovedEvent()]]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 2
        assert findings[0].metadata['event'] == 'TellerAdded'
        assert findings[0].metadata['bond_teller_address'] == EXPECTED_BOND_TELLER

        assert findings[1].metadata['event'] == 'TellerRemoved'
        assert findings[1].metadata['bond_teller_address'] == EXPECTED_BOND_TELLER

    def does_not_detect_if_bonddepository_does_not_match(self):
        mock_tx_event.filter_log.side_effect = [
            [TellerAddedEvent(address='0x000000000000000000000000000000000000dead')],
            [TellerRemovedEvent(address='0x000000000000000000000000000000000000dead')],
        ]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 0
