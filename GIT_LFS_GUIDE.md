# Git Large File Storage (LFS) Guide

This guide explains how to use Git LFS for handling large files in your repository.

## 🎯 What is Git LFS?

Git Large File Storage (LFS) is an extension that replaces large files with text pointers inside Git, while storing the actual file contents on a remote server like GitHub.

### Why Use Git LFS?

- **GitHub File Size Limit**: GitHub has a 100MB file size limit per file
- **Your Issue**: `order_items.csv` is 102MB, exceeding the limit
- **Solution**: Git LFS stores large files separately

---

## 🚀 Initial Setup (Already Done!)

### 1. Install Git LFS

```bash
# On macOS
brew install git-lfs

# On Windows
# Download from: https://git-lfs.github.com/

# On Linux (Ubuntu/Debian)
sudo apt-get install git-lfs
```

### 2. Initialize Git LFS

```bash
git lfs install
```

This only needs to be done once per user account.

### 3. Track Large Files

```bash
# Track specific file types
git lfs track "data/nourishbox/*.csv"

# Or track all CSV files in repository
git lfs track "*.csv"

# This creates/updates .gitattributes file
```

### 4. Add and Commit

```bash
# Add .gitattributes (important!)
git add .gitattributes

# Add your large files
git add data/nourishbox/*.csv

# Commit
git commit -m "Add large CSV files with Git LFS"

# Push to GitHub
git push origin main
```

---

## 📋 Current Configuration

Your repository is configured to track:

```
data/nourishbox/*.csv
```

This is stored in the [.gitattributes](.gitattributes) file.

### Files Currently Tracked by LFS

| File | Size |
|------|------|
| order_items.csv | 102 MB ✅ |
| orders.csv | 6.1 MB |
| reviews.csv | 4.5 MB |
| customers.csv | 515 KB |
| subscriptions.csv | 387 KB |
| customer_preferences.csv | 262 KB |
| churn_events.csv | 184 KB |
| marketing_campaigns.csv | 15 KB |
| product_catalog.csv | 3.4 KB |

**Total LFS Storage**: ~119 MB

---

## 🔄 Common Operations

### Check Which Files are Tracked by LFS

```bash
git lfs ls-files
```

### Check LFS Status

```bash
git lfs status
```

### See What File Types are Tracked

```bash
cat .gitattributes
```

Should show:
```
data/nourishbox/*.csv filter=lfs diff=lfs merge=lfs -text
```

### Track Additional File Types

```bash
# Track all PNG files
git lfs track "*.png"

# Track all PBIX files (Power BI)
git lfs track "*.pbix"

# Track files in specific directory
git lfs track "data/**/*.parquet"
```

---

## 🛠️ Troubleshooting

### Problem: File Already Committed Without LFS

If you already committed a large file without LFS:

```bash
# 1. Remove file from Git cache (not from disk)
git rm --cached path/to/large-file.csv

# 2. Track it with LFS
git lfs track "path/to/large-file.csv"

# 3. Add .gitattributes
git add .gitattributes

# 4. Re-add the file
git add path/to/large-file.csv

# 5. Amend the commit
git commit --amend --no-edit

# 6. Force push (if already pushed)
git push --force origin main
```

### Problem: "This exceeds GitHub's file size limit"

This means the file was committed without LFS. Follow steps above.

### Problem: LFS Upload is Slow

LFS uploads can be slower than regular Git. For 119MB:
- Expected time: 1-5 minutes (depending on connection)
- Progress shown: "Uploading LFS objects: X% (Y/Z), XX MB | X.X MB/s"

### Problem: Cloning Takes Forever

When others clone your repository:

```bash
# Clone without LFS files (faster)
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/username/repo.git

# Then pull LFS files when needed
git lfs pull
```

---

## 📊 GitHub LFS Quotas

### Free Account (Personal)
- **Storage**: 1 GB free
- **Bandwidth**: 1 GB/month free
- **Current Usage**: ~119 MB (12% of free storage)

### If You Exceed Limits

**Options:**
1. **Purchase data packs**: $5/month for 50 GB storage + 50 GB bandwidth
2. **Use Git LFS on other platforms**: GitLab offers 10 GB free
3. **Host large files elsewhere**: Cloud storage, release assets, etc.

### Check Your Usage

Go to: https://github.com/settings/billing

---

## 🔒 .gitattributes File

The `.gitattributes` file tells Git which files should use LFS:

```
data/nourishbox/*.csv filter=lfs diff=lfs merge=lfs -text
```

**Important**: Always commit `.gitattributes` to your repository!

---

## 🎓 Best Practices

### 1. Track LFS Files Early
Set up LFS before committing large files, not after.

### 2. Be Selective
Don't track small files with LFS - only files >50MB or those approaching 100MB.

### 3. Keep .gitattributes in Repo
Always commit this file so collaborators automatically use LFS.

### 4. Use .gitignore for Generated Files
If files can be regenerated, consider adding them to `.gitignore` instead:

```gitignore
# Don't commit large generated files
data/nourishbox/*.csv

# But keep the generation script
!src/generate_nourishbox_data.py
```

### 5. Document LFS Usage
Add a note to your README that the project uses LFS:

```markdown
## Prerequisites

This project uses Git LFS for large data files. Install it first:

\`\`\`bash
brew install git-lfs  # macOS
git lfs install
\`\`\`
```

---

## 🚫 Alternative: Don't Commit Large Data Files

### Option 1: Use .gitignore

Instead of committing large CSV files, you could:

1. **Add to .gitignore**:
```gitignore
# Ignore generated data
data/nourishbox/*.csv
```

2. **Commit the generator**:
```bash
git add src/generate_nourishbox_data.py
```

3. **In README**, instruct users:
```markdown
## Generate Data

\`\`\`bash
python src/generate_nourishbox_data.py
\`\`\`
```

**Pros**: No LFS needed, smaller repository
**Cons**: Users must generate data themselves

### Option 2: Release Assets

Upload large files as GitHub Release assets:

1. Create a release: https://github.com/username/repo/releases/new
2. Upload CSV files as assets
3. In README, link to release:
```markdown
Download data: [Release v1.0](https://github.com/username/repo/releases/tag/v1.0)
```

**Pros**: No LFS quota, no repository bloat
**Cons**: Manual upload process

### Option 3: External Storage

Host files on:
- Google Drive
- Dropbox
- AWS S3
- Kaggle Datasets (recommended for data projects!)

---

## 📝 Summary

✅ **Git LFS is now set up** for your repository
✅ **All CSV files in data/nourishbox/** are tracked by LFS
✅ **Successfully pushed** to GitHub (119 MB uploaded)
✅ **.gitattributes** is committed to preserve settings

### Next Steps:

1. ✅ Your repository is now live at: https://github.com/greg-bi-wizz/nouri
2. Anyone cloning needs Git LFS installed: `git lfs install`
3. Monitor your LFS storage at: https://github.com/settings/billing

---

## 📚 Additional Resources

- **Git LFS Homepage**: https://git-lfs.github.com/
- **GitHub LFS Documentation**: https://docs.github.com/en/repositories/working-with-files/managing-large-files
- **LFS Tutorial**: https://www.atlassian.com/git/tutorials/git-lfs

---

**Note**: This guide reflects your current setup as of January 12, 2026.
