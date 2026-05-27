# Section 04: White-Label Reseller Experience

The white-label reseller experience presents the platform as the reseller's own product, with no VoiceAgent branding visible to end customers. The reseller's sub-accounts see the reseller's logo, brand colors, and domain throughout their experience. This is the core value proposition for resellers and agency partners.

Full white-labeling covers: custom domain (reseller's domain), branded dashboard (CSS variables for theming), branded login page, branded email templates, custom app icons, removed "Powered by VoiceAgent" branding, and custom documentation/help center. The reseller also gets a branded admin panel where they manage their sub-accounts.

The white-label configuration is inherited by sub-accounts by default, but sub-resellers or large end customers within the hierarchy can have their own branding overlays. The inheritance cascade is: platform defaults → reseller branding → sub-reseller branding → tenant branding. Each level can override specific elements or inherit from parent.

For a voice agent platform, the white-label experience extends to embedded widgets, API responses (custom headers), and the mobile app. The goal is complete brand invisibility for the platform operator.
