import fs from "node:fs";
import { compileForm } from "../dist/index.js";
const input = JSON.parse(fs.readFileSync(new URL("../examples/evo-sales-order.snapshot.json", import.meta.url), "utf8"));
console.log(JSON.stringify(compileForm(input), null, 2));
