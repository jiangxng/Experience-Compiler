-- Reference canonical relational projection. Migrate through versioned migrations; never edit deployed history.
CREATE TABLE IF NOT EXISTS ec_knowledge_record (
  record_id uuid PRIMARY KEY,
  schema_version text NOT NULL,
  kind text NOT NULL,
  subject text NOT NULL,
  predicate text NOT NULL,
  value_json jsonb NOT NULL,
  scope_json jsonb NOT NULL,
  provenance_json jsonb NOT NULL,
  confidence double precision NOT NULL CHECK (confidence BETWEEN 0 AND 1),
  valid_from timestamptz,
  valid_to timestamptz,
  observed_at timestamptz NOT NULL,
  status text NOT NULL,
  tags text[] NOT NULL DEFAULT '{}',
  supersedes uuid[] NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ec_knowledge_subject_predicate_idx ON ec_knowledge_record(subject,predicate);
CREATE INDEX IF NOT EXISTS ec_knowledge_kind_status_idx ON ec_knowledge_record(kind,status);
CREATE INDEX IF NOT EXISTS ec_knowledge_validity_idx ON ec_knowledge_record(valid_from,valid_to);
CREATE INDEX IF NOT EXISTS ec_knowledge_scope_gin ON ec_knowledge_record USING gin(scope_json);
CREATE INDEX IF NOT EXISTS ec_knowledge_value_gin ON ec_knowledge_record USING gin(value_json);

CREATE TABLE IF NOT EXISTS ec_learning_strategy (
  strategy_id text NOT NULL,
  version text NOT NULL,
  body_json jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY(strategy_id,version)
);
CREATE TABLE IF NOT EXISTS ec_strategy_evaluation (
  evaluation_id uuid PRIMARY KEY,
  strategy_id text NOT NULL,
  strategy_version text NOT NULL,
  sample_count bigint NOT NULL,
  metrics_json jsonb NOT NULL,
  notes text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY(strategy_id,strategy_version) REFERENCES ec_learning_strategy(strategy_id,version)
);
