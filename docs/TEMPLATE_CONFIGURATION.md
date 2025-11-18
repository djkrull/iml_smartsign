# SmartSign Template Configuration - IML Seminar Display

**Step-by-step guide to recreate the HTML preview in SmartSign Template Creator**

---

## 📋 Prerequisites

Before starting, upload these assets to SmartSign Media Library:

1. **Background Image:** `iml_background.jpg` (yellow geometric pattern)
2. **Logo:** `iml_logo.png` (IML logo - transparent PNG preferred)
3. **Font:** `DINPro-Regular.otf` (upload to SmartSign font library)

---

## 🎨 Template Settings

### Basic Configuration

| Setting | Value |
|---------|-------|
| **Name** | IML Seminar Display |
| **Type** | Smart Media |
| **Orientation** | Landscape |
| **Resolution** | 1920 x 1080 px |
| **Background** | Use uploaded background image |

---

## 📐 Layer Structure (Bottom to Top)

```
Layer 10: Logo (Top Right)
Layer 9: Location Text (Data-bound)
Layer 8: Speaker Text (Data-bound)
Layer 7: Title Text (Data-bound)
Layer 6: Date/Time Text (Data-bound)
Layer 5: Seminar Card Background (White rectangle with shadow)
Layer 4: Seminar Card Border (Yellow left border)
Layer 3: Header Card Background (White rectangle)
Layer 2: Header Text (Static: "SEMINARS THIS WEEK")
Layer 1: Background Image
```

---

## 🎯 Element-by-Element Configuration

### LAYER 1: Background Image

**Element Type:** Image

| Property | Value |
|----------|-------|
| **Image** | `iml_background.jpg` |
| **Position X** | 0 px |
| **Position Y** | 0 px |
| **Width** | 1920 px |
| **Height** | 1080 px |
| **Fit** | Cover |
| **Opacity** | 100% |

**Optional Overlay:**
- Add a rectangle shape
- Size: 1920 x 1080 px
- Fill: Linear gradient (FFC107 to FFEB3B at 15% opacity)
- Position: 0, 0

---

### LAYER 2: Header Background

**Element Type:** Rectangle Shape

| Property | Value |
|----------|-------|
| **Position X** | 80 px |
| **Position Y** | 60 px |
| **Width** | 1000 px |
| **Height** | 120 px |
| **Fill Color** | #FFFFFF (white) |
| **Opacity** | 95% |
| **Border Radius** | 12 px |
| **Shadow** | Yes |
| **Shadow Blur** | 20 px |
| **Shadow Color** | #000000 at 10% opacity |
| **Shadow Offset X** | 0 px |
| **Shadow Offset Y** | 6 px |

---

### LAYER 3: Header Text

**Element Type:** Text

| Property | Value |
|----------|-------|
| **Content** | `Seminars this week` |
| **Data Binding** | None (static text) |
| **Position X** | 130 px |
| **Position Y** | 85 px |
| **Width** | 900 px |
| **Height** | 80 px |
| **Font Family** | Georgia, serif |
| **Font Size** | 72 px |
| **Font Weight** | Bold |
| **Color** | #084077 (IML dark blue) |
| **Alignment** | Left |
| **Letter Spacing** | -1 px |

---

### LAYER 4: Seminar Card Border (Yellow Accent)

**Element Type:** Rectangle Shape

| Property | Value |
|----------|-------|
| **Position X** | 80 px |
| **Position Y** | 260 px |
| **Width** | 8 px |
| **Height** | 160 px |
| **Fill Color** | #FFC107 (yellow/gold) |
| **Border Radius** | 4 px (left side only) |
| **Opacity** | 100% |

**Note:** Create one per seminar row

---

### LAYER 5: Seminar Card Background

**Element Type:** Rectangle Shape

