# GitHub Publish

Create the remote only after confirming the owner/name to use.

Recommended repository name:

```text
rimfridge-wall-access-fix
```

Local publish flow:

```powershell
git status --short
git remote add origin https://github.com/<owner>/rimfridge-wall-access-fix.git
git push -u origin main
```

Do not claim the GitHub remote exists until `git remote -v` and the first push both succeed.
