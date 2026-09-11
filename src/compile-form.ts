import type { EvoExperienceSnapshotV1, SemanticField, UidlControl, UidlField, UidlFormV01 } from "./contracts.js";
import { validateSnapshot } from "./validate.js";

const controlBySemanticType: Record<SemanticField["semanticType"], UidlControl> = {
  Text: "text",
  Quantity: "number",
  Money: "money",
  Currency: "select",
  CustomerRef: "reference",
  ItemRef: "reference",
  WarehouseRef: "reference",
  Enum: "select",
  Date: "date"
};

function compileField(field: SemanticField): UidlField {
  const control = controlBySemanticType[field.semanticType];
  if (!control) throw new Error(`Unsupported semantic type: ${String(field.semanticType)}`);
  const validation = field.min === undefined && field.max === undefined ? undefined : {
    ...(field.min !== undefined ? { min: field.min } : {}),
    ...(field.max !== undefined ? { max: field.max } : {})
  };
  return {
    key: field.key,
    label: field.label,
    semanticType: field.semanticType,
    control,
    required: field.required,
    ...(field.readOnly !== undefined ? { readOnly: field.readOnly } : {}),
    ...(field.unit ? { unit: field.unit } : {}),
    ...(field.options ? { options: field.options.map(o => ({...o})) } : {}),
    ...(validation ? { validation } : {})
  };
}

export function compileForm(snapshot: EvoExperienceSnapshotV1): UidlFormV01 {
  validateSnapshot(snapshot);
  return {
    contractVersion: "0.1.0",
    kind: "form",
    id: `${snapshot.application.code}:${snapshot.command.code}`,
    title: snapshot.command.name,
    purpose: "execute-command",
    command: { code: snapshot.command.code, inputVersion: snapshot.command.inputVersion },
    fields: snapshot.fields.map(compileField),
    actions: [{
      id: "submit",
      label: snapshot.command.name,
      type: "submit",
      command: snapshot.command.code,
      requiresConfirmation: snapshot.command.requiresConfirmation ?? true
    }],
    metadata: { sourceApplication: snapshot.application.code, sourceContract: snapshot.contractVersion }
  };
}
