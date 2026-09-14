---
title: Object storage (S3, GCS, Azure)
description: Hinata keeps attachments and avatars in MinIO, any S3-compatible provider or Azure Blob Storage, with presigned downloads and randomized keys.
---

# Object storage (S3, GCS, Azure)

Attachments and avatars live in **object storage**, not in MongoDB. `HINATA_STORAGE_PROVIDER` selects one of two backends:

- **`s3`** (default): any S3-compatible store, such as the **bundled MinIO**, **AWS S3**, **Google Cloud Storage** (S3-interoperable XML API), **Cloudflare R2**, **DigitalOcean Spaces**, Backblaze B2, Wasabi, Ceph, a managed MinIO, …
- **`azure`**: **Azure Blob Storage** through its native API (Azure does not speak S3).

## MinIO in the default stack

The production `docker-compose.yml` runs MinIO next to the server. The container is attached to the compose **`local-storage` profile**, which is on by default (`COMPOSE_PROFILES=local-storage` in `.env.example`):

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

The server reaches MinIO over the internal Docker network and reuses the MinIO root credentials as its S3 keys:

```yaml
HINATA_S3_ENDPOINT: ${HINATA_S3_ENDPOINT:-http://minio:9000}
HINATA_S3_ACCESS_KEY: ${HINATA_S3_ACCESS_KEY:-${MINIO_ROOT_USER:-}}
HINATA_S3_SECRET_KEY: ${HINATA_S3_SECRET_KEY:-${MINIO_ROOT_PASSWORD:-}}
HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
```

You only set four values in `.env`:

```properties
COMPOSE_PROFILES=local-storage
MINIO_ROOT_USER=hinata
MINIO_ROOT_PASSWORD=change-me-to-a-long-random-value
HINATA_S3_BUCKET=hinata
```

The MinIO **web console** runs on port `9001` and the **S3 API** on `9000`. In local dev (`docker-compose.dev.yml`) both are published on loopback, at `http://localhost:9001` (console) and `http://localhost:9000` (API), with the dev keys `hinata` / `hinata-dev-secret`.

!!! warning "Change the MinIO password before production"
    `hinata-dev-secret` is a development default. Set a long random `MINIO_ROOT_PASSWORD` (e.g. from `./deploy/generate-secrets.sh`) for any real deployment. Never publish the MinIO ports to the internet, only the server needs to reach them.

## The bucket is created for you

On the first upload the server checks whether `HINATA_S3_BUCKET` exists and calls `makeBucket` if it doesn't. The bucket stays **private**, and nothing is ever made public-read. Every download goes through the server (see below), never straight from the bucket.

!!! tip
    You can also create the bucket yourself, for example to set a lifecycle rule or bucket policy in advance. Use the default name `hinata`, or set `HINATA_S3_BUCKET` to your name. The server reuses an existing bucket.

## Presigned downloads and randomized keys

- **Randomized object keys.** Each attachment is stored under a random UUID (optionally with a prefix like `media/` or `avatars/`), never under the user's file name. Keys can't be guessed, and the original file name never shows up in the bucket.
- **Short-lived presigned downloads.** When a client requests an attachment, the server returns a **presigned GET URL**. It is valid for **10 minutes** and sets `Content-Disposition: attachment`, so files download instead of rendering inline.

The S3 credentials stay on the server. Clients only see time-limited URLs, and the bucket never needs to be public.

## Live attachment events (SSE)

Attachment changes reach everyone viewing an issue in real time over **Server-Sent Events**:

```text
GET /api/v1/issues/{issueId}/attachments/stream
```

When someone uploads or removes files, even several at once, every open viewer sees the grid update without polling. The stream runs in-process per server instance. For a clustered deployment you would put a shared broker in front of it.

## Size and content-type limits

The defaults:

| Setting | Env / property | Default |
| --- | --- | --- |
| Max size of a single file | `HINATA_STORAGE_MAX_UPLOAD_MB` | `25` MB |
| Max files in one request | `hinata.storage.max-files-per-request` | `10` |
| Max total size of one request | `HINATA_STORAGE_MAX_REQUEST_MB` | `100` MB |

