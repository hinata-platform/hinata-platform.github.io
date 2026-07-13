---
title: Object storage (S3, GCS, Azure)
description: Hinata keeps attachments and avatars in object storage — the bundled MinIO, any S3-compatible provider (AWS S3, Google Cloud Storage, R2, Spaces, …) or Azure Blob Storage — with presigned downloads and randomized keys.
---

# Object storage (S3, GCS, Azure)

Issue attachments and user avatars are not stored in MongoDB — they live in
**object storage**. Hinata supports two backends, selected with
`HINATA_STORAGE_PROVIDER`:

- **`s3`** (default) — any S3-compatible store: the **bundled MinIO**, **AWS S3**,
  **Google Cloud Storage** (S3-interoperable XML API), **Cloudflare R2**,
  **DigitalOcean Spaces**, Backblaze B2, Wasabi, Ceph, a managed MinIO, …
- **`azure`** — **Azure Blob Storage** through its native API (Azure does not
  speak the S3 protocol).

This page covers the default setup, how downloads stay secure, and how to swap in
an external provider.

## MinIO in the default stack

The production `docker-compose.yml` runs a MinIO container alongside the server.
It is attached to the compose **`local-storage` profile**, which is on by default
(`COMPOSE_PROFILES=local-storage` in `.env.example`):

```yaml
minio:
  image: minio/minio:latest
  profiles: [local-storage]
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: ${MINIO_ROOT_USER:-}
    MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-}
  volumes:
    - minio-data:/data
```

The server connects to it over the internal Docker network, reusing the MinIO root
credentials as its S3 access/secret keys:

```yaml
HINATA_S3_ENDPOINT: ${HINATA_S3_ENDPOINT:-http://minio:9000}
HINATA_S3_ACCESS_KEY: ${HINATA_S3_ACCESS_KEY:-${MINIO_ROOT_USER:-}}
HINATA_S3_SECRET_KEY: ${HINATA_S3_SECRET_KEY:-${MINIO_ROOT_PASSWORD:-}}
HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
```

So in the default stack you only set four things in `.env`:

```properties
COMPOSE_PROFILES=local-storage
MINIO_ROOT_USER=hinata
MINIO_ROOT_PASSWORD=change-me-to-a-long-random-value
HINATA_S3_BUCKET=hinata
```

The MinIO **web console** is available on port `9001` and the **S3 API** on `9000`.
In local dev (`docker-compose.dev.yml`) both are published on loopback —
`http://localhost:9001` (console) and `http://localhost:9000` (API) — with the dev
keys `hinata` / `hinata-dev-secret`.

!!! warning "Change the MinIO password before production"
    `hinata-dev-secret` is a development default. Set a long random
    `MINIO_ROOT_PASSWORD` (e.g. from `./deploy/generate-secrets.sh`) for any real
    deployment, and never publish the MinIO ports to the public internet — only the
    server needs to reach them.

## The bucket is created for you

You do not have to pre-create the bucket. On the first upload the server checks
whether `HINATA_S3_BUCKET` exists and calls `makeBucket` if it doesn't. The bucket
stays **private** — nothing is ever made public-read. Every download is brokered by
the server (see below), so objects are never served straight from the bucket.

!!! tip
    If you'd rather create the bucket yourself (for example to set a lifecycle rule
    or bucket policy in advance), do so with the default name `hinata`, or set
    `HINATA_S3_BUCKET` to the name you created. The server will happily reuse an
    existing bucket.

## Presigned downloads and randomized keys

Two design choices keep object storage safe by default:

- **Randomized object keys.** A user-supplied file name never becomes the object
  key. The server stores each attachment under a random UUID (optionally behind a
  prefix like `media/` or `avatars/`), so a bucket key cannot be guessed and the
  original file name never touches the bucket layout.
- **Presigned, short-lived downloads.** When a client requests an attachment, the
  server returns a **presigned GET URL** that is valid for **10 minutes** and carries
  a `Content-Disposition: attachment` header (so files download rather than render
  inline). The bucket itself never needs to be public.

This means the S3 credentials stay entirely server-side; clients only ever see
time-limited URLs.

## Live attachment events (SSE)

Attachment changes are pushed to everyone viewing an issue in real time over
**Server-Sent Events**:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

When someone uploads or removes a file — or drops several at once — every open
viewer sees the grid update live, without polling. The stream is in-process per
server instance; for a clustered deployment you would front it with a shared broker.

## Size and content-type limits

