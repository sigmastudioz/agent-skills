import './Hero.css';

export function Hero() {
  return (
    <section className="hero">
      <div className="hero-bg" aria-hidden="true" />
      <div className="hero-copy">
        <h1>Ship the northern route</h1>
        <p>Freight visibility for the Baltic corridor, from quay to customer.</p>
        <a className="cta" href="/demo">Book a demo</a>
      </div>
      <img className="hero-art" src="/art/container-ship.png" alt="" width="520" height="360" />
    </section>
  );
}
