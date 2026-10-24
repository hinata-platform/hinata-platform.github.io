---
title: Object storage (S3, GCS, Azure)
description: Hinata keeps attachments and avatars in the bundled SeaweedFS, any S3-compatible provider or Azure Blob Storage, with presigned downloads and randomized keys.
---

# Object storage (S3, GCS, Azure)

Attachments and avatars live in **object storage**, not in MongoDB. `HINATA_STORAGE_PROVIDER` selects one of two backends:

- **`s3`** (default): any S3-compatible store, such as the **bundled SeaweedFS**, **AWS S3**, **Google Cloud Storage** (S3-interoperable XML API), **Cloudflare R2**, **DigitalOcean Spaces**, Backblaze B2, Wasabi, Ceph, a managed MinIO, …
- **`azure`**: **Azure Blob Storage** through its native API (Azure does not speak S3).

## SeaweedFS in the default stack

The production `docker-compose.yml` runs [SeaweedFS](https://github.com/seaweedfs/seaweedfs) (Apache-2.0, pinned to `4.48`) next to the server. Earlier versions bundled MinIO. MinIO no longer publishes community container images, so the stack moved to SeaweedFS. Hinata itself is not tied to either: it speaks plain S3, and every other S3 provider and Azure keep working (see [Using an external provider](#using-an-external-provider)). If you still run the bundled MinIO, see [Moving from MinIO to SeaweedFS](#moving-from-minio-to-seaweedfs).

Both storage services are attached to the compose **`local-storage` profile**, which is on by default (`COMPOSE_PROFILES=local-storage` in `.env.example`):

- **`seaweedfs`** runs the store. Its start script (`deploy/seaweedfs/entrypoint.sh`) refuses to start while any credential or key is missing.
- **`seaweedfs-setup`** runs once, creates the bucket, makes SSE-S3 encryption the bucket default and exits.

```yaml
seaweedfs:
  image: chrislusf/seaweedfs:4.48
  profiles: [local-storage]
  entrypoint: ["/bin/sh", "/opt/hinata/entrypoint.sh"]
  environment:
    HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
    HINATA_S3_ACCESS_KEY: ${HINATA_S3_ACCESS_KEY:-}
    HINATA_S3_SECRET_KEY: ${HINATA_S3_SECRET_KEY:-}
    SEAWEEDFS_ADMIN_ACCESS_KEY: ${SEAWEEDFS_ADMIN_ACCESS_KEY:-}
    SEAWEEDFS_ADMIN_SECRET_KEY: ${SEAWEEDFS_ADMIN_SECRET_KEY:-}
    WEED_S3_SSE_KEK: ${SEAWEEDFS_SSE_KEK:-}
    WEED_JWT_SIGNING_KEY: ${SEAWEEDFS_JWT_VOLUME_WRITE:-}
    WEED_JWT_SIGNING_READ_KEY: ${SEAWEEDFS_JWT_VOLUME_READ:-}
    WEED_JWT_FILER_SIGNING_KEY: ${SEAWEEDFS_JWT_FILER_WRITE:-}
    WEED_JWT_FILER_SIGNING_READ_KEY: ${SEAWEEDFS_JWT_FILER_READ:-}
  volumes:
    - seaweedfs-data:/data
    - ./deploy/seaweedfs:/opt/hinata:ro
```

What the bundled configuration does:

- **Credentials are required.** There are two identities: `hinata`, which the server uses and which may only touch its one bucket, and `admin`, which only the setup job uses.
- **Objects are encrypted at rest** with SSE-S3 under `SEAWEEDFS_SSE_KEK`. The key lives in the environment, never on the data volume.
- **Requests between the parts of SeaweedFS are signed** with the four `SEAWEEDFS_JWT_*` keys.
- **Nothing is published.** Only the server reaches the S3 port (`8333`), over the stack network. There is no web console.

The server talks to it with these defaults from the compose file:

```yaml
HINATA_S3_ENDPOINT: ${HINATA_S3_ENDPOINT:-http://seaweedfs:8333}
HINATA_S3_ACCESS_KEY: ${HINATA_S3_ACCESS_KEY:-}
HINATA_S3_SECRET_KEY: ${HINATA_S3_SECRET_KEY:-}
HINATA_S3_BUCKET: ${HINATA_S3_BUCKET:-hinata}
HINATA_S3_ADDRESSING_STYLE: ${HINATA_S3_ADDRESSING_STYLE:-path}
HINATA_S3_SSE: ${HINATA_S3_SSE:-}
```

In `.env` you set the keys. `./deploy/generate-secrets.sh` prints a fresh value for every secret:

```properties
COMPOSE_PROFILES=local-storage
HINATA_S3_ACCESS_KEY=hinata
HINATA_S3_SECRET_KEY=change-me
HINATA_S3_SSE=AES256
HINATA_S3_BUCKET=hinata
SEAWEEDFS_ADMIN_ACCESS_KEY=hinata-admin
SEAWEEDFS_ADMIN_SECRET_KEY=change-me
SEAWEEDFS_SSE_KEK=change-me-64-hex-chars
SEAWEEDFS_JWT_VOLUME_WRITE=change-me
SEAWEEDFS_JWT_VOLUME_READ=change-me
SEAWEEDFS_JWT_FILER_WRITE=change-me
SEAWEEDFS_JWT_FILER_READ=change-me
```

!!! danger "Keep a copy of `SEAWEEDFS_SSE_KEK` apart from the server"
    Every stored object is encrypted under this key. Without it none of them can be read again, and a copy of the data volume alone does not help. Keep it with your other secrets, in a different place from the data (see [Backups & upgrades](/en/backups.html)). Do not replace it on an install that already holds files: what is stored stays encrypted under the old key.

!!! warning "Leave `-s3.encryptVolumeData` off"
    SeaweedFS has a second encryption switch, `-s3.encryptVolumeData`. In version 4.48 it does not work together with SSE-S3: a copy of an SSE-S3 object becomes unreadable ([seaweedfs/seaweedfs#11646](https://github.com/seaweedfs/seaweedfs/issues/11646)), and the bucket's default encryption is skipped ([seaweedfs/seaweedfs#11647](https://github.com/seaweedfs/seaweedfs/issues/11647)). Hinata does copy objects, for example when you clone an issue with attachments. That is why the bundled configuration leaves the switch off and relies on SSE-S3.

In local dev (`docker-compose.dev.yml`) the same SeaweedFS runs with fixed dev keys and publishes only its S3 API on loopback, at `http://localhost:8333`. It needs the profile too, and the setup job once:

```bash
COMPOSE_PROFILES=local-storage docker compose -f docker-compose.dev.yml up -d
COMPOSE_PROFILES=local-storage docker compose -f docker-compose.dev.yml run --rm seaweedfs-setup
```

The dev keys are `hinata` / `hinata-dev-secret-0123456789abcdef`. They are for your machine only. See [Development](/en/development.html).

## The bucket is created for you

On the first upload the server checks whether `HINATA_S3_BUCKET` exists and calls `makeBucket` if it doesn't. With the bundled SeaweedFS the `seaweedfs-setup` job has already created it. The bucket stays **private**, and nothing is ever made public-read. Every download goes through the server (see below), never straight from the bucket.

!!! tip
    You can also create the bucket yourself, for example to set a lifecycle rule or bucket policy in advance. Use the default name `hinata`, or set `HINATA_S3_BUCKET` to your name. The server reuses an existing bucket.

## Server-side encryption

`HINATA_S3_SSE=AES256` makes the server ask for SSE-S3 on every object it writes. It asks again when it copies one, because a copy is a new object. Leave the variable empty for a store that encrypts on its own or does not know the header. Any other value stops the server at startup, so a typo cannot leave files unencrypted.

With the bundled SeaweedFS, set it to `AES256`. The bucket default from the setup job also covers objects written without the header, so no file depends on only one of the two.

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

Every byte someone uploads passes the same check before it is stored: attachments, images in texts, voice messages, avatars, the logo and the attachments of incoming e-mail. What the check refuses is not stored.

- **The content decides, not the declared type.** The server reads the first bytes and compares them with the declared content type. A program that calls itself a PDF is refused. For e-mail attachments only the content counts.
- **A fixed list per kind.** Attachments may be PNG, JPEG, GIF, WebP, PDF, plain text, CSV, ZIP, JSON, and OOXML Word and Excel documents. Images in texts are PNG, JPEG, GIF or WebP, voice messages M4A, AAC, MP3, WebM, Ogg or WAV, avatars and the logo PNG, JPEG, GIF or BMP.
- **`image/svg+xml` is excluded on purpose.** SVG can embed JavaScript (a stored XSS risk).
- **Size per kind.** Attachments and images in texts up to `HINATA_STORAGE_MAX_UPLOAD_MB`, voice messages up to 16 MB, avatars up to 12 MB and the logo up to 8 MB. The server reads how many pixels an image has from its header before it opens it, so a small file cannot pass itself off as a huge picture.
- **File names** are at most 200 characters long and contain no control characters and no `/` or `\`.
- A refused upload answers `422` with a localized sentence. Its `details` carry `code: upload.refused` and the reason: `type`, `signature`, `size`, `image`, `metadata`, `fileName`, `empty`, `disabled` or `unreadable`. Every refusal counts into the yearly figures of moderation.

Under **Admin area › Moderation › File types** you switch off whole groups: images, PDF, Office documents, text and spreadsheets, ZIP and voice messages. That only narrows the list. It cannot be widened, so nobody can allow SVG or programs. Avatars and the logo are not affected.

The server does not check what an image shows. A person reviews reported images.

### Metadata of images

An image someone puts into a description, a comment or an article is seen by everybody who reads the text. A phone photo often carries the place it was taken in its EXIF data. So the server removes EXIF, XMP and IPTC from embedded images before storing them, GPS position included, along with comments and text blocks. It only cuts these blocks out and does not encode the image again, so quality and animation (GIF, WebP) stay. Only a JPEG whose EXIF says it is shown turned gets turned by the server itself and stored anew, so that it stands the right way up without the EXIF. An image whose blocks cannot be read safely is refused.

**Attachments stay as they were uploaded.** Whoever attaches a photo as a file on purpose gets it back with all its metadata. Avatars, the logo and previews are encoded anew by the server anyway and carry no metadata.

### Images from other sources

When a text is saved, the server goes through every image in it:

- **External images** (`http`, `https`) become a link with the text "External image". If the app showed them, merely opening the text would give the address of every reader to the foreign server, and nobody would have checked the bytes. This mostly affects e-mails with embedded logos.
- **`data:` images** pass the same check as an upload and end up in the media store, at most 20 per save. Where the check refuses one, "Image not included" takes its place.
- Images of this server stay as they are. Any other source becomes "Image not included" as well.

!!! note "Two size ceilings work together"
    Spring's multipart limits (`max-file-size` / `max-request-size`, driven by the same MB values) are the outer guard. The app also enforces the file count and total size. For larger uploads, raise all of them together.

## Quarantine of removed content

When moderation removes a file or an image, the server copies it inside the store to `quarantine/<case>/` and deletes the original only afterwards. A picture that other texts still show stays in its place. Removed texts and the versions of a removed page go into the database. The quarantine is what moderators see in the case and what a successful appeal puts back. Nobody else can reach it. When the retention of the case ends, the server deletes the quarantine with it, unless law enforcement was told. See [Moderation](/en/moderation.html#retention).

The copy happens inside the store and never passes through the server. Every provider below can do that. With SeaweedFS keep `-s3.encryptVolumeData` off, as described above.

## Using an external provider

Clear the compose profile in `.env` to turn off the bundled SeaweedFS:

```properties
COMPOSE_PROFILES=
```

Then configure one of the providers below. You no longer need the `SEAWEEDFS_*` variables. The compose file sets `HINATA_S3_ADDRESSING_STYLE` to `path` for the bundled store, so set it to `auto` for an external one unless your provider asks for something else.

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
- **`HINATA_S3_ADDRESSING_STYLE`** controls S3 URL addressing. The server's own default is `auto`, the compose file sets `path`. `auto` picks virtual host style for AWS endpoints and path style everywhere else, which fits almost everyone. Set `path` or `virtual-host` if your provider requires it.
- Use HTTPS for any endpoint that crosses the network.
- The credentials need `PutObject`, `GetObject`, `DeleteObject`, `ListBucket` and `CreateBucket` (the last one only if you don't create the bucket yourself). On Azure the equivalent permissions apply, and the container is created automatically too.
- Without configuration (blank access key, or blank connection string with `provider=azure`), the attachment and avatar endpoints respond with `error.storage.notConfigured`. The rest of Hinata still works, only uploads don't.
- **Switching providers does not migrate existing objects.** If the instance already holds data, copy the bucket first (`rclone sync`, `aws s3 sync`, `azcopy`). Object keys stay the same, so nothing in the database changes.

!!! tip "Keep buckets private"
    Whichever provider you use, keep the bucket **private**. Hinata always hands out short-lived presigned URLs and never needs public read access. That would only widen your attack surface.

## Moving from MinIO to SeaweedFS

An install that still runs the bundled MinIO moves its files over once. The idea: start SeaweedFS beside MinIO, copy every object with [rclone](https://rclone.org), compare, point the server at SeaweedFS, and retire MinIO only after you have checked the result. MinIO stays untouched until the very end, so you can always go back.

1. **Back up first.** Take a database dump and a copy of the bucket as described in [Backups & upgrades](/en/backups.html).
2. **Keep MinIO running.** The new `docker-compose.yml` no longer has a `minio` service. Move your existing definition into `docker-compose.override.yml` so Compose keeps managing it, with the same volume, so the data stays where it is:

    ```yaml
    services:
      minio:
        image: minio/minio:<the tag you run today>
        command: server /data
        environment:
          MINIO_ROOT_USER: ${MINIO_ROOT_USER}
          MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
        volumes:
          - minio-data:/data
        networks: [hinata]
    volumes:
      minio-data:
    ```

3. **Add the SeaweedFS secrets** to `.env`: run `./deploy/generate-secrets.sh`, copy the `SEAWEEDFS_*` values and a new `HINATA_S3_SECRET_KEY`, set `HINATA_S3_ACCESS_KEY=hinata` and `HINATA_S3_SSE=AES256`, and keep a copy of `SEAWEEDFS_SSE_KEK` somewhere else. Keep `MINIO_ROOT_*` for now. Do not recreate `hinata-server` yet. It keeps reading MinIO with the settings it was started with.
4. **Start SeaweedFS** and run the setup job:

    ```bash
    docker compose up -d seaweedfs
    docker compose run --rm seaweedfs-setup
    ```

5. **Copy every object**, encrypted on the way in. rclone runs on the stack network (`hinata_hinata` with the default project name) and is configured only through environment variables, so no key ends up in a file or in your shell history:

    ```bash
    set -a; . ./.env; set +a
    rclone() {
      docker run --rm --network hinata_hinata \
        -e RCLONE_CONFIG_SRC_TYPE=s3 -e RCLONE_CONFIG_SRC_PROVIDER=Minio \
        -e RCLONE_CONFIG_SRC_ENDPOINT=http://minio:9000 \
        -e RCLONE_CONFIG_SRC_ACCESS_KEY_ID="$MINIO_ROOT_USER" \
        -e RCLONE_CONFIG_SRC_SECRET_ACCESS_KEY="$MINIO_ROOT_PASSWORD" \
        -e RCLONE_CONFIG_DST_TYPE=s3 -e RCLONE_CONFIG_DST_PROVIDER=SeaweedFS \
        -e RCLONE_CONFIG_DST_ENDPOINT=http://seaweedfs:8333 \
        -e RCLONE_CONFIG_DST_ACCESS_KEY_ID="$HINATA_S3_ACCESS_KEY" \
        -e RCLONE_CONFIG_DST_SECRET_ACCESS_KEY="$HINATA_S3_SECRET_KEY" \
        -e RCLONE_CONFIG_DST_SERVER_SIDE_ENCRYPTION=AES256 \
        rclone/rclone:1.71 "$@"
    }
    rclone sync src:hinata dst:hinata --checksum --transfers 8
    ```

    You can repeat this as often as you like. Only what changed is copied again.

6. **Compare.** Object counts must be equal, and the check must report no differences:

    ```bash
    rclone size src:hinata
    rclone size dst:hinata
    rclone check src:hinata dst:hinata --one-way --size-only
    ```

7. **Switch.** Run the `sync` once more right before, so uploads from the meantime come along. Then recreate only the server. With nothing overriding `HINATA_S3_ENDPOINT` in `.env`, the compose defaults point it at `http://seaweedfs:8333` with path addressing:

    ```bash
    docker compose up -d --no-deps --force-recreate hinata-server
    ```

    Open a few attachments and avatars in the app. If something is wrong, point the server back at MinIO (`HINATA_S3_ENDPOINT=http://minio:9000` and the old keys) and recreate it the same way. MinIO still holds everything.

8. **Retire MinIO** once you are satisfied: stop and remove its container with `docker compose rm -sf minio`, then delete the `minio` service and volume from `docker-compose.override.yml` and the `MINIO_ROOT_*` lines from `.env`. The volume itself stays until you delete it on purpose (`docker volume rm hinata_minio-data`). Do that only when the server has run on SeaweedFS for a while and a backup of the new bucket exists.

Object keys stay the same, so nothing in the database changes.

See the [Configuration reference](/en/configuration.html) for every variable and [MongoDB & X.509](/en/database.html) for the database side.
