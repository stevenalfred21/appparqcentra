import { useState } from 'react';
import { ActivityIndicator, KeyboardAvoidingView, Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { ApiError, ParqApi, normalizarUrl } from './api';
import { Conexion } from './storage';
import { Tema } from './ui';

export default function Conectar({ t, inicial, onListo }: { t: Tema; inicial: Conexion | null; onListo: (c: Conexion) => void }) {
  const [url, setUrl] = useState(inicial?.url || '');
  const [usuario, setUsuario] = useState(inicial?.usuario || '');
  const [pin, setPin] = useState(inicial?.pin || '');
  const [probando, setProbando] = useState(false);
  const [msg, setMsg] = useState('');

  async function probar() {
    const u = normalizarUrl(url);
    if (!u) return setMsg('Escribe la dirección de la computadora central.');
    setProbando(true);
    setMsg('');
    const api = new ParqApi(u);
    try {
      const b = await api.boot();
      if (b.licOK === false) throw new ApiError('licencia', 'Se conectó, pero ParqControl no tiene la licencia activa.');
      if (usuario.trim()) {
        try {
          await api.login(usuario.trim(), pin);
        } catch (e) {
          throw new ApiError('login', 'Se conectó, pero el usuario o el PIN no son correctos.');
        }
      }
      await api.col('abiertos');
      onListo({ url: u, usuario: usuario.trim(), pin });
    } catch (e) {
      const err = e instanceof ApiError ? e : new ApiError('unavailable', String(e));
      setMsg(
        err.code === 'unavailable'
          ? 'No responde ' + u + '. Revisa que ParqControl esté abierto, que la dirección sea correcta y, si estás fuera del parqueo, que Tailscale esté conectado en el teléfono.'
          : err.code === 'login'
            ? usuario.trim()
              ? err.message
              : 'El sistema pide usuario y PIN para ver los datos. Escríbelos abajo.'
            : err.message,
      );
    } finally {
      setProbando(false);
    }
  }

  const inp = [st.inp, { color: t.texto, borderColor: t.borde, backgroundColor: t.card }];
  return (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={{ flex: 1 }}>
      <ScrollView contentContainerStyle={{ padding: 20 }} keyboardShouldPersistTaps="handled">
        <Text style={[st.tit, { color: t.texto }]}>ParqControl Monitor</Text>
        <Text style={{ color: t.suave, marginBottom: 20 }}>Conéctalo a la computadora central del parqueo para ver lo que pasa en vivo.</Text>

        <Text style={[st.lab, { color: t.texto }]}>Dirección de la computadora central</Text>
        <TextInput
          style={inp}
          value={url}
          onChangeText={setUrl}
          placeholder="http://100.64.0.5:8090"
          placeholderTextColor={t.suave}
          autoCapitalize="none"
          autoCorrect={false}
          keyboardType="url"
        />
        <Text style={[st.ayuda, { color: t.suave }]}>
          En el parqueo, la que sale abajo en la pantalla de ParqControl (por ejemplo http://192.168.1.20:8090). Desde fuera, la dirección de Tailscale de esa PC.
        </Text>

        <Text style={[st.lab, { color: t.texto }]}>Usuario (si el sistema lo pide)</Text>
        <TextInput style={inp} value={usuario} onChangeText={setUsuario} placeholder="Nombre del usuario en ParqControl" placeholderTextColor={t.suave} autoCorrect={false} />
        <Text style={[st.lab, { color: t.texto }]}>PIN</Text>
        <TextInput style={inp} value={pin} onChangeText={setPin} placeholder="PIN" placeholderTextColor={t.suave} secureTextEntry keyboardType="number-pad" />

        {msg ? <Text style={{ color: t.mal, marginTop: 14 }}>{msg}</Text> : null}

        <Pressable onPress={probar} disabled={probando} style={({ pressed }) => [st.btn, { backgroundColor: t.acento, opacity: pressed || probando ? 0.7 : 1 }]}>
          {probando ? <ActivityIndicator color="#fff" /> : <Text style={st.btnTxt}>Conectar</Text>}
        </Pressable>
        <View style={{ height: 40 }} />
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const st = StyleSheet.create({
  tit: { fontSize: 26, fontWeight: '800', marginTop: 20, marginBottom: 6 },
  lab: { fontSize: 14, fontWeight: '600', marginTop: 16, marginBottom: 6 },
  inp: { borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 12, fontSize: 16 },
  ayuda: { fontSize: 12, marginTop: 6 },
  btn: { marginTop: 24, borderRadius: 12, paddingVertical: 14, alignItems: 'center' },
  btnTxt: { color: '#fff', fontSize: 16, fontWeight: '700' },
});
