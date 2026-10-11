import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import Conectar from './src/Conectar';
import Monitor from './src/Monitor';
import { Conexion, guardarConexion, leerConexion } from './src/storage';
import { useTema } from './src/ui';

export default function App() {
  const t = useTema();
  const [listo, setListo] = useState(false);
  const [con, setCon] = useState<Conexion | null>(null);
  const [editando, setEditando] = useState(false);

  useEffect(() => {
    leerConexion().then((c) => {
      setCon(c);
      setListo(true);
    });
  }, []);

  return (
    <SafeAreaProvider>
      <SafeAreaView style={{ flex: 1, backgroundColor: t.fondo }} edges={['top', 'left', 'right']}>
        <StatusBar style="auto" />
        {!listo ? (
          <View style={{ flex: 1, justifyContent: 'center' }}>
            <ActivityIndicator color={t.acento} />
          </View>
        ) : !con || editando ? (
          <Conectar
            t={t}
            inicial={con}
            onListo={async (c) => {
              await guardarConexion(c);
              setCon(c);
              setEditando(false);
            }}
          />
        ) : (
          <Monitor key={con.url + con.usuario} t={t} con={con} onSalir={() => setEditando(true)} />
        )}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
