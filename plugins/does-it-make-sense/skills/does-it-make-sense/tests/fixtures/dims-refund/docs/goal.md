# Order cancellation and refunds — ops goal (accepted 2026-10-02)

**User:** operations team members, using the admin CLI.

**Goal:** an operator cancels an order and can confirm, from the admin CLI alone, that the
customer has been refunded — without opening the payment provider's dashboard.

**Why:** today ops spend ~40 minutes a day cross-checking refunds in the provider dashboard.

**Non-goals:** partial refunds; customer-facing refund emails (owned by Notifications).
