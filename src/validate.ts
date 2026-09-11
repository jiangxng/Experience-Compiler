import type { EvoExperienceSnapshotV1 } from "./contracts.js";

export function validateSnapshot(snapshot: EvoExperienceSnapshotV1): void {
  if (snapshot.contractVersion !== "1.0.0") throw new Error(`Unsupported semantic contract: ${snapshot.contractVersion}`);
  if (!snapshot.application.code || !snapshot.command.code) throw new Error("Application and command codes are required");
  const seen = new Set<string>();
  for (const field of snapshot.fields) {
    if (!field.key || !field.label) throw new Error("Field key and label are required");
    if (seen.has(field.key)) throw new Error(`Duplicate field key: ${field.key}`);
    seen.add(field.key);
    if (field.semanticType === "Enum" && (!field.options || field.options.length === 0)) throw new Error(`Enum field ${field.key} requires options`);
    if (field.min !== undefined && field.max !== undefined && field.min > field.max) throw new Error(`Invalid range for ${field.key}`);
  }
}
