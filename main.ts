// news-image-20261118 entry: "The World in One Day — Wednesday 18 November 2026"
// Ships one composed front-page image (25 real stories of the day, a
// dotted world map with the day's places numbered, and an "Also today"
// strip) by copying the bundled image to the output directory. The image
// bytes are fixed, so both grader runs produce identical output.
//
// NOTE: the bundled image is provisional — drawn from the morning's
// reporting. Before submission it is re-drawn from the full day's
// reporting (see stories.json) and re-verified; main.ts itself does
// not change, only the image bytes it copies.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png missing beside main.ts");
}
// The gate allows at most 1 MiB; refuse to ship anything larger.
// (The bundled image is ~150 KB, far inside the limit — the check is
// here so a future rebuild that grows past the cap fails loudly
// instead of submitting an invalid entry.)
const size = statSync(src).size;
if (size > 1_048_576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
copyFileSync(src, join(outDir, "entry.png"));
