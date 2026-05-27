# Section 02: Custom Logo & Favicon Management

## Overview

Custom logo and favicon management allows tenants to upload their brand assets and have them displayed throughout the platform. The system handles image upload, validation, transformation (resizing, format conversion), CDN distribution, and cache invalidation. A custom logo appears in the dashboard header, login page, email templates, and any embedded widgets. The favicon appears in browser tabs and bookmarks.

The upload pipeline validates file type (SVG, PNG, WebP), dimensions (minimum 200x200 for logo, 48x48 for favicon), file size (max 5MB for logos, 500KB for favicons), and performs security scanning. Images are transformed to multiple formats and sizes for different use cases: SVG for vector/print quality, WebP for modern browsers, PNG fallback for email clients.

For a voice agent platform with white-label resellers, the logo system also supports "powered by" branding options, where the reseller's logo is shown alongside or instead of the platform's logo. This is a key white-label feature.

## Design Decisions

**Decision 1: SVG as preferred format for logos.** SVG is resolution-independent, smaller file size, and can be styled via CSS. For PNG uploads, auto-trace to SVG where possible, or offer both formats.

**Decision 2: CDN with versioned URLs.** Assets are stored in S3/CloudFront with content-hash-based file names. This enables aggressive caching and instant cache invalidation on re-upload.

**Decision 3: Automatic favicon generation.** From a single upload, generate favicon.ico (multi-size), apple-touch-icon, and Android manifest icons. This ensures consistency across devices.

## Implementation Approach

```typescript
class BrandAssetManager {
  async uploadLogo(tenantId: string, file: UploadedFile): Promise<AssetResult> {
    // Validate
    this.validateImage(file, { maxSize: 5 * 1024 * 1024, formats: ['svg', 'png', 'webp', 'jpg'] });

    // Security scan
    await this.securityScan(file);

    // Generate variants
    const variants = await this.generateLogoVariants(file);

    // Upload to CDN
    const uploaded = await Promise.all(
      variants.map(v => this.uploadToCdn(tenantId, v))
    );

    // Update tenant branding
    await this.db.query(`
      UPDATE tenant_branding 
      SET logo_url = $1, 
          logo_variants = $2, 
          updated_at = NOW() 
      WHERE tenant_id = $3
    `, [uploaded[0].url, JSON.stringify(uploaded), tenantId]);

    // Invalidate CDN cache
    await this.cdn.invalidate(`/tenant/${tenantId}/logo/*`);

    return { url: uploaded[0].url, variants: uploaded };
  }

  private async generateLogoVariants(file: UploadedFile): Promise<ImageVariant[]> {
    const variants: ImageVariant[] = [];
    
    const transforms = [
      { name: 'default', width: null, height: 40, format: 'auto' },
      { name: 'header', width: null, height: 32, format: 'webp' },
      { name: 'email', width: null, height: 80, format: 'png' },
      { name: 'og-image', width: 1200, height: 630, format: 'jpg', fit: 'contain' },
    ];

    for (const transform of transforms) {
      const transformed = await sharp(file.buffer)
        .resize(transform.width, transform.height, { fit: transform.fit || 'inside', withoutEnlargement: true })
        .toFormat(transform.format as any)
        .toBuffer();

      const hash = crypto.createHash('md5').update(transformed).digest('hex').slice(0, 8);
      const filename = `logo-${transform.name}-${hash}.${transform.format}`;
      
      variants.push({ filename, buffer: transformed, format: transform.format });
    }

    return variants;
  }

  async uploadFavicon(tenantId: string, file: UploadedFile): Promise<FaviconResult> {
    const variants = [
      { name: 'favicon.ico', sizes: [16, 32, 48] },
      { name: 'apple-touch-icon.png', size: 180 },
      { name: 'icon-192.png', size: 192 },
      { name: 'icon-512.png', size: 512 },
    ];

    const uploaded = await Promise.all(
      variants.map(v => this.generateAndUploadFavicon(tenantId, file, v))
    );

    await this.db.query(
      'UPDATE tenant_branding SET favicon_url = $1, updated_at = NOW() WHERE tenant_id = $2',
      [uploaded[0].url, tenantId]
    );

    return { urls: uploaded.map(u => u.url) };
  }

  private async generateAndUploadFavicon(
    tenantId: string, file: UploadedFile, variant: FaviconVariant
  ): Promise<{ url: string }> {
    const buffer = await sharp(file.buffer)
      .resize(variant.size || 32, variant.size || 32)
      .toFormat(variant.name.endsWith('.ico') ? 'png' as any : 'png')
      .toBuffer();

    // Convert to ICO if needed
    const finalBuffer = variant.name.endsWith('.ico') 
      ? await this.pngToIco(buffer, variant.sizes!)
      : buffer;

    return this.uploadToCdn(tenantId, {
      filename: variant.name,
      buffer: finalBuffer,
      format: variant.name.endsWith('.ico') ? 'ico' : 'png',
    });
  }

  private async securityScan(file: UploadedFile): Promise<void> {
    // Scan for malware (ClamAV)
    // Validate no SVG script tags (for SVG files)
    if (file.mimetype === 'image/svg+xml') {
      const content = file.buffer.toString('utf-8');
      if (content.includes('<script') || content.includes('onload=') || content.includes('onerror=')) {
        throw new Error('SVG contains unsafe content');
      }
    }
  }
}
```

## Open-Source Tools

- **Sharp** — High-performance image transformation for Node.js
- **Svgo** — SVG optimization and security sanitization
- **AWS S3 + CloudFront** — Object storage with CDN distribution
- **ImageOptim API** — Automated image optimization
- **Favicon Generator** — Multi-format favicon generation

## Production Considerations

- **CDN Cache Invalidation:** Logo changes may not be visible immediately due to CDN caching. Use versioned URLs with content hashes to avoid cache issues. Implement purge-on-publish for instant updates.
- **SVG Security:** SVG files can contain JavaScript, external resources, and XXE attacks. Always sanitize SVG uploads. Strip script tags, event handlers, and external references.
- **Image CDN:** Consider using an image CDN like Cloudinary or imgix that provides on-the-fly transformation. This enables URL-based resizing: `https://cdn.voiceagent.com/f_auto,q_80/w_200,h_40/tenant/abc/logo.svg`.
- **Storage Cost:** Logo files are small but each tenant has multiple variants. Estimate 500KB per tenant × thousands of tenants = manageable. Implement cleanup for deleted tenants.
- **CORS for Embedded Widgets:** If the logo is displayed on external sites (embedded agent), ensure the S3/CDN bucket has appropriate CORS headers configured.
