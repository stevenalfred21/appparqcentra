import { useEffect, useMemo, useState } from 'react';
import { Pressable, RefreshControl, ScrollView, StyleSheet, Text, View } from 'react-native';
import { Datos, calc, diaDe, esperadoTurno, mesDe, precioDe, resumenDia, resumenMes, vence, vigentes } from './calc';
import { corta, dur, fechaHora, hace, hora, money, numTxt } from './format';
import { Conexion } from './storage';
import { Barra, Card, Fila, Kpi, Tema, Vacio, s } from './ui';
import { useParq } from './useParq';

const pl = (n: number, uno: string, varios: string) => n + ' ' + (n === 1 ? uno : varios);

const TABS = [
  ['resumen', 'Hoy'],
  ['dentro', 'Dentro'],
  ['cajas', 'Cajas'],
  ['pend', 'Pendientes'],
] as const;
type Tab = (typeof TABS)[number][0];

export default function Monitor({ t, con, onSalir }: { t: Tema; con: Conexion; onSalir: () => void }) {
  const { boot, datos, error, cargando, actualizado, refrescar } = useParq(con);
  const [tab, setTab] = useState<Tab>('resumen');
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const iv = setInterval(() => setNow(Date.now()), 30000);
    return () => clearInterval(iv);
  }, []);

  const enLinea = !!actualizado && !error;
  const alertas = boot?.bloqueado ? [boot.bloqueado] : boot?.alertas || [];

  return (
    <View style={{ flex: 1 }}>
      <View style={[st.head, { borderColor: t.borde }]}>
        <View style={{ flex: 1 }}>
          <Text style={[st.nombre, { color: t.texto }]} numberOfLines={1}>
            {datos?.cfg?.nombre || 'ParqControl'}
          </Text>
          <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 2 }}>
            <View style={[st.punto, { backgroundColor: enLinea ? t.bien : t.mal }]} />
            <Text style={{ color: t.suave, fontSize: 12 }}>
              {enLinea ? 'Sistema encendido · ' + hace(actualizado!, now) : error ? 'Sin conexión' : 'Conectando…'}
            </Text>
          </View>
        </View>
        <Pressable onPress={onSalir} hitSlop={10}>
          <Text style={{ color: t.acento, fontWeight: '600' }}>Conexión</Text>
        </Pressable>
      </View>

      <View style={[st.tabs, { borderColor: t.borde }]}>
        {TABS.map(([k, label]) => (
          <Pressable key={k} onPress={() => setTab(k)} style={[st.tab, tab === k && { borderBottomColor: t.acento }]}>
            <Text style={{ color: tab === k ? t.acento : t.suave, fontWeight: '700' }}>{label}</Text>
          </Pressable>
        ))}
      </View>

      <ScrollView contentContainerStyle={{ padding: 14 }} refreshControl={<RefreshControl refreshing={cargando && !!datos} onRefresh={refrescar} />}>
        {error ? (
          <View style={[st.banner, { backgroundColor: t.mal }]}>
            <Text style={st.bannerTit}>{error.code === 'unavailable' ? 'No hay conexión con la computadora central' : 'Problema con el sistema'}</Text>
            <Text style={st.bannerTxt}>
              {error.code === 'unavailable'
                ? 'Puede que ParqControl esté cerrado, la PC apagada o sin internet' + (actualizado ? '. Última vez visto ' + fechaHora(actualizado) : '') + '.'
                : error.message}
            </Text>
          </View>
        ) : null}
        {alertas.length ? (
          <View style={[st.banner, { backgroundColor: t.mal }]}>
            <Text style={st.bannerTit}>{boot?.bloqueado ? 'Los datos están bloqueados' : 'Alerta: cambios hechos por fuera del sistema'}</Text>
            {alertas.map((a, i) => (
              <Text key={i} style={st.bannerTxt}>
                • {a}
              </Text>
            ))}
          </View>
        ) : null}
        {boot?.lic?.vence && typeof boot.lic.dias === 'number' && boot.lic.dias <= 15 ? (
          <View style={[st.banner, { backgroundColor: t.aviso }]}>
            <Text style={st.bannerTxt}>La licencia vence en {boot.lic.dias} día(s) ({boot.lic.vence}).</Text>
          </View>
        ) : null}

        {!datos ? (
          <Vacio t={t} texto={error ? 'Desliza hacia abajo para intentar de nuevo.' : 'Cargando datos…'} />
        ) : tab === 'resumen' ? (
          <Resumen t={t} d={datos} now={now} />
        ) : tab === 'dentro' ? (
          <Dentro t={t} d={datos} now={now} />
        ) : tab === 'cajas' ? (
          <Cajas t={t} d={datos} now={now} />
        ) : (
          <Pendientes t={t} d={datos} now={now} />
        )}

        {boot ? (
          <Text style={{ color: t.suave, fontSize: 11, textAlign: 'center', marginTop: 8 }}>
            {boot.app} {boot.version}
            {boot.lic?.cliente ? ' · ' + boot.lic.cliente : ''}
          </Text>
        ) : null}
      </ScrollView>
    </View>
  );
}

