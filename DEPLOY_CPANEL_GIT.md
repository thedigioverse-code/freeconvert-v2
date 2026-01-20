# How to Deploy using cPanel Git Version Control

This method automatically pulls your code from GitHub directly to your server.

## Part 1: Push Code to GitHub (Do this on your PC)
You need to get your code onto GitHub first so cPanel can find it.
1.  Create a **new repository** on GitHub (empty, no readme).
2.  Run these commands in your project folder terminal:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/freeconvert-v2.git
    git branch -M main
    git push -u origin main
    ```

## Part 2: Connect cPanel to GitHub
1.  Log in to **cPanel**.
2.  Find and click **Git™ Version Control** (under "Files").
3.  Click the **Create** button.
4.  Fill in the details:
    *   **Clone URL**: Paste your GitHub URL (e.g., `https://github.com/YOUR_USERNAME/freeconvert-v2.git`).
    *   **Repository Path**: Enter `public_html` (WARNING: This folder must be empty! Delete existing files in File Manager first).
    *   **Repository Name**: Leave as default (e.g., `freeconvert-v2`).
5.  Click **Create**.

## Part 3: Deploy HEAD (Update Site)
1.  Once created, click **Manage** next to your repo in the list.
2.  Click the **Pull or Deploy** tab.
3.  Click **Update from Remote** to pull the latest code.
4.  Click **Deploy HEAD Commit** (if available) to force files into place.

Your site is now live and synced with GitHub!
