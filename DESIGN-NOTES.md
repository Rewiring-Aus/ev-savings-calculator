# EV Savings Calculator — Design Notes

Reference guide for the visual language used in this project. Use these notes to maintain consistency or apply the same style to future Rewiring Australia projects.

---

## Fonts

| Use | Font | Weights | Source |
|-----|------|---------|--------|
| LED sign price digits | **Kode Mono** | 300, 700 | Google Fonts |
| All UI text (headings, body, labels, inputs) | **Roboto** | 300 (light), 400 (regular), 500 (medium), 700 (bold) | Google Fonts |
| Sign row labels | Arial Narrow / Arial (system fallback) | 700 | System |

---

## Colour Palette

### Brand / Accent
- **Primary purple**: `#4a00c3` — used for interactive elements, select text, headings, buttons, rough.js box strokes, checkbox accents
- **Rewiring Australia yellow**: `#f0cf61` — used for sign brand stripe, savings highlighter, yellow banner accents

### Fossil Fuel vs Electric
- **Petrol / fossil red**: `#991100` — fillup card price, rough.js box stroke for petrol card
- **EV green**: `#0d6e2d` — fillup card price, rough.js box stroke for EV card

### LED Glow Colours (sign digits)
- **Petrol rows (red)**: `#ff2200` with layered text-shadow glow (`#ff4422`, `rgba(255,60,0,0.70)`, etc.)
- **Fast Charger (blue)**: `#2299ff` with blue glow
- **Grid (teal)**: `#00ccaa` with teal glow
- **Solar (green)**: `#44ee22` with green glow

### Backgrounds
- **Page gradient**: `linear-gradient(175deg, #9db8cc 0%, #b8cfd8 45%, #c4c8b4 70%, #b8b49a 100%)` — cool blue-grey fading to warm beige
- **Sign face rows**: `linear-gradient(150deg, #e6e5e3 0%, #d5d4d2 100%)` — warm grey metal
- **Sign brand panel**: `linear-gradient(150deg, #4a00c3 0%, #2a00a3 100%)` — deep purple
- **Paper texture (action panel)**: Warm off-white with ruled lines:
  ```css
  background:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 27px,
      rgba(120,120,140,0.07) 27px,
      rgba(120,120,140,0.07) 28px
    ),
    linear-gradient(135deg, #f5f0e8 0%, #ede7db 30%, #f2ece2 60%, #e8e2d6 100%);
  ```

### Text Colours (contrast-tuned for the blue-grey page background)
- **Headings**: `#222`
- **Body text**: `#333`
- **Secondary labels**: `#444`
- **Subtle / supporting text**: `#555`
- **Muted footnotes**: `#555` (was `#888`, darkened for contrast)

---

## rough.js Hand-Drawn Boxes

We use [rough.js](https://roughjs.com/) (v4.6.6) to draw hand-drawn style annotation boxes around interactive elements and result cards.

### Inline select wraps (dropdowns)
```js
rc.rectangle(2, 2, w - 4, h - 4, {
  stroke: '#4a00c3',
  strokeWidth: 1.5,
  roughness: 1.5,
  bowing: 1.5,
});
```

### Fillup comparison cards (petrol vs EV)
```js
rc.rectangle(2, 2, w - 4, h - 4, {
  stroke: isEv ? '#0d6e2d' : '#991100',
  strokeWidth: 1.8,
  roughness: 2,
  bowing: 1.5,
});
```

### Savings summary box (outer)
```js
rc.rectangle(2, 2, w - 4, h - 4, {
  stroke: '#4a00c3',
  strokeWidth: 2,
  roughness: 1.8,
  bowing: 2,
});
```

### Yellow highlighter ("You save" row)
```js
rc.rectangle(0, h * 0.25, w, h * 0.6, {
  fill: '#f0cf61',
  fillStyle: 'solid',
  stroke: 'none',
  roughness: 2.5,
  bowing: 2,
});
```

### Implementation Notes
- SVGs are absolutely positioned (`position: absolute; top: 0; left: 0; pointer-events: none`) inside relatively positioned containers
- A `ResizeObserver` watches all rough.js target elements and redraws only when their size changes — avoids unnecessary redraws on scroll
- After each `renderConfig()` call, `drawRoughBox()` is called in a `requestAnimationFrame` and then `observeRoughTargets()` re-attaches the observer to the new DOM elements

---

## 3D Sign Perspective

The petrol bowser sign uses CSS 3D transforms to create a "viewed from below-right" perspective, as an Australian driver would see a roadside sign:

```css
.scene {
  perspective: 1600px;
  perspective-origin: 65% 70%;
}
.sign-wrap {
  transform: rotateY(-8deg) rotateX(4deg);
}
```

A right-side depth face (22px wide, dark grey gradient) completes the 3D illusion.

---

## Animation

### Petrol price spin-up
- Prices start at 175.0 and climb to their real value over 10 seconds
- Uses `easeOutExpo` easing via `requestAnimationFrame`
- Creates a "rising fuel prices" visual effect on page load

### EV price flicker-on
- EV rows start hidden and flicker on after a 4-second delay
- Staggered 600ms between each row (Fast Charger → Grid → Solar → Solar Sharer)
- CSS `flicker-on` animation simulates an LED display powering up

---

## Responsive Breakpoints

Single breakpoint at **768px**:

```css
@media (max-width: 768px) {
  body { padding: 20px 16px; gap: 30px; }
  .sign-face { width: min(290px, 80vw); }
  .config-panel { width: 100%; max-width: 400px; }
  .action-panel { max-width: 100%; padding: 24px 20px 28px; }
}
```

Desktop: sign (290px) and config panel (320px) sit side by side with 60px gap. Below 768px they stack vertically and go full-width. The action panel always spans full width below both columns (`flex-basis: 100%`).
