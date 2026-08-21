import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(new Request("http://localhost/", { headers: { accept: "text/html" } }), {
    ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) },
  }, { waitUntil() {}, passThroughOnException() {} });
}

test("server-renders the campaign dashboard", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /<title>InfluencerTrust AI/);
  assert.match(html, /Performance overview/);
  assert.match(html, /Recommended creators/);
  assert.match(html, /ROI forecast/);
  assert.match(html, /PulseFit Challenge/);
});

test("keeps interactive campaign and scenario controls", async () => {
  const page = await readFile(new URL("../app/page.tsx", import.meta.url), "utf8");
  const layout = await readFile(new URL("../app/layout.tsx", import.meta.url), "utf8");
  assert.match(page, /setId/);
  assert.match(page, /setScenario/);
  assert.match(page, /conservative.*expected.*optimistic/s);
  assert.match(page, /aria-label="Choose campaign"/);
  assert.match(page, /Import reports/);
  assert.match(page, /parseCsv/);
  assert.match(page, /Analyze raw data/);
  assert.match(page, /buildAnalysis/);
  assert.match(layout, /social-preview\.png/);
});
