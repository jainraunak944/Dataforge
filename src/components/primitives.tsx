import katex from 'katex';
import { useMemo, type ReactNode } from 'react';
import type { Matrix, Vec } from '../memory/additiveMemory';

/** Fixed display precision; the underlying state is full float64. */
export function fmt(x: number, digits = 3): string {
  if (Object.is(x, -0)) x = 0;
  const r = x.toFixed(digits);
  return r === '-0.000' ? '0.000' : r;
}

export function Eq({ tex, block = false, label }: { tex: string; block?: boolean; label?: string }) {
  const html = useMemo(
    () => katex.renderToString(tex, { displayMode: block, throwOnError: false }),
    [tex, block],
  );
  const el = (
    <span
      role="math"
      aria-label={label ?? tex}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
  return block ? <div className="eq-block">{el}</div> : el;
}

export type BadgeKind = 'live' | 'source' | 'reported' | 'toy';

const BADGE_TEXT: Record<BadgeKind, string> = {
  live: 'live computation',
  source: 'source-derived illustration',
  reported: 'author-reported result',
  toy: 'original toy computation',
};

export function Badge({ kind }: { kind: BadgeKind }) {
  return <span className={`badge ${kind}`}>{BADGE_TEXT[kind]}</span>;
}

export function AssocMark({ which }: { which: 'A' | 'B' }) {
  // Shape + letter + color: never color alone.
  return (
    <span className={`assoc ${which === 'A' ? 'a' : 'b'}`}>
      {which === 'A' ? '●' : '▲'}&thinsp;{which}
    </span>
  );
}

export function VectorView({
  v,
  caption,
  accent,
  digits = 3,
  testId,
}: {
  v: Vec;
  caption: ReactNode;
  accent?: 'a' | 'b';
  digits?: number;
  /** Stable hook for the browser smoke test; no visual effect. */
  testId?: string;
}) {
  return (
    <div style={{ display: 'inline-block', textAlign: 'center' }} data-testid={testId}>
      <div className={`vec${accent ? ` accent-${accent}` : ''}`}>
        {v.map((c, i) => (
          <span key={i} className="cell">
            {fmt(c, digits)}
          </span>
        ))}
      </div>
      <div className="matrix-label">{caption}</div>
    </div>
  );
}

export function MatrixView({
  M,
  caption,
  highlight,
  selected,
  onCellClick,
  digits = 3,
}: {
  M: Matrix;
  caption: ReactNode;
  /** highlight(row, col) → true to tint a cell */
  highlight?: (row: number, col: number) => boolean;
  selected?: { row: number; col: number } | null;
  onCellClick?: (row: number, col: number) => void;
  digits?: number;
}) {
  const cols = M[0]?.length ?? 0;
  return (
    <div style={{ display: 'inline-block', textAlign: 'center' }}>
      <div
        className="matrix"
        style={{ gridTemplateColumns: `repeat(${cols}, auto)` }}
        role={onCellClick ? 'group' : undefined}
      >
        {M.map((row, i) =>
          row.map((x, j) => {
            const isSel = selected != null && selected.row === i && selected.col === j;
            const cls = [
              'cell',
              highlight?.(i, j) ? 'hl' : '',
              onCellClick ? 'clickable' : '',
              isSel ? 'selected' : '',
            ]
              .filter(Boolean)
              .join(' ');
            const content = fmt(x, digits);
            return onCellClick ? (
              <button
                key={`${i}-${j}`}
                type="button"
                className={cls}
                style={{ font: 'inherit' }}
                aria-pressed={isSel}
                aria-label={`matrix cell row ${i + 1}, column ${j + 1}, value ${content}`}
                onClick={() => onCellClick(i, j)}
              >
                {content}
              </button>
            ) : (
              <span key={`${i}-${j}`} className={cls}>
                {content}
              </span>
            );
          }),
        )}
      </div>
      <div className="matrix-label">{caption}</div>
    </div>
  );
}

/** SVG unit-circle diagram of the two key vectors. Decorative arrows are
 * backed by the numeric tables next to them (accessible alternative). */
export function KeyCircle({ kA, kB }: { kA: Vec; kB: Vec }) {
  const size = 190;
  const c = size / 2;
  const r = size / 2 - 30;
  const px = (v: Vec) => ({ x: c + v[0] * r, y: c - v[1] * r });
  const a = px(kA);
  const b = px(kB);
  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      role="img"
      aria-label={`Unit circle with key A at (${fmt(kA[0], 2)}, ${fmt(kA[1], 2)}) and key B at (${fmt(kB[0], 2)}, ${fmt(kB[1], 2)})`}
    >
      <circle cx={c} cy={c} r={r} fill="none" stroke="var(--line-strong)" strokeDasharray="3 3" />
      <line x1={c - r} y1={c} x2={c + r} y2={c} stroke="var(--line)" />
      <line x1={c} y1={c - r} x2={c} y2={c + r} stroke="var(--line)" />
      {/* key A: line + circle head */}
      <line x1={c} y1={c} x2={a.x} y2={a.y} stroke="var(--a-color)" strokeWidth="2.5" />
      <circle cx={a.x} cy={a.y} r="5.5" fill="var(--a-color)" />
      {/* key B: line + triangle head */}
      <line x1={c} y1={c} x2={b.x} y2={b.y} stroke="var(--b-color)" strokeWidth="2.5" />
      <polygon
        points={`${b.x},${b.y - 7} ${b.x - 6},${b.y + 5} ${b.x + 6},${b.y + 5}`}
        fill="var(--b-color)"
      />
      <text x={a.x + 8} y={a.y - 6} fontSize="12" fontFamily="var(--sans)" fill="var(--a-color)">
        k_A
      </text>
      <text x={b.x + 8} y={b.y + 4} fontSize="12" fontFamily="var(--sans)" fill="var(--b-color)">
        k_B
      </text>
    </svg>
  );
}

export function ErrorChip({ value }: { value: number }) {
  const zeroish = value < 1e-9;
  return (
    <span className={`error-chip ${zeroish ? 'zeroish' : 'nonzero'}`}>
      L2 error {zeroish ? '0.000' : fmt(value)}
    </span>
  );
}
