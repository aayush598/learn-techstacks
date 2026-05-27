# Section 03: Color Palette & Typography System

## Overview

The color palette and typography system gives tenants control over their visual identity while maintaining design consistency and accessibility. Tenants can customize primary, secondary, accent, background, and text colors, along with font choices and type scale. The system automatically generates complementary colors (hover states, border colors, muted variants) from the primary color to ensure a cohesive look.

Color customization must enforce WCAG AA accessibility standards. The system automatically checks contrast ratios between text and background colors, rejecting combinations that don't meet the 4.5:1 minimum for normal text. For typography, tenants can choose from a curated set of Google Fonts or upload their own web fonts, with automatic subset generation for performance.

The typography scale defines font sizes, line heights, and weights for all UI elements (headings, body, captions, code). Tenants can adjust the base font size (default 16px) and scale ratio (1.25 for minor third, 1.5 for perfect fifth), which cascades to all type levels.

## Implementation Approach

```typescript
interface TenantPalette {
  primary: string;      // #6366f1
  secondary: string;    // #8b5cf6  
  accent: string;       // #f59e0b
  background: string;   // #ffffff
  surface: string;      // #f8fafc
  text: string;         // #0f172a
  textSecondary: string;// #475569
  border: string;       // #e2e8f0
  success: string;      // #10b981
  warning: string;      // #f59e0b
  error: string;        // #ef4444
  info: string;         // #3b82f6
}

class PaletteGenerator {
  generateCompletePalette(primary: string): TenantPalette {
    const color = chroma(primary);
    
    return {
      primary,
      secondary: this.complementary(color).hex(),
      accent: this.tetradic(color)[1].hex(),
      background: this.lightest(color).hex(),
      surface: color.brighten(2.5).hex(),
      text: color.darken(4).hex(),
      textSecondary: color.darken(2.5).hex(),
      border: color.brighten(1.5).hex(),
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    };
  }

  validateContrast(palette: TenantPalette): ContrastViolation[] {
    const violations: ContrastViolation[] = [];
    const pairs = [
      { fg: palette.text, bg: palette.background, label: 'Body text' },
      { fg: palette.textSecondary, bg: palette.background, label: 'Secondary text' },
    ];

    for (const { fg, bg, label } of pairs) {
      const ratio = chroma.contrast(fg, bg);
      if (ratio < 4.5) {
        violations.push({ label, ratio, minimum: 4.5 });
      }
    }

    return violations;
  }

  fontScale(baseSize: number, ratio: number, levels: string[]) {
    const scale: Record<string, string> = {};
    levels.forEach((level, i) => {
      const size = baseSize * Math.pow(ratio, i - levels.indexOf('body'));
      scale[level] = `${size.toFixed(1)}px`;
    });
    return scale;
  }
}
```

## Open-Source Tools

- **Chroma.js** — Color manipulation and contrast checking
- **Google Fonts API** — Curated web font library
- **Fontsource** — Self-hosted open-source fonts
- **Woff2** — Web font compression format
- **type-scale.com** — Visual type scale calculator

## Production Considerations

- **Accessibility Enforcement:** Never allow color combinations that fail WCAG AA. For enterprise tenants, offer WCAG AAA compliance checking as a premium feature.
- **Font Loading Performance:** Web fonts can delay page rendering. Use `font-display: swap` and preload critical fonts. Subset fonts to include only needed characters.
- **Palette Preview:** Show real-time preview of color changes before saving. Apply the proposed palette to sample UI components so tenants can see the result.
- **Dark Mode:** Generate dark mode palette automatically from light mode. Ensure both modes meet contrast requirements.
