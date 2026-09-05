import { useEffect, useRef, useState } from 'react';

export function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(
    () => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  );
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const onChange = () => setReduced(mq.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);
  return reduced;
}

export interface SharedSettings {
  rho: number;
  lambda: number;
  repeats: number;
}

/** Read shareable settings from the URL hash once at startup. */
export function readHashSettings(defaults: SharedSettings): SharedSettings {
  if (typeof window === 'undefined') return defaults;
  const m = new URLSearchParams(window.location.hash.replace(/^#/, ''));
  const num = (key: string, fallback: number) => {
    const raw = m.get(key);
    if (raw == null) return fallback;
    const parsed = Number(raw);
    return Number.isFinite(parsed) ? parsed : fallback;
  };
  return {
    rho: num('rho', defaults.rho),
    lambda: num('lambda', defaults.lambda),
    repeats: num('repeats', defaults.repeats),
  };
}

/** Reflect current settings into the URL hash (replaceState, no history spam). */
export function useHashSync(settings: SharedSettings): void {
  const first = useRef(true);
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    const p = new URLSearchParams();
    p.set('rho', String(settings.rho));
    p.set('lambda', String(settings.lambda));
    p.set('repeats', String(settings.repeats));
    window.history.replaceState(null, '', `#${p.toString()}`);
  }, [settings.rho, settings.lambda, settings.repeats]);
}
