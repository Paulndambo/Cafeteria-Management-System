# Quick Reference - POS Theme Implementation

## Color Quick Reference

| Use Case | Color | Hex Code |
|----------|-------|----------|
| Primary Actions | Cyan | `#0891b2` |
| Hover States | Dark Cyan | `#0e7490` |
| Accents | Teal | `#14b8a6` |
| Secondary Actions | Indigo | `#6366f1` |
| Success | Emerald | `#10b981` |
| Warning | Amber | `#f59e0b` |
| Danger | Red | `#ef4444` |
| Info | Blue | `#3b82f6` |
| Text Primary | Dark Slate | `#0f172a` |
| Text Secondary | Slate Gray | `#64748b` |
| Background | Light Gray | `#f8fafc` |
| Cards | White | `#ffffff` |
| Borders | Light Slate | `#e2e8f0` |

## Common CSS Classes

### Buttons
```html
<!-- Primary Button -->
<button class="btn btn-primary">Action</button>

<!-- Success Button -->
<button class="btn btn-success">Confirm</button>

<!-- Warning Button -->
<button class="btn btn-warning">Caution</button>

<!-- Danger Button -->
<button class="btn btn-danger">Delete</button>

<!-- Secondary Button -->
<button class="btn btn-info">Info</button>
```

### Cards
```html
<!-- Dashboard Card -->
<div class="dashboard-card card-primary">
  <div class="card-icon">
    <i class="bi bi-cart"></i>
  </div>
  <h6 class="card-title">Total Sales</h6>
  <h3 class="card-value">KSh 50,000</h3>
</div>
```

### Product Cards (POS)
```html
<a href="#" class="product-card">
  <img src="product.jpg" alt="Product">
  <h3 class="product-title">Product Name</h3>
  <p class="product-price">500</p>
</a>
```

### Tables
```html
<table class="table">
  <thead>
    <tr>
      <th>Column 1</th>
      <th>Column 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data 1</td>
      <td>Data 2</td>
    </tr>
  </tbody>
</table>
```

### Badges
```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Danger</span>
```

### Transaction Status
```html
<span class="transaction-status completed">Completed</span>
<span class="transaction-status pending">Pending</span>
<span class="transaction-status failed">Failed</span>
```

### Price Tags
```html
<span class="price-tag">KSh 1,500</span>
<span class="price-tag-large">KSh 50,000</span>
```

### Quantity Controls
```html
<div class="quantity-control">
  <button>-</button>
  <span>5</span>
  <button>+</button>
</div>
```

## Typography

### Font Families
- **Body Text**: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- **Numbers/Prices**: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace

### Font Weights
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700
- **Extrabold**: 800

### Font Sizes
- **Small**: 0.75rem (12px)
- **Base**: 0.875rem (14px)
- **Medium**: 1rem (16px)
- **Large**: 1.125rem (18px)
- **XL**: 1.25rem (20px)
- **2XL**: 1.5rem (24px)
- **3XL**: 2rem (32px)

## Spacing

### Padding/Margin Scale
- **xs**: 0.25rem (4px)
- **sm**: 0.5rem (8px)
- **md**: 0.75rem (12px)
- **lg**: 1rem (16px)
- **xl**: 1.5rem (24px)
- **2xl**: 2rem (32px)

## Border Radius

- **Small**: 0.5rem (8px)
- **Medium**: 0.75rem (12px)
- **Large**: 0.875rem (14px)
- **XL**: 1rem (16px)

## Borders

- **Standard**: 2px solid
- **Accent**: 3px solid
- **Thin**: 1px solid

## Shadows

```css
/* Standard Shadows */
--shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

/* Colored Shadows (Hover) */
Cyan: 0 6px 20px rgba(8, 145, 178, 0.3);
Emerald: 0 6px 16px rgba(16, 185, 129, 0.3);
Amber: 0 6px 16px rgba(245, 158, 11, 0.3);
Red: 0 6px 16px rgba(239, 68, 68, 0.3);
```

## Transitions

