# Section 05: User Avatar & Profile Pictures

User avatars personalize the user experience and help identify users in team settings. Avatars are uploaded by users, generated from initials (fallback), or synced from SSO/OAuth providers. The avatar system stores multiple resolutions for different display contexts.

Avatar sources: user upload (drag-and-drop or file picker), initials avatar (generated from first/last name with random background color), Gravatar (fallback if email has Gravatar), and OAuth provider (Google/Microsoft profile picture). Priority: upload > OAuth > initials > Gravatar.

Image processing: uploaded image is resized to multiple sizes (32×32, 64×64, 128×128, 256×256) using Sharp. Original stored for re-processing. Format: WebP (primary, best compression), PNG (fallback for transparency). CDN caching: avatars cached at CDN edge with 1-hour TTL. Cache busting: ?v=timestamp URL parameter on avatar change. Default avatar: initials on colored circle (deterministic color from user ID hash).
