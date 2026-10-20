-- TG-R06: identities, tender documents and immutable company snapshots.
-- PostgreSQL 17. Run with app.db.migrate; do not apply individual files manually.
-- Tenant-aware references always include organization_id.

CREATE TABLE organizations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 200),
    created_at timestamptz NOT NULL DEFAULT now()
);

-- Global authentication identities; memberships assign them to organizations.
-- Authentication itself is TG-T06. No password, token or personal identifier is seeded here.
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    external_subject text NOT NULL UNIQUE CHECK (length(btrim(external_subject)) BETWEEN 1 AND 300),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE memberships (
    organization_id uuid NOT NULL REFERENCES organizations(id),
    user_id uuid NOT NULL REFERENCES users(id),
    role text NOT NULL CHECK (role IN ('owner', 'member', 'viewer')),
    active boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id, user_id)
);
CREATE INDEX memberships_user_idx ON memberships(user_id, organization_id);

CREATE TABLE tenders (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES organizations(id),
    title text NOT NULL CHECK (length(btrim(title)) BETWEEN 1 AND 500),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (id, organization_id)
);
CREATE INDEX tenders_organization_idx ON tenders(organization_id, created_at DESC);

CREATE TABLE documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES organizations(id),
    title text NOT NULL CHECK (length(btrim(title)) BETWEEN 1 AND 500),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (id, organization_id)
);

CREATE TABLE document_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    document_id uuid NOT NULL,
    version integer NOT NULL CHECK (version > 0),
    filename text NOT NULL CHECK (length(btrim(filename)) BETWEEN 1 AND 500),
    media_type text NOT NULL CHECK (media_type IN (
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )),
    size_bytes bigint NOT NULL CHECK (size_bytes > 0),
    sha256 text NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    -- Object references only: actual bytes belong in the private FileStore (TG-R09).
    storage_key text NOT NULL CHECK (
        storage_key LIKE organization_id::text || '/%'
        AND length(storage_key) <= 1000
        AND storage_key !~ '(^|/)\.\.(/|$)'
    ),
    data_class text NOT NULL CHECK (data_class IN ('public', 'private')),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (document_id, organization_id) REFERENCES documents(id, organization_id),
    UNIQUE (document_id, version),
    UNIQUE (organization_id, storage_key),
    UNIQUE (id, organization_id)
);
CREATE INDEX document_versions_organization_idx ON document_versions(organization_id, document_id);

CREATE TABLE tender_documents (
    tender_id uuid NOT NULL,
    organization_id uuid NOT NULL,
    document_version_id uuid NOT NULL,
    PRIMARY KEY (tender_id, organization_id, document_version_id),
    FOREIGN KEY (tender_id, organization_id) REFERENCES tenders(id, organization_id),
    FOREIGN KEY (document_version_id, organization_id)
        REFERENCES document_versions(id, organization_id)
);

CREATE TABLE company_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES organizations(id),
    name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 300),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (id, organization_id)
);

CREATE TABLE company_profile_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    company_profile_id uuid NOT NULL,
    version integer NOT NULL CHECK (version > 0),
    attributes jsonb NOT NULL CHECK (jsonb_typeof(attributes) = 'object'),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (company_profile_id, organization_id)
        REFERENCES company_profiles(id, organization_id),
    UNIQUE (company_profile_id, version),
    UNIQUE (id, organization_id)
);
CREATE INDEX company_profile_versions_organization_idx
    ON company_profile_versions(organization_id, company_profile_id);

CREATE TABLE company_evidence (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    company_profile_version_id uuid NOT NULL,
    document_version_id uuid NOT NULL,
    label text NOT NULL CHECK (length(btrim(label)) BETWEEN 1 AND 500),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (company_profile_version_id, organization_id)
        REFERENCES company_profile_versions(id, organization_id),
    FOREIGN KEY (document_version_id, organization_id)
        REFERENCES document_versions(id, organization_id),
    UNIQUE (id, organization_id, company_profile_version_id)
);
CREATE INDEX company_evidence_profile_idx
    ON company_evidence(organization_id, company_profile_version_id);

CREATE FUNCTION reject_snapshot_change() RETURNS trigger
    LANGUAGE plpgsql SET search_path = pg_catalog
AS $$
BEGIN
    RAISE EXCEPTION USING ERRCODE = '55000',
        MESSAGE = 'Snapshot rows are immutable; insert a new version instead';
END;
$$;

DO $$
DECLARE target text;
BEGIN
    FOREACH target IN ARRAY ARRAY[
        'document_versions', 'company_profile_versions', 'company_evidence'
    ] LOOP
        EXECUTE format('CREATE TRIGGER immutable_snapshot BEFORE UPDATE OR DELETE ON %I '
            'FOR EACH ROW EXECUTE FUNCTION reject_snapshot_change()', target);
        EXECUTE format('CREATE TRIGGER immutable_snapshot_truncate BEFORE TRUNCATE ON %I '
            'FOR EACH STATEMENT EXECUTE FUNCTION reject_snapshot_change()', target);
    END LOOP;
END;
$$;
