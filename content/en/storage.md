---
title: Object storage (S3/MinIO)
description: Hinata keeps attachments and avatars in S3-compatible object storage — MinIO in the default stack, or any external S3 provider — with presigned downloads and randomized keys.
---

# Object storage (S3/MinIO)

Issue attachments and user avatars are not stored in MongoDB — they live in
**S3-compatible object storage**. The default Docker stack ships **MinIO**, but the
server talks to storage through the standard S3 API, so you can point it at AWS S3 or
any other S3-compatible provider without changing code. This page covers the default
setup, how downloads stay secure, and how to swap in an external bucket.

## MinIO in the default stack

The production `docker-compose.yml` runs a MinIO container alongside the server:

```yaml
minio:
  image: minio/minio:latest
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: ${MINIO_ROOT_USER:?set in .env}
    MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:?set in .env}
  volumes:
    - minio-data:/data
```

The server connects to it over the internal Docker network, reusing the MinIO root
credentials as its S3 access/secret keys:

```yaml
HINATA_S3_ENDPOINT: http://minio:9000
HINATA_S3_ACCESS_KEY: ${MINIO_ROOT_USER}
HINATA_S3_SECRET_KEY: ${MINIO_ROOT_PASSWORD}
HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
```

So in the default stack you only set three things in `.env`:

```properties
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

## Using external / AWS S3 instead of MinIO

To use AWS S3 or any other S3-compatible provider (Cloudflare R2, Backblaze B2,
Wasabi, Ceph, a managed MinIO, …), point the same four variables at it and drop the
bundled MinIO container:

```properties
HINATA_S3_ENDPOINT=https://s3.eu-central-1.amazonaws.com
HINATA_S3_ACCESS_KEY=AKIA...
HINATA_S3_SECRET_KEY=your-secret-access-key
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_REGION=eu-central-1
```

Notes:

- **`HINATA_S3_REGION`** defaults to `us-east-1`; set it to your bucket's region for
  AWS and providers that care about it.
- For a non-AWS provider, `HINATA_S3_ENDPOINT` is its S3 endpoint URL (e.g. your R2
  or Backblaze endpoint). Use HTTPS for anything crossing the network.
- The credentials need permission to `PutObject`, `GetObject`, `DeleteObject`,
  `ListBucket`, and (unless you pre-create the bucket) `CreateBucket`.
- If storage is left unconfigured (blank access key), attachment and avatar
  endpoints respond with `error.storage.notConfigured` — the rest of Hinata still
  works, you just can't upload files.

!!! tip "Keep buckets private"
    Whichever provider you use, keep the bucket **private**. Hinata never needs
    public-read: it always hands out short-lived presigned URLs, so public access
    would only widen your attack surface.

See the [Configuration reference](/en/configuration.html) for the full variable
list, and [MongoDB & X.509](/en/database.html) for the database side of the stack.
