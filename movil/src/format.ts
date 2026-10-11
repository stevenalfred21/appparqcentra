const pad = (n: number) => String(n).padStart(2, '0');
const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];

// Igual que el programa: RD$ 1,234.50 (sin depender de Intl en el teléfono)
export function money(n: number) {
  const v = Number(n) || 0;
  const neg = v < 0;
  const [ent, dec] = Math.abs(v).toFixed(2).split('.');
  return (neg ? '-' : '') + 'RD$ ' + ent.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '.' + dec;
}

export function hora(ms: number) {
  const d = new Date(ms);
  const h = d.getHours();
  return (h % 12 || 12) + ':' + pad(d.getMinutes()) + (h < 12 ? ' a. m.' : ' p. m.');
}

export function fecha(ms: number) {
  const d = new Date(ms);
  return pad(d.getDate()) + ' ' + MESES[d.getMonth()] + ' ' + d.getFullYear();
}

export function fechaHora(ms: number) {
  return fecha(ms) + ' ' + hora(ms);
}

export function corta(ms: number) {
  const d = new Date(ms);
  return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + ' ' + hora(ms);
}

export function dur(min: number) {
  const h = Math.floor(min / 60),
    m = Math.round(min % 60);
  return h ? h + ' h ' + pad(m) + ' min' : m + ' min';
}

export const numTxt = (t: { num?: number; placa?: string }) => (t.num ? '#' + String(t.num).padStart(6, '0') : t.placa || '');

export function hace(ms: number, now = Date.now()) {
  const s = Math.max(0, Math.round((now - ms) / 1000));
  if (s < 60) return 'hace ' + s + ' s';
  return 'hace ' + Math.round(s / 60) + ' min';
}
