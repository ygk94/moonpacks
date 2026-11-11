// Routeur minimal par hash (#/shop, #/collection…), sans dépendance.

import { useEffect, useState } from "react";

function current(): string {
  return window.location.hash.replace(/^#/, "") || "/";
}

export function useRoute(): { path: string; params: URLSearchParams } {
  const [hash, setHash] = useState(current());
  useEffect(() => {
    const on = () => setHash(current());
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  const [path, query = ""] = hash.split("?");
  return { path, params: new URLSearchParams(query) };
}

export function navigate(path: string) {
  window.location.hash = path;
}
