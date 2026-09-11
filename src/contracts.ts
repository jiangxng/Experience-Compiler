export type SemanticType =
  | "Text"
  | "Quantity"
  | "Money"
  | "Currency"
  | "CustomerRef"
  | "ItemRef"
  | "WarehouseRef"
  | "Enum"
  | "Date";

export interface SemanticOption { value: string | number | boolean; label: string }
export interface SemanticField {
  key: string;
  label: string;
  semanticType: SemanticType;
  required: boolean;
  readOnly?: boolean;
  unit?: string;
  min?: number;
  max?: number;
  options?: SemanticOption[];
}
export interface EvoExperienceSnapshotV1 {
  contractVersion: "1.0.0";
  application: { code: string; name: string };
  command: { code: string; name: string; inputVersion: string; requiresConfirmation?: boolean };
  fields: SemanticField[];
}
export type UidlControl = "text" | "number" | "money" | "select" | "date" | "reference";
export interface UidlField {
  key: string; label: string; semanticType: string; control: UidlControl; required: boolean;
  readOnly?: boolean; unit?: string; options?: SemanticOption[]; validation?: { min?: number; max?: number; pattern?: string };
}
export interface UidlFormV01 {
  contractVersion: "0.1.0";
  kind: "form";
  id: string;
  title: string;
  purpose: "execute-command";
  command: { code: string; inputVersion: string };
  fields: UidlField[];
  actions: Array<{ id: string; label: string; type: "submit" | "cancel"; command?: string; requiresConfirmation?: boolean }>;
  metadata?: Record<string, unknown>;
}
