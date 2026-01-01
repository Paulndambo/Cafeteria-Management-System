# Color Palette Guide - POS/Sales Platform Theme

## Primary Color Palette

### Main Brand Colors
```
┌─────────────────────────────────────────────────────────────┐
│ Primary Cyan                                                │
│ #0891b2 (rgb(8, 145, 178))                                 │
│ ████████████████████████████████████████████████████████   │
│ Use: Primary buttons, links, active states, headers        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Primary Dark (Hover)                                        │
│ #0e7490 (rgb(14, 116, 144))                                │
│ ████████████████████████████████████████████████████████   │
│ Use: Button hover states, darker accents                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Primary Light                                               │
│ #06b6d4 (rgb(6, 182, 212))                                 │
│ ████████████████████████████████████████████████████████   │
│ Use: Gradients, light accents, highlights                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Accent Teal                                                 │
│ #14b8a6 (rgb(20, 184, 166))                                │
│ ████████████████████████████████████████████████████████   │
│ Use: Sidebar accents, special highlights, borders          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Secondary Indigo                                            │
│ #6366f1 (rgb(99, 102, 241))                                │
│ ████████████████████████████████████████████████████████   │
│ Use: Secondary buttons, alternate actions, info displays   │
└─────────────────────────────────────────────────────────────┘
```

## Semantic Colors

### Success
```
┌─────────────────────────────────────────────────────────────┐
│ Success Emerald                                             │
│ #10b981 (rgb(16, 185, 129))                                │
│ ████████████████████████████████████████████████████████   │
│ Use: Success messages, completed actions, positive states  │
└─────────────────────────────────────────────────────────────┘
```

### Warning
```
┌─────────────────────────────────────────────────────────────┐
│ Warning Amber                                               │
│ #f59e0b (rgb(245, 158, 11))                                │
│ ████████████████████████████████████████████████████████   │
│ Use: Warnings, pending states, caution indicators          │
└─────────────────────────────────────────────────────────────┘
```

### Danger
```
┌─────────────────────────────────────────────────────────────┐
│ Danger Red                                                  │
│ #ef4444 (rgb(239, 68, 68))                                 │
│ ████████████████████████████████████████████████████████   │
│ Use: Errors, delete actions, critical alerts               │
└─────────────────────────────────────────────────────────────┘
```

### Info
```
┌─────────────────────────────────────────────────────────────┐
│ Info Blue                                                   │
│ #3b82f6 (rgb(59, 130, 246))                                │
│ ████████████████████████████████████████████████████████   │
│ Use: Information displays, help text, neutral actions      │
└─────────────────────────────────────────────────────────────┘
```

## Neutral Colors

### Text Colors
```
┌─────────────────────────────────────────────────────────────┐
│ Dark Slate (Primary Text)                                  │
│ #0f172a (rgb(15, 23, 42))                                  │
│ ████████████████████████████████████████████████████████   │
│ Use: Primary text, headings, important content             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Slate Gray (Secondary Text)                                │
│ #64748b (rgb(100, 116, 139))                               │
│ ████████████████████████████████████████████████████████   │
│ Use: Secondary text, descriptions, labels                  │
└─────────────────────────────────────────────────────────────┘
```

### Background Colors
```
┌─────────────────────────────────────────────────────────────┐
│ Light Background                                            │
│ #f8fafc (rgb(248, 250, 252))                               │
│ ████████████████████████████████████████████████████████   │
│ Use: Page backgrounds, light sections                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Card Background                                             │
│ #ffffff (rgb(255, 255, 255))                               │
│ ████████████████████████████████████████████████████████   │
│ Use: Cards, modals, elevated surfaces                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Border Color                                                │
│ #e2e8f0 (rgb(226, 232, 240))                               │
│ ████████████████████████████████████████████████████████   │
│ Use: Borders, dividers, separators                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Hover Background                                            │
│ #f1f5f9 (rgb(241, 245, 249))                               │
│ ████████████████████████████████████████████████████████   │
│ Use: Hover states, subtle backgrounds                      │
└─────────────────────────────────────────────────────────────┘
```

## Gradient Combinations

