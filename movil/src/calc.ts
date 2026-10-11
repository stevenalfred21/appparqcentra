// Cálculos copiados de la pantalla de ParqControl para que los números
// del celular salgan iguales a los de la computadora central.

export type Ticket = {
  id: string;
  num?: number;
  placa: string;
  categoria?: string;
  zona?: string;
  plaza?: string | number;
  empresa?: string;
  destino?: string;
  entrada: number;
  salida: number;
  pago?: number;
  min: number;
  monto: number;
  metodo?: string;
  cobEntrada?: string;
  cobSalida?: string;
  sinTicket?: boolean;
  dePendiente?: boolean;
  quien?: string;
};

export type Item = { id?: string; placa?: string; monto: number; ts: number; cob?: string; concepto?: string; motivo?: string; tipo?: string; nombre?: string };

export type Caja = {
  id: string;
  dia?: string;
  tickets?: Ticket[];
  gastos?: Item[];
  perdidas?: Item[];
  cancelados?: Item[];
  fijos?: Item[];
};

export type Turno = {
  id: string;
  usuario: string;
  inicio: number;
  fondo?: number;
  fin?: number;
  contado?: number;
  esperado?: number;
  diferencia?: number;
  efectivo?: number;
  otros?: number;
  gastos?: number;
  cobros?: number;
};

export type Abierto = { id: string; placa: string; num?: number; categoria?: string; entrada: number; precio?: number; zona?: string; plaza?: string | number; empresa?: string; cobEntrada?: string };
export type Pendiente = Ticket & { quien?: string };

export type Config = {
  nombre: string;
  categorias: { nombre: string; precio: number }[];
  bloqueMin: number;
  graciaMin: number;
  capacidad: number;
  plazoDias: number;
  contarVencidos: boolean;
};

export const SELL = 'Ticket sellado';
export const esDinero = (t: Ticket) => t.metodo !== SELL;

const pad = (n: number) => String(n).padStart(2, '0');
export const diaDe = (ms: number) => {
  const d = new Date(ms);
  return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
};
export const mesDe = (ms: number) => diaDe(ms).slice(0, 7);
export const mesAnterior = (ym: string) => {
  const [y, m] = ym.split('-').map(Number);
  return m === 1 ? y - 1 + '-12' : y + '-' + pad(m - 1);
};

export function normCfg(d: any): Config | null {
  if (!d) return null;
  let cats = Array.isArray(d.categorias)
    ? d.categorias.map((c: any) => ({ nombre: String(c?.nombre || ''), precio: Number(c?.precio) })).filter((c: any) => c.nombre && c.precio > 0)
    : [];
  if (!cats.length && Number(d.precio) > 0) cats = [{ nombre: 'Auto', precio: Number(d.precio) }];
  const zonas = Array.isArray(d.zonas) ? d.zonas.map((z: any) => Math.min(200, Math.floor(Number(z?.plazas) || 0))).filter((n: number) => n > 0) : [];
  return {
    nombre: String(d.nombre || ''),
    categorias: cats,
    bloqueMin: [15, 30, 60].includes(Number(d.bloqueMin)) ? Number(d.bloqueMin) : 60,
    graciaMin: Math.max(0, Number(d.graciaMin) || 0),
    capacidad: zonas.reduce((a: number, n: number) => a + n, 0) || Math.max(0, Number(d.capacidad) || 0),
    plazoDias: Number.isFinite(Number(d.pend?.plazoDias)) && d.pend?.plazoDias !== undefined ? Math.max(0, Number(d.pend.plazoDias)) : 7,
    contarVencidos: !!d.pend?.contarVencidos,
  };
}

export function calc(cfg: Config | null, entrada: number, salida: number, precio: number) {
  const min = Math.max(1, Math.ceil((salida - entrada) / 60000));
  if (!cfg || min <= cfg.graciaMin) return { min, monto: 0 };
  return { min, monto: Math.ceil(min / cfg.bloqueMin) * precio };
}

export const precioDe = (cfg: Config | null, t: { precio?: number; categoria?: string }) =>
  Number(t.precio) > 0 ? Number(t.precio) : (cfg?.categorias.find((c) => c.nombre === t.categoria) || cfg?.categorias[0] || { precio: 0 }).precio;

export const fechaCobro = (t: Ticket) => Number(t.pago) || Number(t.salida);

const lista = (cajas: Caja[], k: 'gastos' | 'perdidas' | 'cancelados' | 'fijos'): Item[] =>
  cajas.flatMap((c) => (Array.isArray(c[k]) ? (c[k] as Item[]) : [])).map((x) => ({ ...x, monto: Number(x.monto) || 0, ts: Number(x.ts) || 0 }));