```css
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

## Hover Effects

### Standard Hover
```css
element:hover {
  transform: translateY(-2px);
  box-shadow: [colored-shadow];
}
```

### Card Hover
```css
.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(8, 145, 178, 0.2);
}
```

### Button Hover
```css
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(8, 145, 178, 0.3);
}
```

## Gradients

### Button Gradients
```css
/* Primary */
background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);

/* Success */
background: linear-gradient(135deg, #10b981 0%, #34d399 100%);

/* Warning */
background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);

/* Danger */
background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);

/* Secondary */
background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
```

### Background Gradients
```css
/* Page Background */
background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f8fafc 100%);

/* Card Header */
background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);

/* Table Header */
background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
```

## Icons

### Recommended Icon Library
Bootstrap Icons (already included)

### Common Icons
- Cart: `bi-cart`, `bi-cart-fill`
- Shop: `bi-shop`
- People: `bi-people`, `bi-people-fill`
- Cash: `bi-cash-stack`, `bi-cash-coin`
- Receipt: `bi-receipt`, `bi-receipt-cutoff`
- Plus: `bi-plus-circle`, `bi-plus-lg`
- Minus: `bi-dash-circle`, `bi-dash-lg`
- Check: `bi-check-circle`, `bi-check-lg`
- X: `bi-x-circle`, `bi-x-lg`

## Responsive Breakpoints

```css
/* Mobile First */
@media (min-width: 576px) { /* Small devices */ }
@media (min-width: 768px) { /* Tablets */ }
@media (min-width: 992px) { /* Desktops */ }
@media (min-width: 1200px) { /* Large desktops */ }
```

## Common Patterns

### POS Grid Layout
```html
<div class="pos-grid">
  <div class="products-section">
    <!-- Product cards -->
  </div>
  <div class="cart-section">
    <!-- Cart items -->
  </div>
</div>
```

### Status Indicator
```html
<div class="d-flex align-items-center">
  <span class="transaction-status completed">Completed</span>
</div>
```

### Price Display
```html
<div class="d-flex justify-content-between">
  <span>Total:</span>
  <span class="price-tag">KSh 5,000</span>
</div>
```

### Receipt Divider
```html
<hr class="receipt-divider">
```

## File Locations

- **Main Styles**: `static/dashboard.css`
- **Base Template**: `templates/new_base.html`
- **POS Page**: `templates/orders/pos.html`
- **Sidebar**: `templates/includes/new_sidebar.html`

## Testing Checklist

- [ ] All buttons have hover effects
- [ ] Cards lift on hover
- [ ] Forms have focus states
- [ ] Tables have hover rows
- [ ] Colors are consistent
- [ ] Shadows are visible
- [ ] Gradients render correctly
- [ ] Text is readable
- [ ] Icons are aligned
- [ ] Responsive on mobile
- [ ] Transitions are smooth
- [ ] No layout shifts

## Browser Support

- Chrome/Edge: ✓ Full support
- Firefox: ✓ Full support
- Safari: ✓ Full support
- Mobile browsers: ✓ Full support

## Performance Tips

1. Use CSS transforms for animations (GPU accelerated)
2. Avoid animating width/height (use scale instead)
3. Use will-change sparingly
4. Optimize images for web
5. Minimize CSS file size
6. Use system fonts when possible

## Accessibility

- Maintain color contrast ratios (WCAG AA minimum)
- Use semantic HTML
- Include ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers
- Don't rely on color alone for information

## Common Issues & Solutions

### Issue: Hover effects not working
**Solution**: Check z-index and pointer-events

### Issue: Gradients not showing
**Solution**: Ensure proper vendor prefixes

### Issue: Shadows too dark
**Solution**: Reduce opacity in rgba values

### Issue: Text not readable
**Solution**: Check color contrast ratios

### Issue: Layout breaking on mobile
**Solution**: Test responsive breakpoints

## Quick Customization

To change primary color throughout:
1. Update `--primary-color` in `:root`
2. Update `--primary-dark` (darker shade)
3. Update `--primary-light` (lighter shade)
4. Update shadow colors in hover states
5. Test contrast ratios

## Support

For questions or issues:
1. Check this documentation
2. Review POS_DESIGN_CHANGES.md
3. Check COLOR_PALETTE_GUIDE.md
4. Inspect browser DevTools
5. Test in different browsers