Only content types from an explicit allow list are accepted: PNG, JPEG, GIF, WebP, PDF, plain text, CSV, ZIP, JSON, and OOXML Word and Excel documents. Also:

- **`image/svg+xml` is excluded on purpose.** SVG can embed JavaScript (a stored XSS risk).
- **Magic byte verification.** For binary types the server checks the leading bytes against the declared content type, so a file can't pretend to be a PNG.
- A rejected upload returns a stable, localized error (`error.storage.fileTooLarge`, `error.storage.fileTypeNotAllowed`, `error.storage.contentMismatch`).

!!! note "Two size ceilings work together"
    Spring's multipart limits (`max-file-size` / `max-request-size`, driven by the same MB values) are the outer guard. The app also enforces the file count and total size. For larger uploads, raise all of them together.

## Using an external provider instead of MinIO

Clear the compose profile in `.env` to turn off the bundled MinIO:

```properties
COMPOSE_PROFILES=
```

Then configure one of the providers below. You can remove the `MINIO_ROOT_*` variables.

### AWS S3

```properties
HINATA_S3_ENDPOINT=https://s3.eu-central-1.amazonaws.com
HINATA_S3_ACCESS_KEY=AKIA...
HINATA_S3_SECRET_KEY=your-secret-access-key
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_REGION=eu-central-1
```

### Google Cloud Storage

GCS speaks S3 through its **interoperable XML API**. Create **HMAC keys** in the Cloud Console under *Cloud Storage → Settings → Interoperability* (for a service account, recommended) and point Hinata at the interop endpoint:

```properties
HINATA_S3_ENDPOINT=https://storage.googleapis.com
HINATA_S3_ACCESS_KEY=GOOG1E...          # HMAC access id
HINATA_S3_SECRET_KEY=your-hmac-secret
HINATA_S3_BUCKET=my-hinata-bucket
HINATA_S3_ADDRESSING_STYLE=path
```

### Azure Blob Storage

Azure has no S3 API, so Hinata talks to it natively. Switch the provider and pass the storage account's **connection string** (portal → storage account → *Access keys*). It must include the account key, because presigned downloads are issued as SAS URLs:

```properties
HINATA_STORAGE_PROVIDER=azure
HINATA_AZURE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
HINATA_S3_BUCKET=hinata   # used as the blob container name
```

### Other S3-compatible providers

Cloudflare R2, DigitalOcean Spaces, Backblaze B2, Wasabi, Ceph, Hetzner, a managed MinIO, … all work with the same `HINATA_S3_*` variables. Endpoint, keys and region come from the provider's dashboard.

Notes:

- **`HINATA_S3_REGION`** defaults to `us-east-1`. Set it to your bucket's region for AWS and providers that need it.
- **`HINATA_S3_ADDRESSING_STYLE`** (default `auto`) controls S3 URL addressing. `auto` picks virtual host style for AWS endpoints and path style everywhere else, which fits almost everyone. Set `path` or `virtual-host` if your provider requires it.
- Use HTTPS for any endpoint that crosses the network.
- The credentials need `PutObject`, `GetObject`, `DeleteObject`, `ListBucket` and `CreateBucket` (the last one only if you don't create the bucket yourself). On Azure the equivalent permissions apply, and the container is created automatically too.
- Without configuration (blank access key, or blank connection string with `provider=azure`), the attachment and avatar endpoints respond with `error.storage.notConfigured`. The rest of Hinata still works, only uploads don't.
- **Switching providers does not migrate existing objects.** If the instance already holds data, copy the bucket first (`mc mirror`, `aws s3 sync`, `azcopy`).

!!! tip "Keep buckets private"
    Whichever provider you use, keep the bucket **private**. Hinata always hands out short-lived presigned URLs and never needs public read access. That would only widen your attack surface.

See the [Configuration reference](/en/configuration.html) for every variable and [MongoDB & X.509](/en/database.html) for the database side.
