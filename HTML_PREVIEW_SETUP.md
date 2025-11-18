# HTML Preview Setup Instructions

**View your SmartSign template design in a web browser**

---

## 📋 What You Have

I've created an **HTML preview** that shows exactly how your SmartSign seminar display will look with IML branding.

**Files created:**
- `template_preview.html` - Interactive HTML preview
- `docs/TEMPLATE_CONFIGURATION.md` - Complete SmartSign configuration guide (32 pages)

---

## 🎨 Design Features

Your template includes:
- ✅ **IML yellow geometric background** (from Image #1)
- ✅ **IML logo in top right** (from Image #2)
- ✅ **DINPro Regular font** throughout
- ✅ **IML dark blue (#084077)** for titles and main text
- ✅ **Professional card layout** with yellow accent borders
- ✅ **Clean, readable design** for digital screens

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Save Your Images

You need to save the two images you provided:

**Image #1 - Background (Yellow geometric pattern):**
- Save as: `iml_background.jpg`
- Location: `C:\Users\chrwah28.KVA\Development\smartsign\`

**Image #2 - Logo:**
- Save as: `iml_logo.png`
- Location: `C:\Users\chrwah28.KVA\Development\smartsign\`

### Step 2: Add DINPro Font (Optional)

If you have the DINPro-Regular.otf font file:
- Place it in: `C:\Users\chrwah28.KVA\Development\smartsign\`

**Note:** If you don't have the font, the preview will use Arial as fallback (still looks good!)

### Step 3: Open the Preview

**Double-click** `template_preview.html`

It will open in your default web browser showing the complete design!

---

## 📂 File Structure

```
C:\Users\chrwah28.KVA\Development\smartsign\
│
├── template_preview.html          ← Open this in browser
├── iml_background.jpg             ← Save Image #1 here
├── iml_logo.png                   ← Save Image #2 here
└── DINPro-Regular.otf             ← (Optional) Font file
```

---

## 🖼️ What You'll See

When you open `template_preview.html`, you'll see:

1. **Beautiful yellow geometric background** (IML branding)
2. **IML logo in top right corner**
3. **"SEMINARS THIS WEEK" header** in IML dark blue
4. **4 seminar cards** showing:
   - Date and time (colored for easy reading)
   - Seminar title (bold, IML blue)
   - Speaker name and institution
   - Location/room

**Example seminars** are populated from your current CSV data!

---

## 🎯 Use Cases for HTML Preview

### 1. **Visual Reference**
Use this while building the template in SmartSign Template Creator:
- Match colors exactly (#084077 for text)
- Match font sizes
- Match spacing and layout
- Match element positions

### 2. **Client Approval**
Show this to stakeholders:
- Open in browser
- Present on screen or share screenshot
- Get design approval before SmartSign config
- Make quick design changes if needed

### 3. **Documentation**
Keep as reference:
- Shows final intended design
- Helps future maintainers understand layout
- Can be used for training

---

## ⚙️ Customizing the Preview

The HTML file is fully editable! You can:

### Change Colors

Find this section in the `<style>` tag:

```css
/* IML Dark Blue for titles */
.title {
    color: #084077;
}
```

Change `#084077` to any color you want!

### Change Font Sizes

```css
.title {
    font-size: 42px;  /* Make larger or smaller */
}
```

### Change Layout

Modify the positioning values:

```css
.logo-container {
    top: 40px;    /* Distance from top */
    right: 60px;  /* Distance from right */
}
```

### Add More Seminars

Find the `<div class="seminar">` sections and duplicate them!

---

## 🔄 Dynamic Data Preview

The HTML preview shows **static sample data** from your current seminars.

**To update with new data:**
1. Run `filter_seminarier.py` to get latest seminars
2. Open `seminarier.csv`
3. Copy seminar data
4. Paste into HTML (replace existing seminar divs)

**Or:** Just keep as design reference - SmartSign will use live CSV data!

---

## 📱 Testing on Different Devices

### Desktop Browser
- **Best for**: Detailed review
- **How**: Double-click `template_preview.html`
- **Zoom**: 100% to see actual size

### Large Screen/TV
- **Best for**: Real-world preview
- **How**: Open on computer connected to TV
- **Resolution**: Ensure TV is 1920x1080 (Full HD)

### Tablet
- **Best for**: Portable demos
- **How**: Email file to yourself, open on tablet
- **Note**: Will scale to fit tablet screen

---

## 🎨 Color Reference

**Your color palette:**

| Color | Hex Code | Usage |
|-------|----------|-------|
| **IML Dark Blue** | #084077 | Titles, headers, speaker names |
| **IML Yellow** | #FFC107 | Card accent borders |
| **Date Blue** | #1976D2 | Date text |
| **Time Pink** | #E91E63 | Time text |
| **White** | #FFFFFF | Card backgrounds (97% opacity) |

All colors are in the HTML file and can be changed!

---

## 📐 Layout Specifications

**Screen:** 1920 x 1080 px (Full HD Landscape)
**Margins:** 80px safe area on all sides
**Cards visible:** 4 seminars at once
**Card spacing:** 25px gap between cards
**Font:** DINPro Regular (fallback: Arial)
**Card borders:** 8px yellow left border

**These exact specs are in:**
`docs/TEMPLATE_CONFIGURATION.md` for recreating in SmartSign

---

## ✅ Checklist

Before using in SmartSign:
- [ ] HTML preview opened in browser
- [ ] Design looks good
- [ ] Colors are correct (IML blue #084077)
- [ ] Images display properly
- [ ] Font looks professional
- [ ] Layout matches requirements
- [ ] Stakeholders approve design

After approval:
- [ ] Use `docs/TEMPLATE_CONFIGURATION.md` to build in SmartSign
- [ ] Follow layer-by-layer instructions
- [ ] Match all measurements exactly
- [ ] Test with live CSV data
- [ ] Deploy to screen

---

## 🔧 Troubleshooting

### Images Don't Show

**Problem:** Broken image icons in preview

**Solution:**
1. Check images are saved in same folder as HTML file
2. Verify filenames match exactly:
   - `iml_background.jpg` (lowercase)
   - `iml_logo.png` (lowercase)
3. Try refreshing browser (Ctrl+R or Cmd+R)

### Font Looks Wrong

**Problem:** Text doesn't look like DINPro

**Solution:**
- This is OK! HTML uses Arial as fallback
- In SmartSign, you'll upload DINPro font separately
- Design/layout is what matters for preview

### Layout Looks Cramped

**Problem:** Elements overlapping or too close

**Solution:**
- Make browser full screen (F11)
- Zoom to 100% (Ctrl+0 or Cmd+0)
- Check your screen resolution (should be 1920x1080 or higher)

### Colors Look Different

**Problem:** Colors don't match exactly

**Solution:**
- Different screens show colors differently
- Verify hex codes in HTML match specifications
- Use color picker tool to confirm #084077 for titles

---

## 📚 Next Steps

### After Reviewing Preview:

1. **If design looks good:**
   - Proceed to SmartSign Template Creator
   - Follow `docs/TEMPLATE_CONFIGURATION.md` step-by-step
   - Use HTML preview as visual reference

2. **If changes needed:**
   - Edit `template_preview.html` directly
   - Test changes in browser
   - Document changes for SmartSign config

3. **Share with team:**
   - Email HTML file + images to stakeholders
   - Get approval before SmartSign work
   - Use as training/documentation

---

## 🎓 Advanced: Browser Developer Tools

Want to experiment with the design?

**Open Developer Tools:**
- Chrome/Edge: Press F12
- Firefox: Press F12
- Safari: Cmd+Option+I

**What you can do:**
- Edit CSS live
- Change colors instantly
- Adjust spacing
- Test different layouts
- Take screenshots

**Changes won't be saved** - but great for testing ideas!

---

## 📄 Related Files

| File | Purpose |
|------|---------|
| `template_preview.html` | Interactive HTML preview (this) |
| `docs/TEMPLATE_CONFIGURATION.md` | SmartSign build guide (32 pages) |
| `docs/SMARTSIGN_CONFIG.md` | General SmartSign CMS guide |
| `seminarier.csv` | Live seminar data |
| `filter_seminarier.py` | Data filtering script |

---

## 🆘 Need Help?

**HTML/CSS Questions:**
- Edit the HTML file in any text editor
- See comments in the code for guidance
- Google: "CSS flexbox", "CSS colors", etc.

**SmartSign Questions:**
- See: `docs/TEMPLATE_CONFIGURATION.md`
- See: `docs/SMARTSIGN_CONFIG.md`
- SmartSign Support: support@smartsign.com

**Design Questions:**
- This preview is fully customizable
- All measurements in `docs/TEMPLATE_CONFIGURATION.md`
- Contact: IML IT Team (it@iml.se)

---

## 🎉 Summary

**You now have:**
1. ✅ Beautiful HTML preview with IML branding
2. ✅ Complete SmartSign configuration guide
3. ✅ Ready to build in SmartSign Template Creator
4. ✅ All measurements, colors, and positions documented

**To use:**
1. Save your two images (background + logo)
2. Open `template_preview.html` in browser
3. Review and approve design
4. Build in SmartSign using configuration guide

**That's it!** 🚀

---

**Version:** 1.0
**Last Updated:** 2025-11-17
**Preview Resolution:** 1920 x 1080 px
**Font:** DINPro Regular (IML brand font)
