import './Features.css';

const FEATURES = [
  { title: 'Live quay status', body: 'Berth, crane and gate events in one timeline.' },
  { title: 'Customs ready', body: 'Pre-filled declarations for EE, LV, LT and FI.' },
  { title: 'Customer ETA', body: 'Share a tracking page with a reliable arrival window.' },
];

export function Features() {
  return (
    <section className="features">
      {FEATURES.map((f) => (
        <article className="feature-card" key={f.title}>
          <h2>{f.title}</h2>
          <p>{f.body}</p>
        </article>
      ))}
    </section>
  );
}
