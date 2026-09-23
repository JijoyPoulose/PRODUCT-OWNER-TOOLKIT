# Flag shipments with missing commercial invoice before cutoff

**Parent:** EPIC-12 Pre-arrival data quality · **Objective:** PI-3 Obj 2: Reduce entry holds by 20%

## Story

**As a** customs entry clerk
**I want** shipments missing a commercial invoice flagged 4 hours before the filing cutoff
**So that** I can request the document from the shipper in time and avoid a customs hold

## Context

Last quarter, 18% of entry holds traced back to a missing invoice discovered after cutoff. Clerks currently find this by manual review.

## Acceptance criteria

```gherkin
Scenario: Shipment missing invoice is flagged
  Given a shipment with an estimated arrival within 24 hours
  And no commercial invoice attached
  When the time is 4 hours before its filing cutoff
  Then the shipment appears in the "Missing documents" queue
  And the assigned clerk receives a notification within 5 minutes

Scenario: Invoice arrives after flagging
  Given a shipment in the "Missing documents" queue
  When a commercial invoice is attached
  Then the shipment is removed from the queue within 1 minute

Scenario: Invalid invoice file is rejected
  Given a shipment in the "Missing documents" queue
  When a file that is not a PDF or image is uploaded as the invoice
  Then the upload is rejected with the message "Invoice must be a PDF, JPG or PNG"
  And the shipment remains in the queue
```

## Business rules

- BR-1: Cutoff time is taken from the port's filing rules table
- BR-2: Low-value shipments exempt from invoice requirements are never flagged

## Out of scope

- Automatically emailing the shipper (separate story)

## Dependencies

- Port filing rules table (Data team, available)

## Estimate

Story points: 5
