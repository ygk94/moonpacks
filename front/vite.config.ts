import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Écoute locale par défaut (dev et preview) ; DEV_HOST=0.0.0.0 npm run dev pour ouvrir au réseau local
// (test sur un téléphone, par exemple).
const host = process.env.DEV_HOST || "127.0.0.1";

export default defineConfig({
  plugins: [react()],
  server: { port: 5173, host },
  preview: { host },
});
