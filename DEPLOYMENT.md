# How to Deploy freeconvert.cloud to GitHub Pages

Follow these exact steps to get your site live.

## Step 1: Create the Repository on GitHub
1.  Log in to your [GitHub account](https://github.com/).
2.  Click the **+** icon in the top-right corner and select **New repository**.
3.  **Repository name**: Enter a name (e.g., `freeconvert-v2` or `tools-site`).
4.  **Visibility**: Choose **Public** (required for free GitHub Pages) or **Private** (if you have Pro).
5.  **Initialize**: Do **NOT** check "Add a README", "Add .gitignore", or "Choose a license". Keep it completely empty.
6.  Click **Create repository**.

## Step 2: Push Your Code
You should see a screen with the title "…or push an existing repository from the command line".
1.  Copy the URL of your new repo (e.g., `https://github.com/YOUR_USERNAME/freeconvert-v2.git`).
2.  Open your terminal/command prompt to this project folder:
    `C:\Users\Admin\.gemini\antigravity\scratch\freeconvert-v2`
3.  Run these commands (replace the URL with yours):

```bash
git remote add origin https://github.com/YOUR_USERNAME/freeconvert-v2.git
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages
1.  Go back to your repository page on GitHub.
2.  Click **Settings** (top tab).
3.  On the left sidebar, click **Pages**.
4.  Under **Build and deployment** > **Source**, ensure "Deploy from a branch" is selected.
5.  Under **Branch**, select `main` and ensure the folder is `/ (root)`.
6.  Click **Save**.

## Step 4: Verify
1.  Wait about 1-2 minutes.
2.  Refresh the Pages settings page.
3.  You will see a banner: "Your site is live at..." followed by the URL (usually `https://username.github.io/repo-name/`).
4.  Click that link to see your deployed site!
