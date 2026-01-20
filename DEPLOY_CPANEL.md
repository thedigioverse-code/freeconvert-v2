# How to Deploy to cPanel (File Manager)

I have compressed your entire site into a single file named `freeconvert-deploy.zip` located in `C:\Users\Admin\.gemini\antigravity\scratch\`.

## Step 1: Prepare the Server
1.  Log in to your cPanel.
2.  Open **File Manager**.
3.  Double-click on **public_html** (or the folder for your domain).
4.  **Important:** If there are existing files there (like `default.php` or old site files), delete them so your new site is clean.

## Step 2: Upload
1.  Click the **Upload** button in the top toolbar.
2.  Drag and drop the `freeconvert-deploy.zip` file from your computer into the upload area.
3.  Wait for the bar to turn green (100%).
4.  Click "Go Back to..."

## Step 3: Extract
1.  You should see `freeconvert-deploy.zip` in your `public_html` folder.
2.  **Right-click** on the zip file.
3.  Select **Extract**.
4.  Click **Extract Files**.
5.  Once done, you will see all your folders (`tools`, `blog`, `assets`) appear.

## Step 4: Cleanup
1.  Right-click `freeconvert-deploy.zip` and **Delete** it (you don't need it anymore).
2.  Visit your website URL to see it live!
