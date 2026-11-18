/**
 * Entry point for the news-image-20261118 submission.
 *
 * The artwork for this entry — a one-page newspaper front page for
 * Wednesday 18 November 2026 — was rendered ahead of time from
 * stories.json and is committed to this repository as entry.png.
 * There is nothing to draw at run time: this program's whole job is
 * to deliver that fixed image to the directory the harness names in
 * the MAKEFUN_OUTPUT_DIR environment variable.
 */

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

/** Name of the committed artwork, here and in the output directory. */
const IMAGE_NAME = "entry.png";

/** Absolute path of the entry.png committed beside this file. */
function sourceImage(): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return resolve(here, IMAGE_NAME);
}

/** The output directory from the environment, or a thrown error. */
function outputDirectory(): string {
  const dir = process.env.MAKEFUN_OUTPUT_DIR;
  if (dir === undefined || dir.trim() === "") {
    throw new Error(
      "MAKEFUN_OUTPUT_DIR is not set; nowhere to publish entry.png",
    );
  }
  return resolve(dir);
}

function main(): void {
  const src = sourceImage();
  if (!existsSync(src)) {
    throw new Error(`source image is missing: ${src}`);
  }

  const dir = outputDirectory();
  mkdirSync(dir, { recursive: true });
  const dest = join(dir, IMAGE_NAME);

  copyFileSync(src, dest);

  const expected = statSync(src).size;
  const bytes = statSync(dest).size;
  if (bytes === 0) {
    throw new Error(`published file is empty: ${dest}`);
  }
  if (bytes !== expected) {
    throw new Error(
      `published file is incomplete: ${dest} has ${bytes} of ${expected} bytes`,
    );
  }
  console.log(`published ${dest} (${bytes} bytes)`);
}

try {
  main();
} catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`news-image-20261118: ${message}`);
  process.exit(1);
}
