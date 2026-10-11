// Servidor de PRUEBA que imita la API de ParqControl.exe con datos inventados.
// Sirve para probar la app sin tener la computadora central a mano.
//   node tools/servidor-prueba.js            -> http://localhost:8090
//   PEDIR_LOGIN=1 node tools/servidor-prueba.js  (exige usuario Admin, PIN 1234)
const http = require('http');

const PORT = Number(process.env.PORT) || 8090;
const PEDIR_LOGIN = !!process.env.PEDIR_LOGIN;
const pad = (n) => String(n).padStart(2, '0');
const diaDe = (ms) => {
  const d = new Date(ms);
  return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
};

const now = Date.now();
const H = 3600e3;
const hoy = diaDe(now);
const ym = hoy.slice(0, 7);
let n = 120;
const tk = (o) => ({ id: 't' + n, num: ++n, placa: String(n).padStart(6, '0'), categoria: 'Auto', min: 0, metodo: 'Efectivo', ...o });

const tickets = [
  tk({ entrada: now - 5 * H, salida: now - 3 * H, min: 120, monto: 100, cobSalida: 'María' }),
  tk({ entrada: now - 4 * H, salida: now - 2.5 * H, min: 90, monto: 100, metodo: 'Transferencia', cobSalida: 'María' }),
  tk({ entrada: now - 3 * H, salida: now - 2 * H, min: 60, monto: 50, cobSalida: 'Pedro', categoria: 'Moto' }),
  tk({ entrada: now - 2 * H, salida: now - 1 * H, min: 60, monto: 50, metodo: 'Ticket sellado', cobSalida: 'Pedro' }),
  tk({ entrada: now - 1.5 * H, salida: now - 0.5 * H, min: 60, monto: 75, cobSalida: 'Pedro', categoria: 'Camioneta SUV', sinTicket: true }),
];

const db = {
  'ajustes/parqueo': {
    nombre: 'Parqueo Central (PRUEBA)',
    categorias: [
      { nombre: 'Auto', precio: 50 },
      { nombre: 'Camioneta SUV', precio: 75 },
      { nombre: 'Moto', precio: 25 },
    ],
    bloqueMin: 60,
    graciaMin: 10,
    capacidad: 40,
    pend: { plazoDias: 7 },
    usuarios: [{ nombre: 'Admin', pinHash: 'x' }, { nombre: 'María' }, { nombre: 'Pedro' }],
  },
  abiertos: {
    a1: { placa: '000126', num: 126, categoria: 'Auto', entrada: now - 0.7 * H, cobEntrada: 'María' },
    a2: { placa: '000127', num: 127, categoria: 'Moto', entrada: now - 2.2 * H, cobEntrada: 'Pedro', zona: 'A', plaza: 3 },
    a3: { placa: '000128', num: 128, categoria: 'Camioneta SUV', entrada: now - 26 * H, cobEntrada: 'María', empresa: 'Torre Norte' },
    a4: { placa: '000129', num: 129, categoria: 'Auto', entrada: now - 0.1 * H, cobEntrada: 'Pedro' },
  },
  pendientes: {
    p1: { placa: '000110', num: 110, categoria: 'Auto', entrada: now - 30 * H, salida: now - 28 * H, monto: 150, quien: 'Juan Pérez', cobSalida: 'María' },
    p2: { placa: '000099', num: 99, categoria: 'Auto', entrada: now - 10 * 24 * H, salida: now - 9 * 24 * H, monto: 200, quien: 'Empresa X', cobSalida: 'Pedro' },
  },
  turnos: {
    t1: { usuario: 'María', inicio: now - 6 * H, fondo: 1000 },
    t2: { usuario: 'Pedro', inicio: now - 4 * H, fondo: 500, fin: now - 0.2 * H, contado: 625, esperado: 650, diferencia: -25, efectivo: 125, otros: 50, gastos: 25, cobros: 3 },
    t3: { usuario: 'María', inicio: now - 30 * H, fondo: 1000, fin: now - 22 * H, contado: 1850, esperado: 1850, diferencia: 0 },
  },
  ['meses/' + ym + '/cajas']: {
    [hoy + '_s1_1']: {
      dia: hoy,
      tickets,
      gastos: [{ id: 'g1', concepto: 'Agua y café', monto: 25, ts: now - 2 * H, cob: 'Pedro' }],
      perdidas: [],
      cancelados: [{ id: 'c1', placa: '000119', categoria: 'Auto', monto: 0, motivo: 'Error al registrar', ts: now - 4.5 * H, cob: 'María', tipo: 'abierto' }],
      fijos: [],
    },
  },
};

const sesiones = new Set();
function json(res, code, obj, extra = {}) {
  res.writeHead(code, { 'Content-Type': 'application/json', ...extra });
  res.end(JSON.stringify(obj));
}

http
  .createServer((req, res) => {
    // Solo para probar la versión web de la app (en el teléfono no hace falta)
    if (req.headers.origin) {
      res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
      res.setHeader('Access-Control-Allow-Credentials', 'true');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    }
    if (req.method === 'OPTIONS') return res.writeHead(204).end();
    const u = new URL(req.url, 'http://x');
    const sid = /(?:^|;\s*)pqs=([^;]+)/.exec(req.headers.cookie || '')?.[1];
    const ok = !PEDIR_LOGIN || (sid && sesiones.has(sid));
    console.log(req.method, u.pathname + u.search, ok ? '' : '(sin sesión)');

    if (u.pathname === '/api/boot')
      return json(res, 200, { licOK: true, app: 'ParqControl', version: '1.3 (prueba)', lic: { cliente: 'Cliente de prueba', vence: '2026-10-20', dias: 9 }, urls: ['http://192.168.1.20:8090'], alertas: [], user: '' });
    if (u.pathname === '/api/login' && req.method === 'POST') {
      let b = '';
      req.on('data', (c) => (b += c));
      req.on('end', () => {
        const j = JSON.parse(b || '{}');
        if (PEDIR_LOGIN && !(j.nombre === 'Admin' && j.pin === '1234')) return json(res, 403, { code: 'login', error: 'PIN incorrecto.' });
        const s = Math.random().toString(36).slice(2);
        sesiones.add(s);
        json(res, 200, { ok: true }, { 'Set-Cookie': 'pqs=' + s + '; Path=/; HttpOnly' });
      });
      return;
    }
    if (!ok) return json(res, 401, { code: 'login', error: 'Tu usuario no tiene permiso o no has entrado con tu PIN.' });
    const p = u.searchParams.get('p') || '';
    if (u.pathname === '/api/doc') return db[p] ? json(res, 200, { exists: true, data: db[p] }) : json(res, 200, { exists: false });
    if (u.pathname === '/api/col') return json(res, 200, { docs: Object.entries(db[p] || {}).map(([id, data]) => ({ id, data })) });
    json(res, 404, { error: 'no existe' });
  })
  .listen(PORT, () => console.log('Servidor de prueba en http://localhost:' + PORT + (PEDIR_LOGIN ? ' (pide login: Admin / 1234)' : '')));
