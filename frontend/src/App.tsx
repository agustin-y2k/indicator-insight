import { useEffect, useState } from 'react';

type ConnectionState = 'loading' | 'ready' | 'error';

export function App() {
  const [connection, setConnection] = useState<ConnectionState>('loading');

  useEffect(() => {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 5000);
    let active = true;

    async function checkConnection() {
      try {
        const response = await fetch('/api/health/ready', { signal: controller.signal });
        const payload: unknown = await response.json();
        if (
          !response.ok ||
          typeof payload !== 'object' ||
          payload === null ||
          !('status' in payload) ||
          payload.status !== 'ok'
        ) {
          throw new Error('Service unavailable');
        }
        if (active) setConnection('ready');
      } catch {
        if (active) setConnection('error');
      } finally {
        window.clearTimeout(timeout);
      }
    }

    void checkConnection();
    return () => {
      active = false;
      window.clearTimeout(timeout);
      controller.abort();
    };
  }, []);

  return (
    <main>
      <h1>Indicator Insight</h1>
      <p>Entrenamiento de decisiones bajo incertidumbre.</p>
      <p role="status">
        {connection === 'loading' && 'Comprobando conexión…'}
        {connection === 'ready' && 'Conexión disponible.'}
        {connection === 'error' && 'No se pudo conectar. Recargá la página para reintentar.'}
      </p>
      <p>Aún no hay actividades disponibles.</p>
    </main>
  );
}
