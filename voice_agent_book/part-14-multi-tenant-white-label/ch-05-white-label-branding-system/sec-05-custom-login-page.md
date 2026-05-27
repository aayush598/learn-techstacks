# Section 05: Custom Login Page & Auth UI

## Overview

The branded login page is the first interaction end users have with a white-label deployment. A custom login page displays the tenant's logo, brand colors, custom background, and tailored messaging (welcome text, privacy policy links, terms of service). The auth UI includes login, registration, password reset, multi-factor authentication enrollment, and SSO provider selection—all styled with tenant branding.

The login page is served from the tenant's custom domain and dynamically themed using the same CSS variable system as the rest of the application. The page supports multiple authentication methods based on tenant configuration: email/password, SSO/SAML (Part 16, Ch 07), magic link, and OAuth providers (Google, GitHub, Microsoft). Each method can be selectively enabled or disabled per tenant.

For enterprise deployments, the login page can also include custom background images/videos, custom CSS injections for advanced customization, and custom JavaScript for analytics or marketing tags. These advanced options are reserved for enterprise tier tenants.

## Implementation Approach

```typescript
class BrandedAuthPageService {
  async getLoginPageConfig(tenantId: string): Promise<LoginPageConfig> {
    const [branding, authConfig] = await Promise.all([
      this.getBranding(tenantId),
      this.getAuthConfig(tenantId),
    ]);

    return {
      logo: branding.logoUrl,
      favicon: branding.faviconUrl,
      colors: {
        primary: branding.primaryColor,
        background: branding.backgroundColor,
        surface: branding.surfaceColor,
        text: branding.textColor,
      },
      background: {
        type: branding.loginBackgroundType || 'solid',
        value: branding.loginBackgroundValue || branding.backgroundColor,
        overlay: branding.loginBackgroundOverlay,
      },
      messages: {
        welcomeText: branding.loginWelcomeText || 'Welcome back',
        buttonText: branding.loginButtonText || 'Sign in',
        helpText: branding.loginHelpText,
      },
      auth: {
        methods: authConfig.methods,
        saml: authConfig.saml,
        oidc: authConfig.oidc,
        mfa: authConfig.mfaRequired,
      },
      links: {
        privacyUrl: branding.privacyUrl,
        termsUrl: branding.termsUrl,
        supportUrl: branding.supportUrl,
      },
      customCss: branding.loginCustomCss,
      customHtml: branding.loginCustomHtml,
    };
  }

  renderLoginPage(config: LoginPageConfig): string {
    return `
      <!DOCTYPE html>
      <html data-theme="light">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>${config.messages.welcomeText} | ${config.companyName}</title>
        <link rel="icon" href="${config.favicon}">
        <style>
          :root {
            --brand-primary: ${config.colors.primary};
            --brand-background: ${config.colors.background};
            --brand-surface: ${config.colors.surface};
            --brand-text: ${config.colors.text};
          }
          /* ... base login styles ... */
          ${config.customCss || ''}
        </style>
      </head>
      <body>
        <div class="login-container"
          style="background: ${this.renderBackground(config.background)}">
          <div class="login-card" style="background: ${config.colors.surface}">
            <img src="${config.logo}" alt="${config.companyName}" class="logo"/>
            <h1 style="color: ${config.colors.text}">${config.messages.welcomeText}</h1>
            
            <form id="login-form">
              <input type="email" placeholder="Email" required/>
              <input type="password" placeholder="Password" required/>
              <button style="background: ${config.colors.primary}">
                ${config.messages.buttonText}
              </button>
            </form>

            <div class="auth-links">
              <a href="${config.links.privacyUrl}">Privacy Policy</a>
              <a href="${config.links.termsUrl}">Terms of Service</a>
            </div>
          </div>
        </div>
        ${config.customHtml || ''}
      </body>
      </html>
    `;
  }

  private renderBackground(bg: BackgroundConfig): string {
    if (bg.type === 'image') {
      return `url('${bg.value}') center/cover no-repeat`;
    }
    if (bg.type === 'gradient') {
      return `linear-gradient(${bg.value})`;
    }
    return bg.value;
  }
}
```

## Open-Source Tools

- **NextAuth.js / Auth.js** — Authentication library with customizable pages
- **Clerk / Auth0** — Auth providers with white-label login pages
- **Tailwind CSS** — Styling for login page components
- **Framer Motion** — Animated login page transitions
- **Lucide / Heroicons** — Icon library for auth UI

## Production Considerations

- **SEO for Login Pages:** Login pages should have `noindex` meta tags to prevent search indexing. Custom domain login pages for enterprises should be blocked from search engines.
- **Custom Domain Cookies:** Login cookies must be scoped to the tenant's custom domain. Ensure cookie domain configuration supports wildcard and custom domains.
- **Phishing Protection:** Branded login pages can increase phishing risk if tenants' domains are compromised. Educate tenants about security best practices. Offer WebAuthn/FIDO2 for phishing-resistant authentication.
- **Custom CSS Risks:** Allow custom CSS but strip any JavaScript. Custom HTML should be sandboxed and not execute scripts. Review customizations before activation for enterprise tenants.
- **Loading Performance:** The branded login page should load in under 2 seconds. Optimize background images, preload fonts, and lazy load non-critical assets.
