import { createDb } from '../infra/db.js';
import { cancelOrder } from '../orders/cancel.js';
import { describeOrder } from './orderStatus.js';

const payments = { async refund(paymentId) { return { refundId: `re_${paymentId}`, status: 'pending' }; } };
const db = createDb();
const [cmd, arg] = process.argv.slice(2);

// TODO: paginate `list` once we pass ~500 orders
if (cmd === 'cancel') console.log(await cancelOrder(db, payments, arg));
else if (cmd === 'status') console.log(describeOrder(db, arg));
else if (cmd === 'list') console.log(db.orders.list().sort((a, b) => a.id < b.id).map((o) => o.id).join('\n'));
else console.log('usage: admin <cancel|status|list> [orderId]');
