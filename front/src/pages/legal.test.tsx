import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { DemoBanner } from "../components/Header";
import { Legal } from "./Legal";

describe("demo honesty", () => {
  it("says on every page that the token delivery is simulated", () => {
    const html = renderToStaticMarkup(<DemoBanner />);
    expect(html).toContain("NEAR testnet");
    expect(html).toContain("Token delivery simulated");
    expect(html).toContain("Simulated burns");
    expect(html).toContain('href="#/legal"');
  });

  it("legal notice: publisher, host, simulation, personal data, under the site name", () => {
    const html = renderToStaticMarkup(<Legal />);
    for (const s of ["Publisher", "Hosting", "Vercel Inc.", "Simulation", "Personal data", "Moonpacks"]) expect(html).toContain(s);
    expect(html).not.toMatch(/Memaster|to be completed/);
  });
});
