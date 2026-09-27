import fs from "node:fs";
import path from "node:path";

const projectRoot = process.cwd();

const sourceDir = path.join(
  projectRoot,
  "..",
  "data-science",
  "outputs"
);

const targetDir = path.join(
  projectRoot,
  "public",
  "data",
  "intelligence"
);

fs.mkdirSync(targetDir, { recursive: true });

const files = {
  "intelligence_results.json": "results.json",
  "intelligence_summary.json": "summary.json",
  "validation_metrics.json": "validation_metrics.json",
};

for (const [sourceName, targetName] of Object.entries(files)) {
  const source = path.join(sourceDir, sourceName);
  const target = path.join(targetDir, targetName);

  if (!fs.existsSync(source)) {
    throw new Error(`Missing approved intelligence output: ${source}`);
  }

  fs.copyFileSync(source, target);
  console.log(`Generated: ${targetName}`);
}

console.log("Post #3 intelligence package generated successfully.");
