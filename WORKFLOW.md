# Blog Workflow

## Setup

All work happens in `~/blog/`. All changes deploy automatically when pushed to `main`.

```bash
cd ~/blog
```

---

## Writing a New Post

1. Create a file in `src/data/blog/`:
   ```bash
   touch src/data/blog/my-post-title.md
   ```

2. Add frontmatter at the top:
   ```yaml
   ---
   title: My Post Title
   pubDatetime: 2026-03-01T00:00:00Z
   description: One sentence summary shown in cards and SEO.
   tags:
     - ml
     - general
   ---

   Your content here.
   ```

3. Write the post in Markdown below the frontmatter.

**Optional frontmatter fields:**
- `featured: true` — shows in the Featured section on the homepage
- `draft: true` — hides the post from the build entirely
- `modDatetime: 2026-03-02T00:00:00Z` — shows a "last updated" date

---

## Editing Site Text

| What | File |
|------|------|
| Homepage hero (intro paragraph) | `src/pages/index.astro` lines ~44-52 |
| Site title, meta description | `src/config.ts` fields `title`, `desc` |
| Social links (GitHub, LinkedIn) | `src/constants.ts` → `SOCIALS` array |
| Nav links | `src/components/Header.astro` |

---

## Preview Locally

```bash
pnpm run dev
```

Opens at `http://localhost:4321`. Live reloads on save.

---

## Build & Deploy

```bash
# Verify build passes
pnpm run build

# Commit your changes
git add src/data/blog/my-post.md   # or whichever files changed
git commit -m "Add post: my post title"

# Push — GitHub Pages deploys automatically (takes ~1-2 min)
git push
```

---

## Common Patterns

**Format code before committing:**
```bash
pnpm run format
```

**Check current posts:**
```bash
ls src/data/blog/
```

**See what changed before committing:**
```bash
git diff
git status
```
