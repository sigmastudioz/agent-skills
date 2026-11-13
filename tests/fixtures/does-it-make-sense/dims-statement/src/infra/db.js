export const customers = {
  async active() { return [{ id: 'c1', name: 'ACME', email: 'ap@acme.example' }]; },
};
export const ledger = {
  async rowsFor(customerId, period) {
    return [{ date: `${period}-03`, description: 'Baltic corridor plan', cents: 123450 }];
  },
};
