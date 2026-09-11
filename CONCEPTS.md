# Concepts

## Semantic Snapshot
A versioned transport representation of business/application/command semantics received from an upstream system such as EVO.

## Compiler
A deterministic transformation from a semantic snapshot to an Interaction Definition.

## UIDL
User Interaction Definition Language. A runtime-neutral, serializable interaction contract.

## Form Compiler
The M0 compiler that transforms command input fields into a confirmation form.

## Runtime
A consumer that renders or executes UIDL. Eidos is the first reference runtime.

## Command Intent
A user-confirmed interaction result that identifies a command and validated input. Experience Compiler describes this interaction but never executes the command.