export function ticketsDe(cajas: Caja[]): Ticket[] {
  const anulados = new Set(lista(cajas, 'cancelados').filter((c) => c.tipo === 'cobrado').map((c) => c.id));
  return cajas
    .flatMap((c) => (Array.isArray(c.tickets) ? c.tickets : []))
    .filter((t) => !anulados.has(t.id))
    .map((t) => ({ ...t, monto: Number(t.monto) || 0, min: Number(t.min) || 0 }));
}
export const gastosDe = (cajas: Caja[]) => lista(cajas, 'gastos');
export const perdidasDe = (cajas: Caja[]) => lista(cajas, 'perdidas');
export const canceladosDe = (cajas: Caja[]) => lista(cajas, 'cancelados');

export const vence = (cfg: Config | null, p: Pendiente) => Number(p.salida) + (cfg ? cfg.plazoDias : 7) * 864e5;

export type Datos = {
  cfg: Config | null;
  abiertos: Abierto[];
  pendientes: Pendiente[];
  turnos: Turno[];
  cajasMes: Caja[]; // mes actual
  cajasPrev: Caja[]; // mes anterior (para cajas que empezaron el mes pasado)
};

export function vigentes(d: Datos) {
  const cerrados = new Set(ticketsDe(d.cajasMes).map((t) => t.id));
  d.pendientes.forEach((p) => cerrados.add(p.id));
  return d.abiertos.filter((t) => t.placa && !cerrados.has(t.id)).sort((a, b) => a.entrada - b.entrada);
}

export function resumenDia(d: Datos, dia: string) {
  const ts = ticketsDe(d.cajasMes).filter((t) => diaDe(fechaCobro(t)) === dia);
  const gs = gastosDe(d.cajasMes).filter((g) => diaDe(g.ts) === dia);
  const ps = perdidasDe(d.cajasMes).filter((p) => diaDe(p.ts) === dia);
  const cx = canceladosDe(d.cajasMes).filter((c) => diaDe(c.ts) === dia);
  const total = ts.reduce((a, t) => a + (esDinero(t) ? t.monto : 0), 0);
  const gastos = gs.reduce((a, g) => a + g.monto, 0);
  const porMetodo: Record<string, { n: number; monto: number }> = {};
  const porCobrador: Record<string, { n: number; monto: number }> = {};
  ts.forEach((t) => {
    const m = (porMetodo[t.metodo || '(sin método)'] ||= { n: 0, monto: 0 });
    m.n++;
    m.monto += t.monto;
    const c = (porCobrador[t.cobSalida || '(sin nombre)'] ||= { n: 0, monto: 0 });
    c.n++;
    if (esDinero(t)) c.monto += t.monto;
  });
  const sell = ts.filter((t) => !esDinero(t));
  const sinT = ts.filter((t) => t.sinTicket);
  const entradas = ts.filter((t) => diaDe(t.entrada) === dia).length + d.abiertos.filter((a) => diaDe(a.entrada) === dia).length;
  return {
    tickets: ts.sort((a, b) => fechaCobro(b) - fechaCobro(a)),
    gastosLista: gs.sort((a, b) => b.ts - a.ts),
    perdidasLista: ps,
    canceladosLista: cx,
    total,
    gastos,
    neto: total - gastos,
    perdidas: ps.reduce((a, p) => a + p.monto, 0),
    sellados: { n: sell.length, monto: sell.reduce((a, t) => a + t.monto, 0) },
    sinTicket: { n: sinT.length, monto: sinT.reduce((a, t) => a + t.monto, 0) },
    porMetodo,
    porCobrador,
    entradas,
  };
}

export function resumenMes(d: Datos, ym: string) {
  const ing = ticketsDe(d.cajasMes).filter((t) => mesDe(fechaCobro(t)) === ym).reduce((a, t) => a + (esDinero(t) ? t.monto : 0), 0);
  const gas = gastosDe(d.cajasMes).filter((g) => mesDe(g.ts) === ym).reduce((a, g) => a + g.monto, 0);
  const per = perdidasDe(d.cajasMes).filter((p) => mesDe(p.ts) === ym).reduce((a, p) => a + p.monto, 0);
  return { ing, gas, per, neto: ing - gas };
}

// Lo mismo que hace el programa al cerrar una caja, pero en vivo para las abiertas
export function esperadoTurno(d: Datos, t: Turno, fin: number) {
  const todas = [...d.cajasMes, ...d.cajasPrev];
  let ef = 0,
    otros = 0,
    gas = 0,
    n = 0;
  ticketsDe(todas)
    .filter((x) => x.cobSalida === t.usuario && fechaCobro(x) >= t.inicio && fechaCobro(x) <= fin)
    .forEach((x) => {
      n++;
      if (x.metodo === 'Efectivo') ef += x.monto;
      else otros += x.monto;
    });
  gastosDe(todas)
    .filter((g) => g.cob === t.usuario && g.ts >= t.inicio && g.ts <= fin)
    .forEach((g) => (gas += g.monto));
  return { ef, otros, gas, n, esperado: (Number(t.fondo) || 0) + ef - gas };
}
