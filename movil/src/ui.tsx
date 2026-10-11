import { ReactNode } from 'react';
import { StyleSheet, Text, View, useColorScheme } from 'react-native';

const claro = {
  fondo: '#F4F6F8',
  card: '#FFFFFF',
  texto: '#111827',
  suave: '#6B7280',
  borde: '#E5E7EB',
  acento: '#0F766E',
  bien: '#15803D',
  mal: '#B42318',
  aviso: '#B45309',
};
const oscuro: typeof claro = {
  fondo: '#0B0F14',
  card: '#151B23',
  texto: '#F3F4F6',
  suave: '#9CA3AF',
  borde: '#273140',
  acento: '#2DD4BF',
  bien: '#4ADE80',
  mal: '#F87171',
  aviso: '#FBBF24',
};
export type Tema = typeof claro;

export function useTema(): Tema {
  return useColorScheme() === 'dark' ? oscuro : claro;
}

export function Card({ t, titulo, children, extra }: { t: Tema; titulo?: string; children: ReactNode; extra?: ReactNode }) {
  return (
    <View style={[s.card, { backgroundColor: t.card, borderColor: t.borde }]}>
      {titulo ? (
        <View style={s.cardHead}>
          <Text style={[s.cardTit, { color: t.texto }]}>{titulo}</Text>
          {extra}
        </View>
      ) : null}
      {children}
    </View>
  );
}

export function Kpi({ t, label, valor, sub, color }: { t: Tema; label: string; valor: string; sub?: string; color?: string }) {
  return (
    <View style={[s.kpi, { backgroundColor: t.card, borderColor: t.borde }]}>
      <Text style={[s.kpiLab, { color: t.suave }]}>{label}</Text>
      <Text style={[s.kpiVal, { color: color || t.texto }]} numberOfLines={1} adjustsFontSizeToFit>
        {valor}
      </Text>
      {sub ? <Text style={[s.kpiSub, { color: t.suave }]}>{sub}</Text> : null}
    </View>
  );
}

export function Fila({ t, izq, sub, der, derSub, colorDer }: { t: Tema; izq: string; sub?: string; der?: string; derSub?: string; colorDer?: string }) {
  return (
    <View style={[s.fila, { borderColor: t.borde }]}>
      <View style={{ flex: 1, paddingRight: 8 }}>
        <Text style={[s.filaIzq, { color: t.texto }]}>{izq}</Text>
        {sub ? <Text style={[s.filaSub, { color: t.suave }]}>{sub}</Text> : null}
      </View>
      {der !== undefined ? (
        <View style={{ alignItems: 'flex-end' }}>
          <Text style={[s.filaDer, { color: colorDer || t.texto }]}>{der}</Text>
          {derSub ? <Text style={[s.filaSub, { color: t.suave }]}>{derSub}</Text> : null}
        </View>
      ) : null}
    </View>
  );
}

export function Vacio({ t, texto }: { t: Tema; texto: string }) {
  return <Text style={{ color: t.suave, paddingVertical: 10 }}>{texto}</Text>;
}

export function Barra({ t, valor }: { t: Tema; valor: number }) {
  const v = Math.max(0, Math.min(1, valor));
  const color = v >= 0.95 ? t.mal : v >= 0.8 ? t.aviso : t.acento;
  return (
    <View style={[s.barra, { backgroundColor: t.borde }]}>
      <View style={{ width: `${v * 100}%`, height: '100%', backgroundColor: color, borderRadius: 4 }} />
    </View>
  );
}

export const s = StyleSheet.create({
  card: { borderWidth: 1, borderRadius: 14, padding: 14, marginBottom: 12 },
  cardHead: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 },
  cardTit: { fontSize: 16, fontWeight: '700' },
  kpi: { borderWidth: 1, borderRadius: 14, padding: 12, flexBasis: '48%', flexGrow: 1 },
  kpiLab: { fontSize: 12, fontWeight: '600', textTransform: 'uppercase', letterSpacing: 0.4 },
  kpiVal: { fontSize: 22, fontWeight: '700', marginTop: 4, fontVariant: ['tabular-nums'] },
  kpiSub: { fontSize: 12, marginTop: 2 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 12 },
  fila: { flexDirection: 'row', alignItems: 'center', paddingVertical: 10, borderTopWidth: StyleSheet.hairlineWidth },
  filaIzq: { fontSize: 15, fontWeight: '600' },
  filaSub: { fontSize: 12, marginTop: 2 },
  filaDer: { fontSize: 15, fontWeight: '700', fontVariant: ['tabular-nums'] },
  barra: { height: 8, borderRadius: 4, overflow: 'hidden', marginTop: 8 },
});
