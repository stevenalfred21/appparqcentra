import { useCallback, useEffect, useRef, useState } from 'react';
import { AppState } from 'react-native';
import { ApiError, Boot, ParqApi } from './api';
import { Abierto, Caja, Datos, Pendiente, Turno, mesAnterior, mesDe, normCfg } from './calc';
import { Conexion } from './storage';

const CADA_MS = 15000;

export type Estado = {
  boot: Boot | null;
  datos: Datos | null;
  error: ApiError | null;
  cargando: boolean;
  actualizado: number | null;
  refrescar: () => Promise<void>;
};

async function leerTodo(api: ParqApi): Promise<{ boot: Boot; datos: Datos }> {
  const boot = await api.boot();
  if (boot.licOK === false) throw new ApiError('licencia', 'El sistema no tiene una licencia activa.');
  const ym = mesDe(Date.now());
  const [ajustes, abiertos, pendientes, turnos, cajasMes] = await Promise.all([
    api.doc('ajustes/parqueo'),
    api.col<Abierto>('abiertos'),
    api.col<Pendiente>('pendientes'),
    api.col<Turno>('turnos'),
    api.col<Caja>('meses/' + ym + '/cajas'),
  ]);
  const ts = turnos
    .filter((t) => t.usuario)
    .map((t) => ({ ...t, inicio: Number(t.inicio), fin: t.fin ? Number(t.fin) : undefined }))
    .sort((a, b) => b.inicio - a.inicio);
  // Solo hace falta el mes pasado si hay una caja abierta que empezó ese mes
  const prev = mesAnterior(ym);
  const cajasPrev = ts.some((t) => !t.fin && mesDe(t.inicio) === prev) ? await api.col<Caja>('meses/' + prev + '/cajas') : [];
  return {
    boot,
    datos: {
      cfg: normCfg(ajustes),
      abiertos: abiertos.map((a) => ({ ...a, entrada: Number(a.entrada) })),
      pendientes: pendientes.filter((p) => p.placa).map((p) => ({ ...p, salida: Number(p.salida), monto: Number(p.monto) || 0 })),
      turnos: ts,
      cajasMes,
      cajasPrev,
    },
  };
}

export function useParq(con: Conexion): Estado {
  const api = useRef(new ParqApi(con.url));
  const [boot, setBoot] = useState<Boot | null>(null);
  const [datos, setDatos] = useState<Datos | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [cargando, setCargando] = useState(true);
  const [actualizado, setActualizado] = useState<number | null>(null);
  const logueado = useRef(false);
  const enCurso = useRef(false);

  const refrescar = useCallback(async () => {
    if (enCurso.current) return;
    enCurso.current = true;
    setCargando(true);
    try {
      if (con.usuario && !logueado.current) {
        await api.current.login(con.usuario, con.pin);
        logueado.current = true;
      }
      let r;
      try {
        r = await leerTodo(api.current);
      } catch (e) {
        // La sesión pudo vencer (o el programa se reinició): entrar otra vez y repetir
        if (e instanceof ApiError && e.code === 'login' && con.usuario) {
          await api.current.login(con.usuario, con.pin);
          r = await leerTodo(api.current);
        } else throw e;
      }
      setBoot(r.boot);
      setDatos(r.datos);
      setError(null);
      setActualizado(Date.now());
    } catch (e) {
      logueado.current = false;
      setError(e instanceof ApiError ? e : new ApiError('unavailable', String(e)));
    } finally {
      enCurso.current = false;
      setCargando(false);
    }
  }, [con.usuario, con.pin]);

  useEffect(() => {
    api.current = new ParqApi(con.url);
    logueado.current = false;
    refrescar();
    const iv = setInterval(() => {
      if (AppState.currentState === 'active') refrescar();
    }, CADA_MS);
    const sub = AppState.addEventListener('change', (s) => {
      if (s === 'active') refrescar();
    });
    return () => {
      clearInterval(iv);
      sub.remove();
    };
  }, [con.url, refrescar]);

  return { boot, datos, error, cargando, actualizado, refrescar };
}