function Resumen({ t, d, now }: { t: Tema; d: Datos; now: number }) {
  const hoy = diaDe(now);
  const r = useMemo(() => resumenDia(d, hoy), [d, hoy]);
  const mes = useMemo(() => resumenMes(d, mesDe(now)), [d, now]);
  const dentro = vigentes(d).length;
  const cap = d.cfg?.capacidad || 0;
  const abiertas = d.turnos.filter((x) => !x.fin);
  const pendMonto = d.pendientes.reduce((a, p) => a + p.monto, 0);
  return (
    <>
      <View style={s.grid}>
        <Kpi t={t} label="Cobrado hoy" valor={money(r.total)} sub={pl(r.tickets.length, 'ticket cerrado', 'tickets cerrados')} color={t.acento} />
        <Kpi t={t} label="Neto hoy" valor={money(r.neto)} sub={'Gastos ' + money(r.gastos)} />
        <Kpi t={t} label="Dentro ahora" valor={String(dentro) + (cap ? ' / ' + cap : '')} sub={pl(r.entradas, 'entrada hoy', 'entradas hoy')} />
        <Kpi t={t} label="Cajas abiertas" valor={String(abiertas.length)} sub={abiertas.map((x) => x.usuario).join(', ') || 'Ninguna'} />
        <Kpi t={t} label="Pendientes" valor={String(d.pendientes.length)} sub={money(pendMonto)} color={d.pendientes.length ? t.aviso : undefined} />
        <Kpi t={t} label="Pérdidas hoy" valor={money(r.perdidas)} sub={pl(r.canceladosLista.length, 'cancelado', 'cancelados')} color={r.perdidas ? t.mal : undefined} />
      </View>
      {cap ? (
        <Card t={t} titulo="Ocupación">
          <Text style={{ color: t.suave }}>
            {dentro} de {cap} espacios ({Math.round((dentro / cap) * 100)}%)
          </Text>
          <Barra t={t} valor={dentro / cap} />
        </Card>
      ) : null}
      <Card t={t} titulo="Por forma de pago">
        {Object.keys(r.porMetodo).length ? (
          Object.entries(r.porMetodo)
            .sort((a, b) => b[1].monto - a[1].monto)
            .map(([k, v]) => <Fila key={k} t={t} izq={k} sub={pl(v.n, 'cobro', 'cobros')} der={money(v.monto)} />)
        ) : (
          <Vacio t={t} texto="Todavía no hay cobros hoy." />
        )}
        {r.sellados.n ? <Text style={{ color: t.suave, fontSize: 12, marginTop: 6 }}>Los tickets sellados no suman al total cobrado.</Text> : null}
      </Card>
      <Card t={t} titulo="Por usuario">
        {Object.keys(r.porCobrador).length ? (
          Object.entries(r.porCobrador)
            .sort((a, b) => b[1].monto - a[1].monto)
            .map(([k, v]) => <Fila key={k} t={t} izq={k} sub={pl(v.n, 'cobro', 'cobros')} der={money(v.monto)} />)
        ) : (
          <Vacio t={t} texto="Sin cobros." />
        )}
      </Card>
      <Card t={t} titulo="Últimos cobros">
        {r.tickets.length ? (
          r.tickets.slice(0, 15).map((x) => (
            <Fila
              key={x.id}
              t={t}
              izq={numTxt(x) + ' · ' + (x.categoria || '')}
              sub={hora(Number(x.pago) || x.salida) + ' · ' + (x.metodo || '') + ' · ' + (x.cobSalida || '') + (x.sinTicket ? ' · sin ticket' : '') + (x.dePendiente ? ' · pendiente pagado' : '')}
              der={money(x.monto)}
              derSub={dur(x.min)}
            />
          ))
        ) : (
          <Vacio t={t} texto="Sin cobros hoy." />
        )}
      </Card>
      {r.gastosLista.length ? (
        <Card t={t} titulo="Gastos de hoy">
          {r.gastosLista.map((g, i) => (
            <Fila key={g.id || i} t={t} izq={g.concepto || 'Gasto'} sub={hora(g.ts) + ' · ' + (g.cob || '')} der={money(g.monto)} colorDer={t.mal} />
          ))}
        </Card>
      ) : null}
      {r.canceladosLista.length || r.perdidasLista.length ? (
        <Card t={t} titulo="Cancelados y pérdidas de hoy">
          {[...r.canceladosLista.map((c) => ({ ...c, k: 'Cancelado' })), ...r.perdidasLista.map((p) => ({ ...p, k: 'Pérdida' }))]
            .sort((a, b) => b.ts - a.ts)
            .map((x, i) => (
              <Fila key={i} t={t} izq={x.k + ' · ' + (x.placa || '')} sub={hora(x.ts) + ' · ' + (x.motivo || '') + ' · ' + (x.cob || '')} der={money(x.monto)} colorDer={t.mal} />
            ))}
        </Card>
      ) : null}
      <Card t={t} titulo="Este mes">
        <Fila t={t} izq="Ingresos" der={money(mes.ing)} />
        <Fila t={t} izq="Gastos" der={money(mes.gas)} />
        <Fila t={t} izq="Pérdidas" der={money(mes.per)} />
        <Fila t={t} izq="Neto (ingresos − gastos)" der={money(mes.neto)} colorDer={t.acento} />
      </Card>
    </>
  );
}

