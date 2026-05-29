# Section 05: MinIO Storage Setup

## Overview

MinIO provides S3-compatible object storage for the voice agent platform, handling call recordings, transcripts, exports, and other binary assets during development. Its S3 API compatibility means the same code works against AWS S3, Google Cloud Storage, or any S3-compatible provider in production.

## Container Configuration

```yaml
# docker/docker-compose.yml (MinIO service)
services:
  minio:
    image: minio/minio:latest
    container_name: voice-agent-minio
    restart: unless-stopped
    ports:
      - "9000:9000"   # S3 API
      - "9001:9001"   # Console UI
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
      MINIO_REGION: us-east-1
      MINIO_BROWSER: on
      MINIO_PROMETHEUS_AUTH_TYPE: public
    volumes:
      - minio-data:/data
    command: server /data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - voice-agent-dev
```

## Bucket Initialization

```yaml
# docker/docker-compose.yml (MinIO init service)
services:
  minio-init:
    image: minio/mc:latest
    container_name: voice-agent-minio-init
    restart: "no"
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: ["/bin/sh", "-c"]
    command: |
      echo "Configuring MinIO..." && \
      mc alias set local http://minio:9000 minioadmin minioadmin && \

      # Create buckets
      mc mb local/voice-agent-recordings --ignore-existing && \
      mc mb local/voice-agent-transcripts --ignore-existing && \
      mc mb local/voice-agent-exports --ignore-existing && \
      mc mb local/voice-agent-temp --ignore-existing && \

      # Set bucket policies
      mc anonymous set download local/voice-agent-recordings && \
      mc anonymous set download local/voice-agent-transcripts && \

      # Set lifecycle policy for recordings (auto-delete after 90 days)
      mc ilm import local/voice-agent-recordings <<EOF
      {
        "Rules": [
          {
            "ID": "expire-old-recordings",
            "Status": "Enabled",
            "Expiration": {
              "Days": 90
            }
          }
        ]
      }
      EOF
      echo "MinIO configured successfully"
    networks:
      - voice-agent-dev
```

## Bucket Structure

```text
voice-agent-recordings/
├── {organization_id}/
│   ├── {call_id}.wav          # Full call recording
│   ├── {call_id}_agent.wav    # Agent-side audio
│   └── {call_id}_customer.wav # Customer-side audio

voice-agent-transcripts/
├── {organization_id}/
│   ├── {call_id}.json         # Full transcript
│   ├── {call_id}_diarized.json # Speaker-diarized version
│   └── {call_id}_summary.md   # AI-generated summary

voice-agent-exports/
├── {organization_id}/
│   ├── {export_id}.csv        # Data export
│   └── {export_id}.zip        # Bulk export archive

voice-agent-temp/
├── {uuid}/
│   ├── upload.tmp             # In-progress uploads
│   └── processed.wav          # Transient processing files
```

## S3 Client Implementation

```typescript
// packages/voice/src/storage/s3-client.ts
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
  DeleteObjectCommand,
  ListObjectsV2Command,
  type PutObjectCommandInput,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const globalForS3 = globalThis as unknown as {
  s3: S3Client | undefined;
};

function createS3Client(): S3Client {
  const endpoint = process.env.MINIO_ENDPOINT ?? "localhost";
  const port = process.env.MINIO_PORT ?? "9000";
  const useSSL = process.env.MINIO_USE_SSL === "true";

  return new S3Client({
    endpoint: `http${useSSL ? "s" : ""}://${endpoint}:${port}`,
    region: process.env.MINIO_REGION ?? "us-east-1",
    credentials: {
      accessKeyId: process.env.MINIO_ACCESS_KEY ?? "minioadmin",
      secretAccessKey: process.env.MINIO_SECRET_KEY ?? "minioadmin",
    },
    forcePathStyle: true, // Required for MinIO
    requestHandler: {
      requestTimeout: 30000,
    },
  });
}

export function getS3Client(): S3Client {
  if (!globalForS3.s3) {
    globalForS3.s3 = createS3Client();
  }
  return globalForS3.s3;
}

