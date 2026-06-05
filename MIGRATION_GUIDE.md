# Migration Guide : Drag-Drop Deploys → GitHub + Auto-Deploy

This is Jeff's step-by-step guide for moving the atlas from "drag-drop deploy/ to Netlify" to "push to GitHub and Netlify auto-deploys." Mirrors what you already did for firstlightfoundry.

**Estimated time : 30-45 minutes.**

---

## Before you start

You need :

- A GitHub account (you have one : @JeffreySchaller)
- Your existing Netlify project (`theancientatlas.com`)
- GitHub Desktop installed (or terminal Git if you prefer)
- The current `deploy/` folder of the atlas project

You'll keep your existing Netlify deploy running throughout. There's no downtime risk : Netlify will continue serving the last drag-drop deploy until the new GitHub-connected build takes over.

---

## Step 1 : Create the GitHub repo

1. Go to **github.com/new**
2. Settings :
   - **Repository name** : `ancient-atlas` (lowercase, hyphenated — matches the eventual contributor experience)
   - **Description** : `A hand-curated map of the world's most significant ancient sites — source for theancientatlas.com`
   - **Public** ✅ (per our prior conversation — public for the community-effects)
   - **Add a README** : ❌ (we'll add our own)
   - **Add .gitignore** : ❌ (we'll add our own)
   - **License** : MIT (or leave for now and add later)
3. Click **Create repository**

Note the URL : `github.com/JeffreySchaller/ancient-atlas`

---

## Step 2 : Set up the local repo structure

In Finder, navigate to `~/iCloud Drive/Projects/ancient-atlas/`.

**Make a new working folder** somewhere outside iCloud (e.g. `~/Code/ancient-atlas/`) and copy these in :

```
~/Code/ancient-atlas/
├── public/                          ← create this folder
│   ├── index.html                   ← copy from deploy/
│   ├── contact.html                 ← copy from deploy/
│   ├── library/                     ← copy whole folder from deploy/library/
│   ├── og-image.png                 ← copy from deploy/
│   ├── apple-touch-icon.png         ← copy from deploy/
│   ├── favicon-32.png               ← copy from deploy/
│   └── icon-256.png                 ← copy from deploy/
├── scripts/                         ← create this folder
│   ├── audit-videos.py              ← copy from project root
│   └── generate-og.py               ← copy from project root
├── docs/                            ← copy this folder from github-migration/
│   └── AUTOMATION_ROADMAP.md
├── .github/                         ← copy this folder from github-migration/
├── README.md                        ← copy from github-migration/
├── CONTRIBUTING.md                  ← copy from github-migration/
├── .gitignore                       ← copy from github-migration/
└── LICENSE                          ← copy from github-migration/
```

The `github-migration/` folder I prepared has all the docs and config files ready to drag in.

**Why outside iCloud :** Git and iCloud sync conflict in unpredictable ways. Code should live outside iCloud-managed folders. Your existing iCloud project becomes the "old version" that you can archive or delete after this works.

---

## Step 3 : Push the initial commit

### Using GitHub Desktop (recommended) :

1. Open GitHub Desktop
2. **File → Add local repository...** → choose `~/Code/ancient-atlas/`
3. GitHub Desktop will say "this folder is not a Git repository — would you like to create one?" → **Yes**
4. **Repository → Publish repository** → confirms the name `ancient-atlas` and pushes to GitHub
5. After push, you should see all your files at `github.com/JeffreySchaller/ancient-atlas`

### Using terminal Git :

```bash
cd ~/Code/ancient-atlas/
git init
git add .
git commit -m "Initial commit : the atlas as it exists today"
git branch -M main
git remote add origin https://github.com/JeffreySchaller/ancient-atlas.git
git push -u origin main
```

After this step, the repo is live on GitHub with the current atlas content. **Netlify is not yet connected** — your live site is still serving the last drag-drop deploy.

---

## Step 4 : Connect Netlify to the repo

1. Go to **app.netlify.com** → click on your **theancientatlas.com** project
2. **Site configuration → Build & deploy → Continuous deployment**
3. Scroll to the section that says something like "Build settings" or "Continuous deployment"
4. Click **Link site to Git** (or similar wording — Netlify's UI changes)
5. Choose **GitHub** as the provider
6. Authorize Netlify if it's your first time
7. Pick the repository : `JeffreySchaller/ancient-atlas`
8. **Build settings** :
   - **Branch to deploy** : `main`
   - **Build command** : (leave blank for now — we have no build step yet; the HTML is already final)
   - **Publish directory** : `public`
9. Click **Deploy site**

Netlify will pull the repo, find the `public/` folder, and deploy it. Should take 30-60 seconds.

**Verify** : visit `theancientatlas.com` and confirm everything still works. Should be identical to before, because the content is identical.

---

## Step 5 : Confirm the auto-deploy works

To prove the new pipeline works :

1. Edit any file in the repo (e.g. add a typo to `README.md`)
2. Commit and push
3. Watch the Netlify dashboard — within 60 seconds, a new deploy should appear
4. After it goes green, the change is live
5. Revert the typo, commit, and push again — confirm the second deploy also works

This is the moment the architecture flips. From now on, the atlas is updated by pushing to GitHub. No more drag-drop.

---

## Step 6 : Archive the old workflow

In your iCloud project (the original `~/iCloud Drive/Projects/ancient-atlas/`) :

- **Don't delete it yet** — keep it as a backup until the GitHub version has run smoothly for a week
- **Stop editing it** — all future edits go to the new `~/Code/ancient-atlas/` location
- **Note in your CLAUDE.md or memory** : "atlas source is now at ~/Code/ancient-atlas/, pushes to GitHub auto-deploy"

After a week of smooth GitHub deploys, you can archive the iCloud folder (zip + move to backup) and delete the local copy.

---

## What to do if something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Netlify deploy fails with "publish directory not found" | `public/` folder doesn't exist in repo, or path is wrong | Confirm `public/` exists at repo root and contains `index.html`. Check Netlify build settings → publish directory. |
| Site loads but missing CSS / blank | OG image or favicon paths are absolute (`/og-image.png`) instead of relative | Check `index.html` for `/library/...` → should be `library/...` (we already fixed this). |
| Netlify Forms (contact page) stops working | Form detection runs at build time; new build cleared the form registry | Re-add the email recipient in Netlify dashboard → Forms → atlas-contact → Notifications |
| Deploy succeeds but site shows old version | Browser cached the old deploy | Hard refresh (Cmd+Shift+R on macOS) |

If something else breaks, the rollback is one click : Netlify Deploys → find the last good deploy → **Publish deploy**. Site reverts in 30 seconds.

---

## What's next after this works

You've completed **Phase 1 : GitHub foundation** from the [AUTOMATION_ROADMAP](docs/AUTOMATION_ROADMAP.md).

Next milestones :

1. **Extract the JSON files** : pull `SITES`, `VIDEOS`, `CREATORS` out of `index.html` into `data/*.json`. Write `scripts/build.py` to reassemble. This unlocks contributor PRs against clean structured data.
2. **Phase 2 : Contributor experience** : build the `/contribute.html` page and the CI checks.
3. **Phase 3 : Evergreen** : daily cron that polls creator RSS feeds.
4. **Phase 4 : Mission infrastructure** : assignment desk, "Filmed for the Atlas" badge, contributor leaderboard.

I'll walk you through each phase when you're ready.

For now, the goal is just to get the foundation in place. Push to GitHub, connect Netlify, confirm auto-deploy. The rest builds on this.

---

## Questions while you migrate

Ping me with any error message or screenshot. The migration is the moment to be cautious. Once GitHub auto-deploy works, the floor is solid for everything else.

Good luck. This is the upgrade.
