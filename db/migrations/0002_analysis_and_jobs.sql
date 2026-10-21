-- TG-R06: source attribution, versioned analysis inputs, findings and job records.

CREATE TABLE chunks (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    document_version_id uuid NOT NULL,
    chunker_version text NOT NULL CHECK (length(btrim(chunker_version)) BETWEEN 1 AND 100),
    ordinal integer NOT NULL CHECK (ordinal >= 0),
    content text NOT NULL CHECK (length(btrim(content)) > 0),
    char_start integer NOT NULL CHECK (char_start >= 0),
    char_end integer NOT NULL CHECK (char_end > char_start),
    source_locator jsonb NOT NULL CHECK (jsonb_typeof(source_locator) = 'object'),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (document_version_id, organization_id)
        REFERENCES document_versions(id, organization_id),
    UNIQUE (document_version_id, chunker_version, ordinal),
    UNIQUE (id, organization_id, document_version_id)
);
CREATE INDEX chunks_document_idx ON chunks(organization_id, document_version_id);
-- Model-specific vectors and indexes are intentionally deferred to TG-D08/TG-D14.

CREATE TABLE analysis_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    tender_id uuid NOT NULL,
    company_profile_version_id uuid NOT NULL,
    requested_by uuid NOT NULL,
    configuration jsonb NOT NULL CHECK (jsonb_typeof(configuration) = 'object'),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (tender_id, organization_id) REFERENCES tenders(id, organization_id),
    FOREIGN KEY (company_profile_version_id, organization_id)
        REFERENCES company_profile_versions(id, organization_id),
    FOREIGN KEY (organization_id, requested_by)
        REFERENCES memberships(organization_id, user_id),
    UNIQUE (id, organization_id),
    UNIQUE (id, organization_id, tender_id),
    UNIQUE (id, organization_id, company_profile_version_id)
);
CREATE INDEX analysis_runs_tender_idx ON analysis_runs(organization_id, tender_id, created_at DESC);

CREATE TABLE analysis_run_documents (
    run_id uuid NOT NULL,
    organization_id uuid NOT NULL,
    tender_id uuid NOT NULL,
    document_version_id uuid NOT NULL,
    PRIMARY KEY (run_id, organization_id, document_version_id),
    FOREIGN KEY (run_id, organization_id, tender_id)
        REFERENCES analysis_runs(id, organization_id, tender_id),
    FOREIGN KEY (tender_id, organization_id, document_version_id)
        REFERENCES tender_documents(tender_id, organization_id, document_version_id)
);

CREATE TABLE requirements (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    run_id uuid NOT NULL,
    label text NOT NULL CHECK (length(btrim(label)) BETWEEN 1 AND 100),
    text text NOT NULL CHECK (length(btrim(text)) > 0),
    source_document_version_id uuid NOT NULL,
    source_chunk_id uuid NOT NULL,
    source_quote text NOT NULL CHECK (length(btrim(source_quote)) > 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (run_id, organization_id, source_document_version_id)
        REFERENCES analysis_run_documents(run_id, organization_id, document_version_id),
    FOREIGN KEY (source_chunk_id, organization_id, source_document_version_id)
        REFERENCES chunks(id, organization_id, document_version_id),
    UNIQUE (run_id, label),
    UNIQUE (id, organization_id, run_id)
);
CREATE INDEX requirements_run_idx ON requirements(organization_id, run_id);

CREATE TABLE findings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    run_id uuid NOT NULL,
    requirement_id uuid NOT NULL,
    company_profile_version_id uuid NOT NULL,
    company_evidence_id uuid,
    status text NOT NULL CHECK (status IN ('met', 'unmet', 'unknown')),
    explanation text NOT NULL CHECK (length(btrim(explanation)) > 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (requirement_id, organization_id, run_id)
        REFERENCES requirements(id, organization_id, run_id),
    FOREIGN KEY (run_id, organization_id, company_profile_version_id)
        REFERENCES analysis_runs(id, organization_id, company_profile_version_id),
    FOREIGN KEY (company_evidence_id, organization_id, company_profile_version_id)
        REFERENCES company_evidence(id, organization_id, company_profile_version_id),
    CHECK (status = 'unknown' OR company_evidence_id IS NOT NULL),
    UNIQUE (run_id, requirement_id)
);
CREATE INDEX findings_run_idx ON findings(organization_id, run_id);

CREATE TABLE processing_jobs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES organizations(id),
    kind text NOT NULL CHECK (kind IN ('ingestion', 'analysis')),
    run_id uuid,
    document_version_id uuid,
    idempotency_key text NOT NULL CHECK (length(btrim(idempotency_key)) BETWEEN 1 AND 200),
    status text NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'completed', 'failed', 'cancelled')),
    attempt integer NOT NULL DEFAULT 0 CHECK (attempt >= 0),
    max_attempts integer NOT NULL DEFAULT 3 CHECK (max_attempts BETWEEN 1 AND 10),
    available_at timestamptz NOT NULL DEFAULT now(),
    lease_expires_at timestamptz,
    error_code text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (run_id, organization_id) REFERENCES analysis_runs(id, organization_id),
    FOREIGN KEY (document_version_id, organization_id)
        REFERENCES document_versions(id, organization_id),
    CHECK (attempt <= max_attempts),
    CHECK ((kind = 'ingestion' AND document_version_id IS NOT NULL AND run_id IS NULL)
        OR (kind = 'analysis' AND run_id IS NOT NULL AND document_version_id IS NULL)),
    UNIQUE (organization_id, idempotency_key)
);
CREATE INDEX processing_jobs_ready_idx ON processing_jobs(available_at, created_at)
    WHERE status = 'queued';
CREATE INDEX processing_jobs_organization_idx ON processing_jobs(organization_id, status);
CREATE INDEX processing_jobs_run_idx ON processing_jobs(organization_id, run_id);
CREATE INDEX processing_jobs_document_idx ON processing_jobs(organization_id, document_version_id);

DO $$
DECLARE target text;
BEGIN
    FOREACH target IN ARRAY ARRAY[
        'chunks', 'analysis_runs', 'analysis_run_documents', 'requirements', 'findings'
    ] LOOP
        EXECUTE format('CREATE TRIGGER immutable_snapshot BEFORE UPDATE OR DELETE ON %I '
            'FOR EACH ROW EXECUTE FUNCTION reject_snapshot_change()', target);
        EXECUTE format('CREATE TRIGGER immutable_snapshot_truncate BEFORE TRUNCATE ON %I '
            'FOR EACH STATEMENT EXECUTE FUNCTION reject_snapshot_change()', target);
    END LOOP;
END;
$$;
