# The Correct Way to Use Git (Local PC -> GitHub -> cPanel)

You saw the error earlier because you ran the commands on the **cPanel Server** (which is empty).
You need to run the commands **on your Computer** (where the code is), to push it to GitHub.

## Step 1: Push Code from YOUR Computer
1.  Open **PowerShell** or **Command Prompt** on your Windows PC.
2.  Copy and paste this command to go to the folder where I built your site:
    ```powershell
    cd "C:\Users\Admin\.gemini\antigravity\scratch\freeconvert-v2"
    ```
3.  Now, connect your GitHub repository:
    *(Replace with your actual URL)*
    ```powershell
    git remote add origin https://github.com/YOUR_USERNAME/freeconvert-v2.git
    ```
4.  Push the code:
    ```powershell
    git branch -M main
    git push -u origin main
    ```
    *(A window will pop up asking you to log in to GitHub. Sign in.)*

## Step 2: Pull Code to cPanel
Now that the code is on GitHub, cPanel can see it.

1.  Go to **cPanel** -> **Git™ Version Control**.
2.  Find your repository list.
3.  Click **Manage** (button on the right).
4.  Click the **Pull or Deploy** tab.
5.  Click **Update from Remote**.
6.  Click **Deploy HEAD Commit**.

## How to Update the Site in the Future
When you want to make changes later:
1.  Edit files on your computer.
2.  Run these commands in PowerShell:
    ```powershell
    git add .
    git commit -m "Update changes"
    git push
    ```
3.  Go to cPanel and click **Update from Remote**.
