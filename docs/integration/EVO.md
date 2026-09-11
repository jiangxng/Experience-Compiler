# EVO Integration

EVO is the reference upstream system and exists as a separate repository/project.

Boundary:
```text
EVO ApplicationDefinition + FieldDefinition + CommandDefinition
        -> versioned Semantic Snapshot
        -> Experience Compiler
```

Experience Compiler must never query EVO tables directly. EVO integration must be through a published transport contract or adapter.

M0 uses `EvoExperienceSnapshotV1` as an intentionally small external snapshot. It is not a claim that EVO internal tables have this exact shape.

Future continuous integration should validate:
1. EVO exports a snapshot conforming to the pinned semantic contract.
2. Experience Compiler compiles it to UIDL.
3. Eidos consumes the UIDL fixture.
