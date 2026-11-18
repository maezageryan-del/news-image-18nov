// main.ts — entrypoint for "The World in One Day — Wednesday 18 November 2026"
// (make.fun bounty news-image-20261118, v2).
//
// The entry is a single front-page image, entry.png, composed by
// render.py from stories-v2.json and the engraved artwork in art/.
// This entrypoint delivers that image: it copies entry.png from
// beside this file into the directory named by MAKEFUN_OUTPUT_DIR,
// then verifies the copy landed intact — same byte count, and a real
// PNG signature — before reporting success.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function hasPngSignature(path: string): boolean {
  const head = readFileSync(path).subarray(0, PNG_MAGIC.length);
  return PNG_MAGIC.every((byte, i) => head[i] === byte);
}

// The front page is a fixed-format entry: exactly 1024x1024. The PNG
// IHDR chunk stores width and height as big-endian uint32s at bytes
// 16..24, right after the signature and the chunk header.
function isFrontPageSize(path: string): boolean {
  const head = readFileSync(path).subarray(0, 24);
  const width = head.readUInt32BE(16);
  const height = head.readUInt32BE(20);
  return width === 1024 && height === 1024;
}

function main(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR;
  if (!outDir) {
    fail("MAKEFUN_OUTPUT_DIR is not set; nowhere to deliver entry.png");
  }

  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  if (!existsSync(source)) {
    fail(`entry.png not found beside main.ts (${source})`);
  }
  const sourceSize = statSync(source).size;
  if (sourceSize === 0) {
    fail("entry.png is empty");
  }
  if (!hasPngSignature(source)) {
    fail("entry.png does not start with a PNG signature");
  }
  if (!isFrontPageSize(source)) {
    fail("entry.png is not the 1024x1024 front page");
  }

  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  if (dest !== source) {
    copyFileSync(source, dest);
  }

  const destSize = statSync(dest).size;
  if (destSize !== sourceSize) {
    fail(`copy mismatch: source is ${sourceSize} bytes, delivered ${destSize}`);
  }
  if (!hasPngSignature(dest)) {
    fail("delivered file does not start with a PNG signature");
  }
  console.log(`main.ts: delivered entry.png (${destSize} bytes) to ${dest}`);
}

main();