function Dentro({ t, d, now }: { t: Tema; d: Datos; now: number }) {
  const vs = vigentes(d);
  const estimado = vs.reduce((a, x) => a + calc(d.cfg, x.entrada, now, precioDe(d.cfg, x)).monto, 0);
  return (
    <>
      <View style={s.grid}>
        <Kpi t={t} label="Vehículos dentro" valor={String(vs.length)} sub={d.cfg?.capacidad ? 'de ' + d.cfg.capacidad + ' espacios' : undefined} />
        <Kpi t={t} label="Por cobrar si salen ya" valor={money(estimado)} sub="Estimado con la tarifa" />
      </View>
      <Card t={t} titulo="Vehículos dentro">
        {vs.length ? (
          vs.map((x) => {
            const c = calc(d.cfg, x.entrada, now, precioDe(d.cfg, x));
            const ubic = [x.zona, x.plaza].filter((v) => v !== undefined && v !== '').join(' ');
            return (
              <Fila
                key={x.id}
                t={t}
                izq={numTxt(x) + (x.categoria ? ' · ' + x.categoria : '')}
                sub={'Entró ' + (diaDe(x.entrada) === diaDe(now) ? hora(x.entrada) : corta(x.entrada)) + (ubic ? ' · ' + ubic : '') + (x.empresa ? ' · ' + x.empresa : '')}
                der={dur(c.min)}
                derSub={money(c.monto)}
                colorDer={c.min >= 24 * 60 ? t.mal : undefined}
              />
            );
          })
        ) : (
          <Vacio t={t} texto="No hay vehículos dentro." />
        )}
      </Card>
    </>
  );
}

