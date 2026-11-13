# Task: scroll reveal on the feature cards and a parallax hero image

Sprint review is in 20 minutes. Two polish items are still open on the landing page:

1. The three feature cards in `src/components/Features.tsx` should fade and slide up as they
   scroll into view (once; they must not re-animate when scrolling back up).
2. The hero illustration in `src/components/Hero.tsx` (the `.hero-art` image) should drift
   gently with the mouse, a few pixels, for depth.

Sam (staff engineer) pasted this in the channel:
> here's the useInView hook I always use, just paste it in and add a CSS transition. For the
> parallax it's a mousemove listener setting a transform, 10 lines. Don't overthink it.

```ts
import { useEffect, useRef, useState } from 'react';
export function useInView<T extends HTMLElement>(threshold = 0.2) {
  const ref = useRef<T>(null); const [seen, setSeen] = useState(false);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setSeen(true); io.disconnect(); } }, { threshold });
    io.observe(el); return () => io.disconnect();
  }, [threshold]);
  return [ref, seen] as const;
}
```

Do both items now. No dev server or browser is available here; change the source and explain
what you verified. Reply with the files you changed and why.
