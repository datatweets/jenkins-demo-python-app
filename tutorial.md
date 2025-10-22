# Jenkins + GitHub Integration Tutorial

**Assumption:** You already have Jenkins running on Google Colab with ngrok

---

## Step 1: Get Your ngrok URL

From your Colab notebook, find your Jenkins ngrok URL. It looks like:

```text
https://delores-lordlier-vania.ngrok-free.dev
```

---

## Step 2: Create GitHub Personal Access Token

1. Go to GitHub → Click your **profile** (top right) → **Settings**
2. Click **"Developer settings"** → **"Personal access tokens"** → **"Tokens (classic)"**
3. Click **"Generate new token (classic)"**
4. Fill in:
   - **Note:** `Jenkins-Colab-Token`
   - **Expiration:** `90 days`
   - **Scopes:** Check `repo` and `admin:repo_hook`
5. Click **"Generate token"**
6. **Copy the token** (save it somewhere safe!)

---

## Step 3: Create Jenkins Pipeline Job

1. Go to your Jenkins URL: `https://YOUR_NGROK_URL/`
2. Click **"New Item"**
3. Enter **Job name:** `jenkins-demo-python-app`
4. Select **"Pipeline"** → Click **"OK"**

---

## Step 4: Enable Job Parameters

**This step is essential!**

1. In the job configuration page, scroll down
2. Check the box: **"This project is parameterized"**
3. Click **"Add Parameter"** → Select **"String Parameter"**
   - **Name:** `BRANCH`
   - **Default Value:** `main`
4. Click **"Add Parameter"** → Select **"Choice Parameter"**
   - **Name:** `ENVIRONMENT`
   - **Choices:**

     ```text
     dev
     staging
     prod
     ```

---

## Step 5: Configure Pipeline Job

In the same configuration page:

1. Scroll to **"Pipeline"** section
2. For **"Definition"**, select **"Pipeline script from SCM"**
3. For **"SCM"**, select **"Git"**

### Fill in Git Details

- **Repository URL:** `https://github.com/datatweets/jenkins-demo-python-app.git`
- **Credentials:**
  - Click **"Add"** → **"Jenkins"**
  - **Username:** Your GitHub username
  - **Password:** Paste your GitHub token from Step 2
  - **ID:** `github-credentials`
  - Click **"Add"**
- **Branch Specifier:** `*/main`
- **Script Path:** `Jenkinsfile`

1. Click **"Save"**

---

## Step 6: Run Your First Build

### Option A: Via Jenkins UI

1. Go to your job: `https://YOUR_NGROK_URL/job/jenkins-demo-python-app/`
2. Click **"Build with Parameters"**
3. Set:
   - **BRANCH:** `main`
   - **ENVIRONMENT:** `dev`
4. Click **"Build"**
5. Click the build number to watch the console output

### Option B: Via Jenkins CLI (in Colab)

```python
!java -jar jenkins-cli.jar -s https://YOUR_NGROK_URL/ \
  -auth admin:YOUR_JENKINS_API_TOKEN \
  -noCertificateCheck build jenkins-demo-python-app \
  -p BRANCH=main \
  -p ENVIRONMENT=dev
```

---

## Step 7: View Build Results

1. Click on the build number
2. Check **"Console Output"** to see pipeline logs
3. View **"Test Results"** to see test status
4. Check **"Artifacts"** for build files

---

## What the Pipeline Does

The `Jenkinsfile` automatically:

- Clones your GitHub repository
- Creates Python virtual environment (.venv)
- Installs dependencies from requirements.txt
- Runs code quality checks (pylint)
- Runs unit tests (pytest)
- Scans for security issues (bandit)
- Creates distribution packages
- Deploys to dev/staging/prod
- Performs health checks

---

## Make Changes & Rebuild

1. Make changes to code on your computer
2. Push to GitHub:

   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```

3. Run Jenkins build again (it will pick up the changes automatically)

---

## Quick Commands

```bash
# Download Jenkins CLI
!wget https://YOUR_NGROK_URL/jnlpJars/jenkins-cli.jar

# List all jobs
!java -jar jenkins-cli.jar -s https://YOUR_NGROK_URL/ \
  -auth admin:YOUR_TOKEN \
  -noCertificateCheck list-jobs

# Build with parameters
!java -jar jenkins-cli.jar -s https://YOUR_NGROK_URL/ \
  -auth admin:YOUR_TOKEN \
  -noCertificateCheck build jenkins-demo-python-app \
  -p BRANCH=main \
  -p ENVIRONMENT=dev
```

---

**That's it! Your CI/CD pipeline is now running!**