Uploads are validated on multiple axes. The defaults:

| Setting | Env / property | Default |
| --- | --- | --- |
| Max size of a single file | `HINATA_STORAGE_MAX_UPLOAD_MB` | `25` MB |
| Max files in one request | `hinata.storage.max-files-per-request` | `10` |
| Max total size of one request | `HINATA_STORAGE_MAX_REQUEST_MB` | `100` MB |

Allowed content types are an explicit allow-list — PNG, JPEG, GIF, WebP, PDF, plain
text, CSV, ZIP, JSON, and the OOXML Word/Excel documents. A few important safeguards:

- **`image/svg+xml` is intentionally excluded**, because SVG can embed JavaScript
  (a stored-XSS risk).
- **Magic-byte verification.** For binary types the server checks the file's leading
  bytes against the declared content type, so a file cannot masquerade as, say, a PNG.
- A rejected upload returns a localized, stable error (`error.storage.fileTooLarge`,
  `error.storage.fileTypeNotAllowed`, `error.storage.contentMismatch`).

!!! note "Two size ceilings work together"
    Spring's multipart limits (`max-file-size` / `max-request-size`, driven by the
    same MB values) are the outer guard; the app then enforces the file count and
    aggregate size on top. Raise all of them together if you need larger uploads.

## Using an external provider instead of MinIO

To use an external store, turn the bundled MinIO off by clearing the compose
profile in `.env` —

```properties
COMPOSE_PROFILES=
```

— and configure one of the providers below. The `MINIO_ROOT_*` variables can then
be removed.

### AWS S3

```properties
HINATA_S3_ENDPOINT=https://s3.eu-central-1.amazonaws.com
HINATA_S3_ACCESS_KEY=AKIA...
HINATA_S3_SECRET_KEY=your-secret-access-key
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_REGION=eu-central-1
```

### Google Cloud Storage

GCS speaks S3 through its **interoperable XML API**. Create **HMAC keys** in the
Cloud Console under *Cloud Storage → Settings → Interoperability* (for a service
account, recommended) and point Hinata at the interop endpoint:

```properties
HINATA_S3_ENDPOINT=https://storage.googleapis.com
HINATA_S3_ACCESS_KEY=GOOG1E...          # HMAC access id
HINATA_S3_SECRET_KEY=your-hmac-secret
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_ADDRESSING_STYLE=path
```

### Azure Blob Storage

Azure has no S3 API, so Hinata talks to it natively. Switch the provider and pass
the storage account's **connection string** (portal → storage account → *Access
keys*). An account-key connection string is required — presigned downloads are
issued as SAS URLs:

```properties
HINATA_STORAGE_PROVIDER=azure
HINATA_AZURE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
HINATA_S3_BUCKET=hinata   # used as the blob container name
```

### Other S3-compatible providers

Cloudflare R2, DigitalOcean Spaces, Backblaze B2, Wasabi, Ceph, Hetzner, a managed
MinIO, … all work with the same `HINATA_S3_*` variables — endpoint, keys and region
come from the provider's dashboard.

Notes:

- **`HINATA_S3_REGION`** defaults to `us-east-1`; set it to your bucket's region for
  AWS and providers that care about it.
- **`HINATA_S3_ADDRESSING_STYLE`** (default `auto`) controls S3 URL addressing:
  `auto` picks virtual-host style for AWS endpoints and path style elsewhere, which
  is right for almost everyone; set `path` or `virtual-host` explicitly if your
  provider requires it.
- Use HTTPS for any endpoint crossing the network.
- The credentials need permission to `PutObject`, `GetObject`, `DeleteObject`,
  `ListBucket`, and (unless you pre-create the bucket) `CreateBucket` — or the
  Azure equivalents (the container is created automatically too).
- If storage is left unconfigured (blank access key, or blank connection string
  with `provider=azure`), attachment and avatar endpoints respond with
  `error.storage.notConfigured` — the rest of Hinata still works, you just can't
  upload files.
- **Switching providers does not migrate existing objects.** Copy the bucket
  contents first (`mc mirror`, `aws s3 sync`, `azcopy`) if the instance already
  holds data.

!!! tip "Keep buckets private"
    Whichever provider you use, keep the bucket **private**. Hinata never needs
    public-read: it always hands out short-lived presigned URLs, so public access
    would only widen your attack surface.

See the [Configuration reference](/en/configuration.html) for the full variable
list, and [MongoDB & X.509](/en/database.html) for the database side of the stack.