### Primary Gradients
```css
/* Cyan Gradient (Primary Buttons) */
background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);

/* Cyan Dark Gradient (Hover) */
background: linear-gradient(135deg, #0e7490 0%, #0891b2 100%);

/* Sidebar Gradient */
background: linear-gradient(180deg, #0891b2 0%, #0e7490 100%);

/* Page Background Gradient */
background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f8fafc 100%);
```

### Semantic Gradients
```css
/* Success Gradient */
background: linear-gradient(135deg, #10b981 0%, #34d399 100%);

/* Warning Gradient */
background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);

/* Danger Gradient */
background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);

/* Info/Secondary Gradient */
background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
```

### Accent Gradients
```css
/* Top Accent Bar */
background: linear-gradient(90deg, #0891b2 0%, #14b8a6 50%, #6366f1 100%);

/* Card Header */
background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);

/* Table Header */
background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
```

## Shadow Colors

### Standard Shadows
```css
/* Small Shadow */
box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);

/* Medium Shadow */
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);

/* Large Shadow */
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);

/* Extra Large Shadow */
box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

### Colored Shadows (Hover States)
```css
/* Cyan Shadow (Primary) */
box-shadow: 0 6px 20px rgba(8, 145, 178, 0.3);

/* Teal Shadow (Accent) */
box-shadow: 0 8px 20px rgba(20, 184, 166, 0.2);

/* Emerald Shadow (Success) */
box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);

/* Amber Shadow (Warning) */
box-shadow: 0 6px 16px rgba(245, 158, 11, 0.3);

/* Red Shadow (Danger) */
box-shadow: 0 6px 16px rgba(239, 68, 68, 0.3);

/* Indigo Shadow (Secondary) */
box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3);
```

## Usage Guidelines

### Do's ✓
- Use cyan (#0891b2) as the primary brand color
- Use teal (#14b8a6) for accents and highlights
- Use gradients for buttons and important elements
- Use colored shadows on hover for depth
- Use monospace fonts for numbers and prices
- Maintain 2px borders for definition
- Use uppercase text with letter-spacing for labels

### Don'ts ✗
- Don't mix too many gradient directions
- Don't use pure black (#000000) - use dark slate instead
- Don't use thin borders (< 1px) - maintain visibility
- Don't overuse animations - keep them subtle
- Don't use colors outside the palette without reason
- Don't forget hover states on interactive elements

## Accessibility Notes

### Contrast Ratios
- Primary Cyan on White: 4.5:1 (AA compliant)
- Dark Slate on White: 16.1:1 (AAA compliant)
- Slate Gray on White: 4.6:1 (AA compliant)

### Color Blind Considerations
- Cyan and red provide good contrast for most color blindness types
- Always use icons or text alongside color indicators
- Status indicators include animated dots, not just color

## Component-Specific Colors

### Sidebar
- Background: Cyan gradient
- Active border: Teal (#14b8a6)
- Text: White (#ffffff)

### Cards
- Background: White (#ffffff)
- Border: Light gray (#e2e8f0)
- Top accent: Cyan-teal-indigo gradient

### Tables
- Header background: Light slate gradient
- Header text: Cyan (#0891b2)
- Border: Cyan (#0891b2)

### Buttons
- Primary: Cyan gradient
- Success: Emerald gradient
- Warning: Amber gradient
- Danger: Red gradient
- Secondary: Indigo gradient

### Forms
- Border: Light gray (#e2e8f0)
- Focus border: Cyan (#0891b2)
- Focus shadow: Cyan with 15% opacity

## CSS Variables Reference

```css
:root {
  /* Primary Colors */
  --primary-color: #0891b2;
  --primary-dark: #0e7490;
  --primary-light: #06b6d4;
  
  /* Secondary & Accent */
  --secondary-color: #6366f1;
  --accent-color: #14b8a6;
  
  /* Semantic Colors */
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --info-color: #3b82f6;
  
  /* Neutral Colors */
  --dark-color: #0f172a;
  --light-color: #f8fafc;
  --border-color: #e2e8f0;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --card-bg: #ffffff;
  --hover-bg: #f1f5f9;
}
```

