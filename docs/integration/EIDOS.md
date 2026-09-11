# Eidos Integration

Eidos is the reference downstream AI-native experience runtime and exists as a separate project.

Boundary:
```text
Experience Compiler -> UIDL -> Eidos
```

The compiler must not generate Eidos-private component JSON. UIDL is the compatibility boundary so either project can evolve independently.

M0 compatibility target: UIDL 0.1.0.
