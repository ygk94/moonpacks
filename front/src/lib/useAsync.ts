import { useCallback, useEffect, useRef, useState } from "react";

/** Charge une valeur asynchrone ; `reload()` relance. Ignore les réponses périmées. */
export function useAsync<T>(
  load: () => Promise<T>,
  deps: unknown[],
): { data: T | undefined; error: unknown; loading: boolean; reload: () => void } {
  const [state, setState] = useState<{ data?: T; error?: unknown; loading: boolean }>({ loading: true });
  const seq = useRef(0);
  const run = useCallback(() => {
    const id = ++seq.current;
    setState((s) => ({ ...s, loading: true }));
    load().then(
      (data) => id === seq.current && setState({ data, loading: false }),
      (error) => id === seq.current && setState((s) => ({ ...s, error, loading: false })),
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  useEffect(run, [run]);
  return { data: state.data, error: state.error, loading: state.loading, reload: run };
}
