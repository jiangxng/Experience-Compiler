# Migration, Upgrade and Rollback

Contracts use semantic versions. Database migrations are append-only files. Expand/contract schema changes allow rolling deployment. Readers tolerate the intended compatibility window; writers emit one declared version. Feature flags gate behavior changes. Migrations that change meaning require data provenance and replay/rebuild plans.
