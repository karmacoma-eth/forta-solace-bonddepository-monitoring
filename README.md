# Solace BondDepository Monitoring


## Description

This agent detects TellerAdded and TellerRemoved events emitted by BondDepository contracts

## Supported Chains

- Ethereum

TODO:
- Polygon

## Alerts

- SOLACE-2
  - Triggers when a teller is added or removed from the configured BondDepository contract
  - type: info
  - severity: info
  - metadata:
    - bond_teller_address: the address of the teller contract that was added or removed
    - bond_depository_address: the address of the BondDepository contract
    - action: `added` or `removed`

## Test Data

This Ethereum transaction can be used to verify the detection logic:

`0x438464e0017caeabd4f51951969480fbd4b2ab0a707ca4fc070f5fac53dac51c`

It corresponds to a `BondDepository.addTeller(address teller)` interaction:

```
$ npm run tx 0x438464e0017caeabd4f51951969480fbd4b2ab0a707ca4fc070f5fac53dac51c

> forta-agent-starter@0.0.1 tx
> forta-agent run --tx "0x438464e0017caeabd4f51951969480fbd4b2ab0a707ca4fc070f5fac53dac51c"

1 findings for transaction 0x438464e0017caeabd4f51951969480fbd4b2ab0a707ca4fc070f5fac53dac51c {
  "name": "BondDepository Monitoring",
  "description": "TellerAdded detected in BondDepository",
  "alertId": "SOLACE-2",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "bond_depository_address": "0x501ace2f00ec599d4fdea408680e192f88d94d0d",
    "bond_teller_address": "0x501aCef4F8397413C33B13cB39670aD2f17BfE62",
    "event": "TellerAdded"
  }
}
```