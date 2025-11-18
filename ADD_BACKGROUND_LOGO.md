# Adding Background Image & Logo to Existing Display

**Quick guide to add missing assets**

---

## 🎯 What You Need

Based on your screenshot, you have the seminar cards working but missing:

1. ❌ **Background image** (yellow geometric pattern)
2. ❌ **IML logo** (top right corner)

Let me help you add these!

---

## ✅ Solution 1: Use Updated HTML File

### Step 1: Save Your Images

**Image #1 - Background:**
```
Save as: C:\Users\chrwah28.KVA\Development\smartsign\iml_background.jpg
```

**Image #2 - Logo:**
```
Save as: C:\Users\chrwah28.KVA\Development\smartsign\iml_logo.png
```

### Step 2: Open Updated Template

I've created: `template_with_assets.html`

**This file has:**
- ✅ Background image (with yellow fallback if image doesn't load)
- ✅ Logo in top right (with text fallback)
- ✅ All your seminar data
- ✅ Optimized for 16:9 screens

**Just open it in your browser!**

---

## ✅ Solution 2: Add to SmartSign Template

If you're building in SmartSign Template Creator:

### Add Background Image

1. **Upload image to Media Library:**
   - Go to SmartSign CMS → Media
   - Upload `iml_background.jpg`

2. **In Template Creator:**
   - **Layer 1:** Add Image element
   - **Select:** iml_background.jpg
   - **Position:** X: 0, Y: 0
   - **Size:** 1920 x 1080 px
   - **Fit:** Cover
   - **Z-index:** 0 (bottom layer)

### Add Logo

1. **Upload logo to Media Library:**
   - Upload `iml_logo.png` (PNG with transparent background)

2. **In Template Creator:**
   - **New Layer:** Add Image element
   - **Select:** iml_logo.png
   - **Position:** X: 1720 px, Y: 40 px
   - **Height:** 80 px
   - **Width:** Auto (maintain aspect ratio)
   - **Z-index:** 100 (top layer)

3. **Optional: Add white background behind logo:**
   - Add Rectangle shape
   - Position: X: 1700 px, Y: 30 px
   - Size: 220 x 120 px
   - Fill: White (#FFFFFF, 98% opacity)
   - Border Radius: 8 px
   - Shadow: 4 px blur, 20% opacity
   - Place BEHIND logo (lower Z-index)

---

## ✅ Solution 3: CSS for Existing Website

If this is a website/custom display, add this CSS:

### Background CSS

```css
body {
    background-image: url('path/to/iml_background.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Fallback yellow gradient if image doesn't load */
body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #FFD54F 0%, #FFC107 25%, #FFEB3B 50%, #FFD54F 75%, #FFC107 100%);
    z-index: -1;
}
```

### Logo CSS

```css
.logo-container {
    position: fixed;
    top: 40px;
    right: 60px;
    z-index: 1000;
    background: rgba(255, 255, 255, 0.98);
    padding: 20px 30px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.logo {
    display: block;
    height: 80px;
    width: auto;
    max-width: 200px;
}
```

### HTML to add:

```html
<div class="logo-container">
    <img src="path/to/iml_logo.png" alt="Institut Mittag-Leffler" class="logo">
</div>
```

---

## 🖼️ Image Requirements

### Background Image (iml_background.jpg)

**Requirements:**
- Format: JPG or PNG
- Size: 1920 x 1080 px minimum (Full HD)
- Aspect ratio: 16:9
- File size: < 2 MB (for fast loading)
- Colors: Yellow/gold tones (#FFC107, #FFEB3B)

**From your Image #1:**
- Yellow geometric pattern
- Should be saved as `iml_background.jpg`

### Logo (iml_logo.png)

**Requirements:**
- Format: PNG (with transparent background)
- Height: ~200-300 px
- Width: Auto (maintain aspect ratio)
- File size: < 500 KB
- Background: Transparent

**From your Image #2:**
- IML logo
- Should be saved as `iml_logo.png`

---

## 📐 16:9 Screen Optimization

Your screen is 16:9 (like 1920x1080, 1280x720, etc.)

**The updated HTML includes:**

```css
/* Ensures proper display on 16:9 screens */
@media screen and (aspect-ratio: 16/9) {
    body {
        width: 100vw;
        height: 100vh;
    }
}
```

**This makes sure:**
- Background covers entire screen
- No black bars on sides
- Content scales properly
- Logo stays in top right

---

## 🎨 Color Values Used

**Background:**
- Primary: #FFC107 (IML Yellow)
- Accent: #FFEB3B (Light Yellow)
- Gradient: #FFD54F to #FFC107

**Text:**
- Headers: #084077 (IML Dark Blue)
- Speaker names: #084077
- Date: #084077
- Time: #E91E63 (Pink accent)

**Cards:**
- Background: White (98% opacity)
- Left border: #FFC107 (8px wide)

---

## ✅ Quick Checklist

### Before Starting:
- [ ] Have Image #1 saved as `iml_background.jpg`
- [ ] Have Image #2 saved as `iml_logo.png`
- [ ] Both images in same folder as HTML file

### For HTML Preview:
- [ ] Open `template_with_assets.html` in browser
- [ ] See background image
- [ ] See logo in top right
- [ ] Check on full screen (F11)

### For SmartSign:
- [ ] Upload both images to Media Library
- [ ] Add background as Layer 1 (bottom)
- [ ] Add logo as top layer
- [ ] Test preview in Template Creator

### For Website:
- [ ] Add CSS to stylesheet
- [ ] Add logo HTML to page
- [ ] Upload images to web server
- [ ] Update image paths in code

---

## 🔧 Troubleshooting

### Background Not Showing

**Problem:** Plain beige/cream background instead of yellow pattern

**Solutions:**

1. **Check image path:**
   ```css
   /* Make sure path is correct */
   background-image: url('iml_background.jpg'); /* Same folder */
   background-image: url('../images/iml_background.jpg'); /* Images folder */
   ```

2. **Check image exists:**
   - Open browser developer tools (F12)
   - Look for 404 errors in Console tab
   - Verify filename matches exactly (case-sensitive)

3. **Use fallback:**
   - The template includes yellow gradient fallback
   - If image doesn't load, you'll see gradient instead

### Logo Not Showing

**Problem:** No logo in top right corner

**Solutions:**

1. **Check image path:**
   ```html
   <img src="iml_logo.png" alt="Institut Mittag-Leffler">
   ```

2. **Check logo format:**
   - Must be PNG or JPG
   - PNG recommended for transparent background

3. **Check Z-index:**
   ```css
   .logo-container {
       z-index: 1000; /* Must be higher than other elements */
   }
   ```

4. **Use fallback text:**
   - Template shows "Institut Mittag-Leffler" if logo doesn't load

### Images Look Stretched

**Problem:** Background or logo appears distorted

**Solutions:**

1. **For background:**
   ```css
   background-size: cover; /* Maintains aspect ratio */
   background-position: center; /* Centers image */
   ```

2. **For logo:**
   ```css
   height: 80px;
   width: auto; /* Maintains aspect ratio */
   ```

### White boxes instead of images

**Problem:** Broken image icons

**Solution:**
- Images not found
- Check file paths
- Verify files uploaded to correct location

---

## 📱 Testing Checklist

### Desktop Browser Test:
- [ ] Background visible and covers screen
- [ ] Logo visible in top right
- [ ] Logo has white background box
- [ ] All text readable over background
- [ ] Cards have yellow left border
- [ ] Layout looks clean

### Full Screen Test (F11):
- [ ] Background fills entire screen
- [ ] No white/black borders
- [ ] Logo stays in top right
- [ ] Text remains readable
- [ ] 16:9 ratio maintained

### SmartSign Screen Test:
- [ ] Background loads
- [ ] Logo displays
- [ ] All elements positioned correctly
- [ ] Data updates from CSV
- [ ] Smooth transitions

---

## 🚀 Quick Start

**Fastest way to see it working:**

1. **Save images:**
   ```
   iml_background.jpg  →  C:\Users\chrwah28.KVA\Development\smartsign\
   iml_logo.png        →  C:\Users\chrwah28.KVA\Development\smartsign\
   ```

2. **Open file:**
   ```
   Double-click: template_with_assets.html
   ```

3. **View full screen:**
   ```
   Press F11 in browser
   ```

**That's it!** You should see:
- ✅ Yellow geometric background
- ✅ IML logo in top right with white box
- ✅ 4 seminar cards
- ✅ Professional layout

---

## 📚 Related Files

| File | Purpose |
|------|---------|
| `template_with_assets.html` | Updated HTML with BG & logo |
| `template_preview.html` | Original preview |
| `docs/TEMPLATE_CONFIGURATION.md` | SmartSign build guide |
| `HTML_PREVIEW_SETUP.md` | Setup instructions |

---

## 💡 Pro Tips

### For Best Results:

1. **Use high-quality images:**
   - Background: 1920x1080 px or higher
   - Logo: 300-400 px height
   - Save as optimized JPG/PNG

2. **Test on actual screen:**
   - Open HTML on the display computer
   - Use full screen mode
   - Check from viewing distance

3. **Keep files together:**
   - HTML file, images, and fonts in same folder
   - Easier to manage and deploy

4. **Use relative paths:**
   ```html
   <!-- Good - works anywhere -->
   <img src="iml_logo.png">

   <!-- Avoid - only works in specific location -->
   <img src="C:\Users\...\iml_logo.png">
   ```

---

## 🎯 Expected Result

**After adding background and logo:**

```
┌────────────────────────────────────────────────────────┐
│  [Yellow geometric background pattern]                │
│                                    ┌──────────────┐   │
│  SEMINARS THIS WEEK                │  [IML Logo]  │   │
│  Institut Mittag-Leffler           │              │   │
│                                    └──────────────┘   │
│  ┌──────────────────────────────────────────────┐    │
│  │ Tue 18 Nov • 09:30-10:30               │    │
│  │ Björn Stinner: Finite element...             │    │
│  │ Speaker: Björn Stinner, Warwick              │    │
│  │ Location: Kuskvillan                         │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  [3 more seminar cards...]                           │
└────────────────────────────────────────────────────────┘
```

---

**Need more help?**
- See: `HTML_PREVIEW_SETUP.md` for detailed setup
- See: `docs/TEMPLATE_CONFIGURATION.md` for SmartSign instructions

**Version:** 1.0
**Screen Ratio:** 16:9
**Resolution:** 1920 x 1080 px (Full HD)
