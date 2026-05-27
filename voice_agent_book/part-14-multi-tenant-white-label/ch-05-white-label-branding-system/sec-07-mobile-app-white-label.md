# Section 07: White-Label Mobile App Support

## Overview

White-label mobile apps allow resellers and enterprise tenants to distribute branded versions of the voice agent mobile app through app stores. Each white-label app has custom app icons, splash screens, color schemes, and app store listings (name, description, screenshots), while sharing the core application codebase. This enables resellers to offer a "custom" app experience without maintaining separate codebases.

The white-label mobile strategy uses a combination of build-time configuration (app icon, bundle ID, app name) and runtime theming (colors, fonts, feature flags). Each tenant's app is built from the same codebase but configured with their brand assets and settings during the build pipeline. App store distribution requires separate app store entries per white-label app, managed through the reseller's or tenant's own developer accounts.

For a voice agent platform, the mobile app includes agent configuration, call monitoring, real-time transcription, and analytics viewing—all themed per tenant. Push notification configuration, deep linking, and universal links must also be tenant-aware.

## Design Decisions

**Decision 1: Runtime theming from API.** The app fetches theme configuration from the API on startup. This allows branding changes without app store updates. Only build-time assets (app icon, splash screen) require new builds.

**Decision 2: Fastlane for build automation.** Fastlane automates the white-label build pipeline: downloading tenant assets, configuring Xcode/Android project files, building, code signing, and deploying to app stores.

**Decision 3: Separate app store entries per tenant.** Each white-label app is a separate app store listing with its own bundle ID and developer account. This requires managing multiple Apple Developer and Google Play Console accounts.

## Implementation Approach

```typescript
class WhiteLabelMobileBuild {
  async generateBuildConfig(tenantId: string, platform: 'ios' | 'android'): Promise<BuildConfig> {
    const branding = await this.getBranding(tenantId);
    
    return {
      appName: branding.mobileAppName || 'Voice Agent',
      bundleId: `com.${branding.bundlePrefix || 'voiceagent'}.${tenantId.slice(0, 8)}`,
      version: '1.0.0',
      build: 1,
      icon: await this.downloadAsset(branding.mobileAppIconUrl),
      splashScreen: await this.downloadAsset(branding.mobileSplashUrl),
      colors: {
        primary: branding.primaryColor,
        background: branding.backgroundColor,
      },
      deepLinkScheme: `voiceagent-${tenantId.slice(0, 8)}`,
      apiUrl: branding.apiUrl || 'https://api.voiceagent.com',
      webSocketUrl: branding.wsUrl || 'wss://api.voiceagent.com',
      featureFlags: branding.mobileFeatureFlags || {},
    };
  }

  async triggerBuild(tenantId: string, platform: 'ios' | 'android'): Promise<BuildJob> {
    const config = await this.generateBuildConfig(tenantId, platform);
    
    // Upload config to build server
    await this.s3.putObject({
      Bucket: 'mobile-builds',
      Key: `configs/${tenantId}/${platform}.json`,
      Body: JSON.stringify(config),
    });

    // Trigger CI build
    const build = await this.circleCI.triggerPipeline({
      branch: 'main',
      parameters: {
        tenant_id: tenantId,
        platform,
        config_url: `s3://mobile-builds/configs/${tenantId}/${platform}.json`,
      },
    });

    return { buildId: build.id, status: 'queued' };
  }
}

// Fastlane configuration (generated per tenant)
const fastlaneConfig = `
lane :deploy_white_label do |options|
  tenant_id = options[:tenant_id]
  config = JSON.parse(File.read("configs/#{tenant_id}/ios.json"))
  
  # Configure Xcode project
  update_app_identifier(
    xcodeproj: "VoiceAgent.xcodeproj",
    plist_path: "VoiceAgent/Info.plist",
    app_identifier: config["bundle_id"]
  )
  
  # Set app icon
  produce(
    username: config["apple_username"],
    app_identifier: config["bundle_id"],
    app_name: config["app_name"],
    language: "en_US",
    sku: config["bundle_id"],
    team_name: config["team_name"]
  )
  
  # Build and upload
  build_app(scheme: "VoiceAgent", export_method: "app-store")
  upload_to_app_store(skip_metadata: true, skip_screenshots: true)
end
`;
```

## Open-Source Tools

- **Fastlane** — Mobile app build automation
- **React Native / Flutter** — Cross-platform framework for white-label apps
- **CodePush / EAS Update** — Over-the-air updates for JavaScript-based apps
- **XcodeGen / Tuist** — Xcode project generation for white-label builds
- **Codemagic / Bitrise** — CI/CD for mobile app builds

## Production Considerations

- **App Store Review:** Each white-label app goes through separate app store review. Maintain good relationships with Apple and Google. Ensure apps comply with app store guidelines.
- **Push Notification Certificates:** Each bundle ID needs its own push notification certificate/key. Automate certificate generation and renewal.
- **Deep Linking:** Each white-label app needs registered URL schemes and universal links. These must be configured per tenant domain.
- **Update Frequency:** White-label apps require app store updates for native code changes. For branding changes, use runtime theming. For feature changes, use feature flags.
- **Cost:** Apple Developer account ($99/year per account) × number of white-label apps. Bundle IDs are unlimited. Consider enterprise developer program for managing multiple apps.
- **Crash Reporting:** Each white-label app sends crash reports separately. Aggregate in a shared dashboard with tenant filtering.
