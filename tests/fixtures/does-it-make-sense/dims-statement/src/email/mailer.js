export class Mailer {
  constructor({ transport }) { this.transport = transport; this.sent = []; }
  // attachments: [{ filename, contentType, content: Buffer|string }]
  async send({ to, subject, text, attachments = [] }) {
    const msg = { to, subject, text, attachments };
    if (this.transport === 'log') console.log('mail:', JSON.stringify({ to, subject, attachments: attachments.length }));
    this.sent.push(msg);
    return { accepted: true, id: `m_${this.sent.length}` };
  }
}
