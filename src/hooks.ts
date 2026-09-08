import { useEffect, useRef, useState } from 'react';
import { normalizeSessionParams } from './memory/session';

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

/**
 * Pure parser for a shareable hash such as "#rho=0.6&lambda=1&repeats=1".
 * Missing or non-numeric values fall back to the supplied defaults, and the
 * result is normalized to the app's stated bounds — a mistyped or edited
 * shared URL can neither crash the first render (the engine throws on
 * out-of-range λ by design) nor display numbers the math didn't use.
 */
export function parseHashSettings(hash: string, defaults: SharedSettings): SharedSettings {
  const m = new URLSearchParams(hash.replace(/^#/, ''));
  const num = (key: string, fallback: number) => {
    const raw = m.get(key);
    if (raw == null) return fallback;
    const parsed = Number(raw);
    return Number.isFinite(parsed) ? parsed : fallback;
  };
  return normalizeSessionParams({
    rho: num('rho', defaults.rho),
    lambda: num('lambda', defaults.lambda),
    repeats: num('repeats', defaults.repeats),
  });
}

/** Read shareable settings from the URL hash once at startup (normalized). */
export function readHashSettings(defaults: SharedSettings): SharedSettings {
  if (typeof window === 'undefined') return normalizeSessionParams(defaults);
  return parseHashSettings(window.location.hash, defaults);
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
