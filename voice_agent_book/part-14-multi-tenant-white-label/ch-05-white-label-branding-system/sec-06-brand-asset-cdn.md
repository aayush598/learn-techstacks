# Section 06: Brand Asset CDN Strategy

## Overview

Brand assets (logos, favicons, background images, fonts) must be delivered with high availability, low latency, and global reach. A CDN-based asset delivery strategy ensures that tenant branding loads quickly regardless of the end user's location. The asset pipeline handles upload, transformation, storage, CDN distribution, cache management, and versioning.

The CDN strategy uses a combination of origin storage (S3) and edge caching (CloudFront/CDN). Assets are uploaded to S3 with content-hash-based filenames for cache busting. The CDN caches assets at edge locations worldwide, with cache-control headers set for long-lived cache (1 year) due to the immutable filename pattern. Cache invalidation is handled by uploading new versions with new filenames.

For a voice agent platform with potentially thousands of tenants, the CDN must handle a high volume of small asset requests efficiently. Asset optimization (minification, compression, format conversion) is performed at upload time. Image CDNs like Cloudinary or imgix can provide on-the-fly transformation for responsive images.

## Implementation Approach

```typescript
class BrandAssetCDN {
  private s3: S3Client;
  private cloudfront: CloudFrontClient;

  async uploadAsset(tenantId: string, file: Buffer, path: string): Promise<string> {
    const hash = crypto.createHash('md5').update(file).digest('hex').slice(0, 8);
    const extension = path.split('.').pop();
    const filename = `${path.replace(`.${extension}`, '')}-${hash}.${extension}`;
    const key = `tenants/${tenantId}/brand/${filename}`;

    await this.s3.putObject({
      Bucket: process.env.ASSETS_BUCKET,
      Key: key,
      Body: file,
      ContentType: this.getMimeType(extension!),
      CacheControl: 'public, max-age=31536000, immutable',
    });

    return `${this.cdnUrl}/${key}`;
  }

  async purgeTenantAssets(tenantId: string): Promise<void> {
    await this.cloudfront.createInvalidation({
      DistributionId: process.env.CDN_DISTRIBUTION_ID,
      InvalidationBatch: {
        Paths: {
          Quantity: 1,
          Items: [`/tenants/${tenantId}/brand/*`],
        },
        CallerReference: `purge-${tenantId}-${Date.now()}`,
      },
    });
  }

  getOptimizedUrl(originalUrl: string, options: ImageOptions): string {
    // If using image CDN like Cloudinary
    const params = new URLSearchParams({
      w: options.width?.toString() || '',
      h: options.height?.toString() || '',
      f: options.format || 'auto',
      q: options.quality?.toString() || '80',
    });

    return `${this.imageCdnUrl}/${encodeURIComponent(originalUrl)}?${params}`;
  }
}
```

## Open-Source Tools

- **AWS S3** — Durable object storage for brand assets
- **CloudFront / Fastly** — Global CDN with edge caching
- **Sharp** — Image transformation pipeline
- **Cloudinary / imgix** — Image CDN with on-the-fly transformations
- **Broccoli / Vite** — Asset build pipeline for optimization

## Production Considerations

- **Cache Invalidation:** Even with versioned URLs, you may need to force-purge outdated assets. CDN invalidation costs money (per path). Use sparingly or use versioned URLs exclusively.
- **Global Edge Caching:** Configure CDN to cache assets at all edge locations with long TTL. Asset requests should be served from edge with <20ms latency globally.
- **Asset Security:** Scan all uploaded assets for malware. Restrict file types to images only. Set bucket policies to prevent public listing.
- **Cost Optimization:** CDN data transfer costs money. Optimize asset sizes (compress PNGs, use WebP, minify SVGs). Monitor CDN costs per tenant for chargeback.
- **Reseller-Specific Assets:** For white-label resellers, ensure assets are isolated by sub-tenant. A reseller's logo should not be mixed with their sub-tenants' logos.