| Property | Value |
|----------|-------|
| **Position X** | 88 px |
| **Position Y** | 260 px |
| **Width** | 1752 px |
| **Height** | 160 px |
| **Fill Color** | #FFFFFF (white) |
| **Opacity** | 97% |
| **Border Radius** | 0 10 10 0 px (right side rounded) |
| **Shadow** | Yes |
| **Shadow Blur** | 15 px |
| **Shadow Color** | #000000 at 12% opacity |
| **Shadow Offset Y** | 4 px |

**Note:** Create one per seminar row

---

### LAYER 6: Date and Time (Data-Bound)

**Element Type:** Text

| Property | Value |
|----------|-------|
| **Content** | `{{Date_Formatted}} • {{Time}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier (CSV) |
| **Column 1** | `Date_Formatted` |
| **Column 2** | `Time` |
| **Position X** | 125 px |
| **Position Y** | 275 px |
| **Width** | 1000 px |
| **Height** | 40 px |
| **Font Family** | DINPro Regular |
| **Font Size** | 32 px |
| **Font Weight** | 600 (Semi-bold) |
| **Color Date** | #1976D2 (blue) |
| **Color Time** | #E91E63 (pink) |
| **Separator** | • (bullet, color #999999) |
| **Alignment** | Left |

**Template Syntax:**
```html
<span style="color:#1976D2">{{Date_Formatted}}</span>
<span style="color:#999999"> • </span>
<span style="color:#E91E63">{{Time}}</span>
```

---

### LAYER 7: Seminar Title (Data-Bound)

**Element Type:** Text

| Property | Value |
|----------|-------|
| **Content** | `{{Title}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier (CSV) |
| **Column** | `Title` |
| **Position X** | 125 px |
| **Position Y** | 315 px |
| **Width** | 1680 px |
| **Height** | 55 px |
| **Font Family** | DINPro Regular |
| **Font Size** | 42 px |
| **Font Weight** | Bold |
| **Color** | #084077 (IML dark blue) |
| **Alignment** | Left |
| **Line Height** | 1.3 |
| **Max Lines** | 1 |
| **Overflow** | Ellipsis (...) |

---

### LAYER 8: Speaker Information (Data-Bound)

**Element Type:** Text

| Property | Value |
|----------|-------|
| **Content** | `Speaker: {{Speaker}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier (CSV) |
| **Column** | `Speaker` |
| **Position X** | 125 px |
| **Position Y** | 370 px |
| **Width** | 1200 px |
| **Height** | 35 px |
| **Font Family** | DINPro Regular |
| **Font Size** | 32 px |
| **Font Weight** | Normal |
| **Color Label** | #555555 (medium gray) |
| **Color Name** | #084077 (IML dark blue) |
| **Alignment** | Left |

**Template Syntax:**
```html
<span style="font-weight:600; color:#555555">Speaker:</span>
<span style="color:#084077">{{Speaker}}</span>
```

---

### LAYER 9: Location (Data-Bound)

**Element Type:** Text

| Property | Value |
|----------|-------|
| **Content** | `Location: {{Location}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier (CSV) |
| **Column** | `Location` |
| **Position X** | 125 px |
| **Position Y** | 395 px |
| **Width** | 800 px |
| **Height** | 30 px |
| **Font Family** | DINPro Regular |
| **Font Size** | 30 px |
| **Font Weight** | Normal |
| **Color Label** | #666666 (gray) |
| **Color Name** | #444444 (dark gray) |
| **Alignment** | Left |

**Template Syntax:**
```html
<span style="font-weight:600; color:#666666">Location:</span>
<span style="color:#444444">{{Location}}</span>
```

---

### LAYER 10: IML Logo (Top Right)

**Element Type:** Image

| Property | Value |
|----------|-------|
| **Image** | `iml_logo.png` |
| **Position X** | 1720 px |
| **Position Y** | 40 px |
| **Width** | Auto (maintain aspect ratio) |
| **Height** | 120 px |
| **Max Width** | 300 px |
| **Fit** | Contain |
| **Alignment** | Right |
| **Object Fit** | Contain (maintains aspect ratio) |

**Note:** Logo displays WITHOUT white background box

---

## 🔄 Repeating/Scrolling Configuration

Since you have multiple seminars, configure how they display:

### Option A: Vertical Scrolling List

| Setting | Value |
|---------|-------|
| **Display Mode** | Vertical Scroll |
| **Items Visible** | 4 seminars |
| **Scroll Speed** | Slow (20 seconds per full scroll) |
| **Auto-scroll** | ✓ Enabled |
| **Loop** | ✓ Enabled |
| **Spacing** | 25 px between cards |

### Option B: Pagination (Recommended)

| Setting | Value |
|---------|-------|
| **Display Mode** | Paginated |
| **Items per Page** | 4 seminars |
| **Duration per Page** | 15 seconds |
| **Transition** | Fade (0.5s) |
| **Loop** | ✓ Enabled |

---

## 🎬 Animation Settings (Optional)

### Card Entrance Animation

| Property | Value |
|----------|-------|
| **Animation** | Fade In + Slide Up |
| **Duration** | 0.5 seconds |
| **Easing** | Ease-out |
| **Stagger Delay** | 0.1s between cards |

### Hover Effect (if supported)

| Property | Value |
|---------|-------|
| **Transform** | Translate X +5px |
| **Shadow Increase** | 20px blur (from 15px) |
| **Transition** | 0.2 seconds |

---

## 📏 Exact Positioning Guide

### Seminar Card Positions (for 4 visible seminars)

**Card 1:**
- Position: (80, 260)
- Size: 1760 x 160 px

**Card 2:**
- Position: (80, 445)
- Size: 1760 x 160 px

**Card 3:**
- Position: (80, 630)
- Size: 1760 x 160 px

**Card 4:**
- Position: (80, 815)
- Size: 1760 x 160 px

**Spacing:** 25 px gap between cards

---

## 🎨 Color Palette

| Element | Color Code | RGB | Usage |
|---------|------------|-----|-------|
| **IML Dark Blue** | #084077 | 8, 64, 119 | Titles, headers, main text |
| **Primary Yellow** | #FFC107 | 255, 193, 7 | Card border accent |
| **Light Yellow** | #FFEB3B | 255, 235, 59 | Background gradient |
| **Blue (Date)** | #1976D2 | 25, 118, 210 | Date text |
| **Pink (Time)** | #E91E63 | 233, 30, 99 | Time text |
| **Medium Gray** | #666666 | 102, 102, 102 | Labels |
| **Light Gray** | #999999 | 153, 153, 153 | Separators |
| **White** | #FFFFFF | 255, 255, 255 | Card backgrounds |

---

## 📊 Data Binding Reference

### CSV Columns → Template Fields

| CSV Column | Bind To | Example Value |
|------------|---------|---------------|
| `Date_Formatted` | Date text | "Tuesday 18 Nov" |
| `Time` | Time text | "09:30-10:30" |
| `Title` | Title text | "Björn Stinner: Finite..." |
| `Speaker` | Speaker text | "Björn Stinner, University of Warwick" |
| `Location` | Location text | "Kuskvillan" |

### Binding Syntax Examples

**Simple binding:**
```
{{Date_Formatted}}
```

**Multiple fields:**
```
{{Date_Formatted}} • {{Time}}
```

**With labels:**
```
Speaker: {{Speaker}}
Location: {{Location}}
```

**With styling (if supported):**
```html
<span class="label">Speaker:</span> <span class="value">{{Speaker}}</span>
```

---

## ✅ Configuration Checklist

### Pre-Setup
- [ ] Background image uploaded to Media Library
- [ ] Logo uploaded to Media Library (PNG with transparency)
- [ ] DINPro font uploaded to Font Library
- [ ] CSV datasource created and tested

### Template Creation
- [ ] New Smart Media template created (1920x1080)
- [ ] Background image added and positioned
- [ ] Header section created (white card + text)
- [ ] Logo positioned in top right
- [ ] Seminar card created (border + background)
- [ ] Date/Time text added with data binding
- [ ] Title text added with data binding
- [ ] Speaker text added with data binding
- [ ] Location text added with data binding

### Data Binding
- [ ] Datasource linked to template
- [ ] All data bindings configured
- [ ] Column names match CSV exactly
- [ ] Preview shows data correctly

### Styling
- [ ] Font family set to DINPro
- [ ] Colors match specification
- [ ] Font sizes correct
- [ ] Spacing and positioning accurate

### Display Configuration
- [ ] Repeating/scrolling configured
- [ ] Animation settings applied (optional)
- [ ] Preview tested with real data

### Final Steps
- [ ] Template saved
- [ ] Booking created with template
- [ ] Channel assigned
- [ ] Live test on screen

---

## 🔍 Troubleshooting

### Data Not Showing

**Problem:** Template shows placeholder text, not actual data

**Solutions:**
1. Verify datasource is linked to template
2. Check column names match exactly (case-sensitive)
3. Ensure datasource has fetched data (check row count)
4. Re-bind data fields in template editor

### Font Not Loading

**Problem:** DINPro font not displaying

**Solutions:**
1. Verify font uploaded to SmartSign font library
2. Check font format is OTF (not TTF)
3. Try fallback: Arial or Helvetica
4. Clear browser cache and reload template editor

### Images Not Appearing

**Problem:** Background or logo not visible

**Solutions:**
1. Check images uploaded to Media Library
2. Verify image file formats (JPG for background, PNG for logo)
3. Check file sizes aren't too large (< 5 MB recommended)
4. Ensure images are selected correctly in template

### Layout Misaligned

**Problem:** Elements not positioned correctly

**Solutions:**
1. Double-check X/Y coordinates in this guide
2. Verify screen resolution is 1920x1080
3. Use template grid/guides for alignment
4. Preview at 100% zoom (not scaled)

### Cards Overlapping

**Problem:** Seminar cards overlap each other

**Solutions:**
1. Check repeating/pagination settings
2. Ensure "Items per page" is set to 4
3. Verify spacing between cards (25 px)
4. Adjust card height if needed (currently 160 px)

---

## 📐 Design Specifications Summary

**Screen:** 1920 x 1080 px (Full HD Landscape)
**Safe Area:** 80 px margin on all sides
**Grid:** 4 seminar cards visible at once
**Spacing:** 25 px between elements
**Border Radius:** 8-12 px for cards
**Shadows:** Subtle, 4-6 px offset, 10-15% opacity
**Animations:** Optional fade-in on load

---

## 🎓 Advanced Tips

### Custom Transitions

For smooth data updates when CSV refreshes:
- Use fade transition (0.3-0.5 seconds)
- Avoid jarring instant updates
- Consider cross-fade between old and new data

### Accessibility

- Ensure text contrast ratio > 4.5:1
- Font sizes large enough for distance reading
- Avoid pure white backgrounds (use 97% opacity)

### Performance

- Optimize images (< 500 KB each)
- Limit animations to entrance only
- Use CSS animations when possible
- Avoid video backgrounds (static image is faster)

---

## 📱 Alternative Layouts

### Portrait Orientation (1080 x 1920)

If using vertical screens:
- Stack seminars vertically (same design)
- Show 6-8 seminars per page
- Reduce font sizes by ~20%
- Adjust spacing proportionally

### Multiple Screens

If splitting across multiple screens:
- Screen 1: Header + Seminars 1-4
- Screen 2: Seminars 5-8
- Use identical styling for consistency

---

## 📚 Related Documentation

- **HTML Preview:** `template_preview.html` (open in browser)
- **SmartSign CMS Guide:** `docs/SMARTSIGN_CONFIG.md`
- **Deployment Guide:** `docs/DEPLOYMENT_MODERN.md`
- **CSV Data Format:** See `seminarier.csv`

---

## 🆘 Need Help?

**SmartSign Template Editor:**
- Help docs: https://support.smartsign.com/template-creator
- Support: support@smartsign.com

**This Project:**
- See: `README.md` for overview
- Contact: IML IT Team (it@iml.se)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-17
**Template Name:** IML Seminar Display
**Screen Resolution:** 1920 x 1080 px (Full HD)