// Bucket names
export const BUCKETS = {
  RECORDINGS: process.env.MINIO_BUCKET_RECORDINGS ?? "voice-agent-recordings",
  TRANSCRIPTS: process.env.MINIO_BUCKET_TRANSCRIPTS ?? "voice-agent-transcripts",
  EXPORTS: "voice-agent-exports",
  TEMP: "voice-agent-temp",
} as const;
```

## Storage Operations

```typescript
// packages/voice/src/storage/storage-service.ts
import { getS3Client, BUCKETS } from "./s3-client";
import {
  PutObjectCommand,
  GetObjectCommand,
  DeleteObjectCommand,
  ListObjectsV2Command,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

export class StorageService {
  private s3 = getS3Client();

  async uploadRecording(
    organizationId: string,
    callId: string,
    audioBuffer: Buffer,
    contentType: string = "audio/wav",
  ): Promise<string> {
    const key = `${organizationId}/${callId}.wav`;

    await this.s3.send(
      new PutObjectCommand({
        Bucket: BUCKETS.RECORDINGS,
        Key: key,
        Body: audioBuffer,
        ContentType: contentType,
        Metadata: {
          "call-id": callId,
          "organization-id": organizationId,
          "uploaded-at": new Date().toISOString(),
        },
      }),
    );

    return key;
  }

  async getRecordingStream(
    organizationId: string,
    callId: string,
  ): Promise<ReadableStream> {
    const key = `${organizationId}/${callId}.wav`;

    const response = await this.s3.send(
      new GetObjectCommand({
        Bucket: BUCKETS.RECORDINGS,
        Key: key,
      }),
    );

    return response.Body as ReadableStream;
  }

  async getSignedDownloadUrl(
    organizationId: string,
    callId: string,
    expiresIn: number = 3600,
  ): Promise<string> {
    const key = `${organizationId}/${callId}.wav`;

    return getSignedUrl(
      this.s3,
      new GetObjectCommand({
        Bucket: BUCKETS.RECORDINGS,
        Key: key,
      }),
      { expiresIn },
    );
  }

  async uploadTranscript(
    organizationId: string,
    callId: string,
    transcript: Transcript,
  ): Promise<string> {
    const key = `${organizationId}/${callId}.json`;

    await this.s3.send(
      new PutObjectCommand({
        Bucket: BUCKETS.TRANSCRIPTS,
        Key: key,
        Body: JSON.stringify(transcript),
        ContentType: "application/json",
      }),
    );

    return key;
  }

  async deleteRecording(
    organizationId: string,
    callId: string,
  ): Promise<void> {
    const key = `${organizationId}/${callId}.wav`;

    await this.s3.send(
      new DeleteObjectCommand({
        Bucket: BUCKETS.RECORDINGS,
        Key: key,
      }),
    );
  }

  async listRecordings(
    organizationId: string,
    prefix?: string,
  ): Promise<string[]> {
    const response = await this.s3.send(
      new ListObjectsV2Command({
        Bucket: BUCKETS.RECORDINGS,
        Prefix: prefix ?? `${organizationId}/`,
      }),
    );

    return (response.Contents ?? []).map((obj) => obj.Key!);
  }
}
```

## File Upload Endpoint

```typescript
// apps/api/src/app/api/recordings/upload/route.ts
import { NextRequest, NextResponse } from "next/server";
import { StorageService } from "@voice-agent/voice/storage";

const storage = new StorageService();

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const audioFile = formData.get("audio") as Blob;
  const callId = formData.get("callId") as string;
  const organizationId = request.headers.get("x-organization-id")!;

  if (!audioFile || !callId) {
    return NextResponse.json(
      { error: "Missing audio file or call ID" },
      { status: 400 },
    );
  }

  const buffer = Buffer.from(await audioFile.arrayBuffer());
  const key = await storage.uploadRecording(
    organizationId,
    callId,
    buffer,
    audioFile.type,
  );

  return NextResponse.json({ key, url: await storage.getSignedDownloadUrl(organizationId, callId) });
}
```

## Lifecycle Policies

```json
// MinIO lifecycle configuration for auto-cleanup
{
  "Rules": [
    {
      "ID": "expire-old-recordings",
      "Status": "Enabled",
      "Filter": {},
      "Expiration": {
        "Days": 90
      }
    },
    {
      "ID": "expire-temp-files",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "temp/"
      },
      "Expiration": {
        "Days": 1
      }
    }
  ]
}
```

## Design Decisions

### MinIO vs. local filesystem

**Decision**: Always use MinIO/S3 API, even for local storage.

**Rationale**: Using the S3 API abstracts storage from the beginning. The same `StorageService` class works against MinIO (dev), AWS S3 (production), or any S3-compatible provider. Testing against the real API surface catches integration issues that local filesystem storage wouldn't.

### forcePathStyle: true

MinIO requires path-style URLs (`http://minio:9000/bucket/key`) rather than virtual-hosted-style URLs (`http://bucket.minio:9000/key`). The `forcePathStyle: true` option in the SDK ensures path-style URLs are used.

### Presigned URLs

Presigned URLs allow secure, time-limited access to private objects without exposing credentials. The recording player in the web app uses presigned URLs to stream recordings directly from storage without proxying through the API.

## Integration Points

- **@aws-sdk/client-s3**: AWS SDK for S3 API calls
- **@aws-sdk/s3-request-presigner**: Generate presigned URLs
- **Call recording pipeline**: Uploads WAV files after call completion
- **Transcription pipeline**: Uploads JSON transcripts
- **Export service**: Generates CSV/zip exports

## Production Considerations

1. **TLS/SSL**: MinIO in development uses plain HTTP. Production (AWS S3) enforces HTTPS. The SDK handles this transparently
2. **Bucket policies**: Production buckets should be private. Access is via presigned URLs or IAM roles
3. **Multi-region**: For disaster recovery, replicate recordings across regions. AWS S3 supports cross-region replication
4. **Glacier transition**: Older recordings (>90 days) should transition to Glacier for cost savings. S3 lifecycle policies automate this
5. **Upload optimization**: For large recordings (>100MB), use multipart upload or presigned POST URLs for direct browser-to-S3 uploads
