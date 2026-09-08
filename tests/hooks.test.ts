/**
 * Tests for the URL-hash seam. A shared link is untrusted input: values must
 * parse leniently, fall back to the caller's defaults, and come back
 * normalized to the app's stated bounds — never raw. (Before normalization,
 * "#lambda=2" reached the engine unclamped and crashed the first render.)
 */
import { describe, expect, it } from 'vitest';
import { parseHashSettings } from '../src/hooks';
import { MAX_REPEATS } from '../src/memory/session';

const DEFAULTS = { rho: 0.6, lambda: 1, repeats: 1 }; // mirrors App's DEFAULTS

describe('parseHashSettings', () => {
  it('keeps valid in-range values unchanged', () => {
    expect(parseHashSettings('#rho=0.25&lambda=0.5&repeats=2', DEFAULTS)).toEqual({
      rho: 0.25,
      lambda: 0.5,
      repeats: 2,
    });
  });

  it('missing keys use the supplied defaults', () => {
    expect(parseHashSettings('', DEFAULTS)).toEqual(DEFAULTS);
    expect(parseHashSettings('#rho=0.3', DEFAULTS)).toEqual({ rho: 0.3, lambda: 1, repeats: 1 });
  });

  it('normalizes out-of-range λ instead of letting it crash the render', () => {
    expect(parseHashSettings('#lambda=2', DEFAULTS).lambda).toBe(1);
    expect(parseHashSettings('#lambda=-0.5', DEFAULTS).lambda).toBe(0);
  });

  it('normalizes out-of-range ρ and repeats to the stated bounds', () => {
    expect(parseHashSettings('#rho=7', DEFAULTS).rho).toBe(1);
    expect(parseHashSettings('#rho=-3', DEFAULTS).rho).toBe(0);
    expect(parseHashSettings('#repeats=500', DEFAULTS).repeats).toBe(MAX_REPEATS);
    expect(parseHashSettings('#repeats=0', DEFAULTS).repeats).toBe(1);
    expect(parseHashSettings('#repeats=2.6', DEFAULTS).repeats).toBe(3); // existing rounding
  });

  it('malformed or non-finite values fall back safely to the defaults', () => {
    expect(parseHashSettings('#rho=abc&lambda=Infinity&repeats=NaN', DEFAULTS)).toEqual(DEFAULTS);
    expect(parseHashSettings('#not-even-a-query-string', DEFAULTS)).toEqual(DEFAULTS);
  });

  it('the combined invalid share link resolves to the effective values', () => {
    expect(parseHashSettings('#rho=7&lambda=2&repeats=500', DEFAULTS)).toEqual({
      rho: 1,
      lambda: 1,
      repeats: MAX_REPEATS,
    });
  });
});