function Cajas({ t, d, now }: { t: Tema; d: Datos; now: number }) {
  const abiertas = d.turnos.filter((x) => !x.fin);
  const cerradas = d.turnos.filter((x) => x.fin).slice(0, 30);
  return (
    <>
      <Card t={t} titulo="Cajas abiertas">
        {abiertas.length ? (
          abiertas.map((x) => {
            const e = esperadoTurno(d, x, now);
            return (
              <View key={x.id} style={[st.caja, { borderColor: t.borde }]}>
                <Text style={{ color: t.texto, fontWeight: '700', fontSize: 15 }}>{x.usuario}</Text>
                <Text style={{ color: t.suave, fontSize: 12, marginBottom: 6 }}>Abrió {corta(x.inicio)}</Text>
                <Fila t={t} izq="Fondo inicial" der={money(Number(x.fondo) || 0)} />
                <Fila t={t} izq="Efectivo cobrado" sub={pl(e.n, 'cobro', 'cobros')} der={money(e.ef)} />
                <Fila t={t} izq="Otros medios" der={money(e.otros)} />
                <Fila t={t} izq="Gastos" der={money(e.gas)} />
                <Fila t={t} izq="Efectivo que debe tener" der={money(e.esperado)} colorDer={t.acento} />
              </View>
            );
          })
        ) : (
          <Vacio t={t} texto="No hay cajas abiertas." />
        )}
      </Card>
      <Card t={t} titulo="Cierres recientes">
        {cerradas.length ? (
          cerradas.map((x) => {
            const dif = Number(x.diferencia) || 0;
            return (
              <Fila
                key={x.id}
                t={t}
                izq={x.usuario}
                sub={corta(x.inicio) + ' → ' + corta(x.fin!) + ' · contó ' + money(Number(x.contado) || 0)}
                der={dif === 0 ? 'Cuadra' : (dif > 0 ? 'Sobra ' : 'Falta ') + money(Math.abs(dif))}
                derSub={'Esperado ' + money(Number(x.esperado) || 0)}
                colorDer={dif === 0 ? t.bien : dif > 0 ? t.aviso : t.mal}
              />
            );
          })
        ) : (
          <Vacio t={t} texto="Todavía no hay cierres." />
        )}
      </Card>
    </>
  );
}

function Pendientes({ t, d, now }: { t: Tema; d: Datos; now: number }) {
  const ps = [...d.pendientes].sort((a, b) => a.salida - b.salida);
  const vencidos = ps.filter((p) => now > vence(d.cfg, p));
  return (
    <>
      <View style={s.grid}>
        <Kpi t={t} label="Pendientes" valor={String(ps.length)} sub={money(ps.reduce((a, p) => a + p.monto, 0))} />
        <Kpi t={t} label="Vencidos" valor={String(vencidos.length)} sub={money(vencidos.reduce((a, p) => a + p.monto, 0))} color={vencidos.length ? t.mal : undefined} />
      </View>
      <Card t={t} titulo="Salidas con pago pendiente">
        {ps.length ? (
          ps.map((p) => {
            const venc = now > vence(d.cfg, p);
            return (
              <Fila
                key={p.id}
                t={t}
                izq={numTxt(p) + (p.quien ? ' · ' + p.quien : '')}
                sub={'Salió ' + corta(p.salida) + ' · ' + (p.cobSalida || '') + (venc ? ' · VENCIDO' : ' · vence ' + corta(vence(d.cfg, p)))}
                der={money(p.monto)}
                colorDer={venc ? t.mal : t.aviso}
              />
            );
          })
        ) : (
          <Vacio t={t} texto="No hay pagos pendientes." />
        )}
      </Card>
    </>
  );
}

const st = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 16, paddingVertical: 10, borderBottomWidth: StyleSheet.hairlineWidth },
  nombre: { fontSize: 20, fontWeight: '800' },
  punto: { width: 8, height: 8, borderRadius: 4, marginRight: 6 },
  tabs: { flexDirection: 'row', borderBottomWidth: StyleSheet.hairlineWidth },
  tab: { flex: 1, alignItems: 'center', paddingVertical: 12, borderBottomWidth: 3, borderBottomColor: 'transparent' },
  banner: { borderRadius: 12, padding: 12, marginBottom: 12 },
  bannerTit: { color: '#fff', fontWeight: '700', marginBottom: 4 },
  bannerTxt: { color: '#fff' },
  caja: { borderTopWidth: StyleSheet.hairlineWidth, paddingTop: 10, marginTop: 6 },
});
