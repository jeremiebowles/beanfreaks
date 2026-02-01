import fs from "node:fs";
import path from "node:path";

const p = path.join(process.cwd(), "dist", ".nojekyll");
fs.mkdirSync(path.dirname(p), { recursive: true });
fs.writeFileSync(p, "");
console.log("touched dist/.nojekyll");
