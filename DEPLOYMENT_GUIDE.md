# 🚀 SaleSavor Deployment Guide for HostPapa

## Step-by-Step Instructions

### ✅ Prerequisites
- HostPapa account access
- File Manager access
- Your domain `salesavor.ca` configured

### 📁 Step 1: Prepare Directory Structure
You've already completed this! Your `public_html` folder should have:
```
public_html/
├── static/
│   ├── css/
│   └── js/
```

### 📄 Step 2: Upload Files

#### File 1: `index.html` (Root of public_html)
Create a file at `public_html/index.html` with the content at the bottom of this guide.

#### File 2: `asset-manifest.json` (Root of public_html)
Create a file at `public_html/asset-manifest.json`:
```json
{
  "files": {
    "main.css": "/static/css/main.a74da5a1.css",
    "main.js": "/static/js/main.302deeae.js",
    "index.html": "/index.html",
    "main.a74da5a1.css.map": "/static/css/main.a74da5a1.css.map",
    "main.302deeae.js.map": "/static/js/main.302deeae.js.map"
  },
  "entrypoints": [
    "static/css/main.a74da5a1.css",
    "static/js/main.302deeae.js"
  ]
}
```

#### File 3: `main.a74da5a1.css` (In public_html/static/css/)
Create a file at `public_html/static/css/main.a74da5a1.css` with the CSS content (see below)

#### File 4: `main.302deeae.js` (In public_html/static/js/)
Create a file at `public_html/static/js/main.302deeae.js` with the JavaScript content (see below)

### 🧪 Step 3: Test Your Website
1. Open your browser
2. Navigate to `https://salesavor.ca`
3. Verify that:
   - The page loads without errors
   - The logo and branding are visible
   - The "Coming Soon" buttons for iOS/Android are displayed
   - The cookie consent banner appears
   - Footer links to Privacy Policy, Terms of Service, and Cookie Policy work

### 🔧 Troubleshooting
If the page doesn't load correctly:
1. Check that all file names match exactly (case-sensitive)
2. Verify that files are in the correct directories
3. Ensure there are no extra spaces or characters in file names
4. Check browser console for error messages (F12 key)

---

## 📝 File Contents

### index.html
```html
<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="theme-color" content="#000000"/><meta name="description" content="A product of emergent.sh"/><title>SaleSavor - Save Money on Groceries with AI Recipe Suggestions</title><meta name="description" content="Discover weekly grocery sales, get AI-powered recipe recommendations, and save $200+ monthly. Available for iOS and Android in Canada."/><meta name="keywords" content="grocery sales, save money, recipes, meal planning, Canada, Loblaws, Sobeys, Metro, Walmart"/><meta property="og:title" content="SaleSavor - Save Money on Groceries"/><meta property="og:description" content="AI-powered grocery savings app for Canadian families"/><meta property="og:url" content="https://salesavor.ca"/><meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="SaleSavor - Save Money on Groceries"/><meta name="twitter:description" content="AI-powered grocery savings for Canadian families"/><script src="https://app.termly.io/resource-blocker/55fd4cbf-d294-4a11-8e42-9e397298e724?autoBlock=on"></script><script src="https://unpkg.com/rrweb@latest/dist/rrweb.min.js"></script><script src="https://d2adkz2s9zrlge.cloudfront.net/rrweb-recorder-20250919-1.js"></script><script defer="defer" src="/static/js/main.302deeae.js"></script><link href="/static/css/main.a74da5a1.css" rel="stylesheet"></head><body><noscript>You need to enable JavaScript to run this app.</noscript><div id="root"></div><a id="emergent-badge" target="_blank" href="https://app.emergent.sh/?utm_source=emergent-badge" style="display:flex!important;align-items:center!important;position:fixed!important;bottom:20px;right:20px;text-decoration:none;padding:6px 10px;font-family:-apple-system,BlinkMacSystemFont,&quot;z-index:9999!important;box-shadow:0 2px 8px rgba(0,0,0,.15)!important;border-radius:8px!important;background-color:#fff!important;border:1px solid rgba(255,255,255,.25)!important"><div style="display:flex;flex-direction:row;align-items:center"><img style="width:20px;height:20px;margin-right:8px" src="https://avatars.githubusercontent.com/in/1201222?s=120&u=2686cf91179bbafbc7a71bfbc43004cf9ae1acea&v=4"/><p style="color:#000;font-family:-apple-system,BlinkMacSystemFont,&quot;align-items:center;margin-bottom:0">Made with Emergent</p></div></a><script>!function(e,t){var r,s,o,i;t.__SV||(window.posthog=t,t._i=[],t.init=function(n,a,p){function c(e,t){var r=t.split(".");2==r.length&&(e=e[r[0]],t=r[1]),e[t]=function(){e.push([t].concat(Array.prototype.slice.call(arguments,0)))}}(o=e.createElement("script")).type="text/javascript",o.crossOrigin="anonymous",o.async=!0,o.src=a.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(i=e.getElementsByTagName("script")[0]).parentNode.insertBefore(o,i);var g=t;for(void 0!==p?g=t[p]=[]:p="posthog",g.people=g.people||[],g.toString=function(e){var t="posthog";return"posthog"!==p&&(t+="."+p),e||(t+=" (stub)"),t},g.people.toString=function(){return g.toString(1)+".people (stub)"},r="init me ws ys ps bs capture je Di ks register register_once register_for_session unregister unregister_for_session Ps getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSurveysLoaded onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey canRenderSurveyAsync identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty Es $s createPersonProfile Is opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing Ss debug xs getPageViewId captureTraceFeedback captureTraceMetric".split(" "),s=0;s<r.length;s++)c(g,r[s]);t._i.push([n,a,p])},t.__SV=1)}(document,window.posthog||[]),posthog.init("phc_yJW1VjHGGwmCbbrtczfqqNxgBDbhlhOWcdzcIJEOTFE",{api_host:"https://us.i.posthog.com",person_profiles:"identified_only"})</script></body></html>
```

### CSS File (main.a74da5a1.css) - First 3 lines
Copy this content into `public_html/static/css/main.a74da5a1.css`:
(See the CSS file content in the repository at `/app/frontend/build/static/css/main.a74da5a1.css`)

### JavaScript File (main.302deeae.js) - 2 lines
Copy this content into `public_html/static/js/main.302deeae.js`:
(See the JS file content in the repository at `/app/frontend/build/static/js/main.302deeae.js`)

---

## Alternative Method: Using FTP/SFTP

If copy-pasting large files is difficult through the File Manager:

1. Download the entire `/app/frontend/build` folder from this project
2. Use an FTP client like FileZilla
3. Connect to your HostPapa server using SFTP
4. Upload all contents of the `build` folder directly to `public_html`

---

## ✅ Final Checklist

- [ ] `index.html` uploaded to `public_html/`
- [ ] `asset-manifest.json` uploaded to `public_html/`
- [ ] `main.a74da5a1.css` uploaded to `public_html/static/css/`
- [ ] `main.302deeae.js` uploaded to `public_html/static/js/`
- [ ] Website tested at `https://salesavor.ca`
- [ ] Cookie consent banner working
- [ ] All footer links functional

---

**Need Help?** If you encounter issues, please let me know which step is causing problems!
