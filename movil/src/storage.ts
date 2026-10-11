import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

export type Conexion = { url: string; usuario: string; pin: string };

const KEY = 'parqcontrol_conexion';

// En web (solo para probar) no hay SecureStore
const web = Platform.OS === 'web';

export async function leerConexion(): Promise<Conexion | null> {
  try {
    const s = web ? globalThis.localStorage?.getItem(KEY) : await SecureStore.getItemAsync(KEY);
    return s ? (JSON.parse(s) as Conexion) : null;
  } catch {
    return null;
  }
}

export async function guardarConexion(c: Conexion) {
  const s = JSON.stringify(c);
  if (web) globalThis.localStorage?.setItem(KEY, s);
  else await SecureStore.setItemAsync(KEY, s);
}

export async function borrarConexion() {
  if (web) globalThis.localStorage?.removeItem(KEY);
  else await SecureStore.deleteItemAsync(KEY);
}
