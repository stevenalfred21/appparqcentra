// Cliente de la API local de ParqControl.exe (la misma que usa su pantalla web).
// Rutas sacadas del propio programa: /api/boot, /api/login, /api/col?p=, /api/doc?p=

export type Boot = {
  licOK?: boolean;
  app?: string;
  version?: string;
  codigo?: string;
  user?: string;
  lic?: { cliente?: string; vence?: string; dias?: number };
  urls?: string[];
  alertas?: string[];
  bloqueado?: string;
};

export type Doc<T = any> = T & { id: string };

export class ApiError extends Error {
  code: string;
  status: number;
  constructor(code: string, message: string, status = 0) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

export function normalizarUrl(u: string): string {
  let s = u.trim().replace(/\/+$/, '');
  if (!s) return s;
  if (!/^https?:\/\//i.test(s)) s = 'http://' + s;
  // Si no trae puerto y es http, el programa usa 8090 por defecto
  const m = /^(https?):\/\/([^/:]+)(:\d+)?(\/.*)?$/i.exec(s);
  if (m && !m[3] && m[1].toLowerCase() === 'http') s = m[1] + '://' + m[2] + ':8090' + (m[4] || '');
  return s;
}

const TIMEOUT_MS = 12000;

export class ParqApi {
  constructor(public base: string) {}

  private async req<T>(method: string, path: string, body?: unknown): Promise<T> {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), TIMEOUT_MS);
    let r: Response;
    try {
      r = await fetch(this.base + path, {
        method,
        credentials: 'include',
        headers: body === undefined ? {} : { 'Content-Type': 'application/json' },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: ctl.signal,
      });
    } catch {
      throw new ApiError('unavailable', 'No hay conexión con la computadora central.');
    } finally {
      clearTimeout(t);
    }
    let j: any = {};
    try {
      j = await r.json();
    } catch {}
    if (r.status === 402) throw new ApiError('licencia', 'El sistema no tiene una licencia activa.', 402);
    if (!r.ok) throw new ApiError(j.code || (r.status === 401 || r.status === 403 ? 'login' : 'unavailable'), j.error || 'Error ' + r.status, r.status);
    return j as T;
  }

  boot() {
    return this.req<Boot>('GET', '/api/boot');
  }

  async login(nombre: string, pin: string) {
    await this.req('POST', '/api/login', { nombre, pin });
  }

  async col<T = any>(path: string): Promise<Doc<T>[]> {
    const j = await this.req<{ docs?: { id: string; data: T }[] }>('GET', '/api/col?p=' + encodeURIComponent(path));
    return (j.docs || []).map((d) => ({ ...(d.data as any), id: d.id }));
  }

  async doc<T = any>(path: string): Promise<T | null> {
    const j = await this.req<{ exists?: boolean; data?: T }>('GET', '/api/doc?p=' + encodeURIComponent(path));
    return j.exists ? (j.data as T) : null;
  }
}
