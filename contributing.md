# Documentation Contributing Guide

We welcome contributions from all users and the community. By contributing, you agree to the [Percona Community code of conduct](https://percona.community/contribute/coc/). Thank you for deciding to contribute and help us improve the [Percona Server for MySQL documentation](https://docs.percona.com/percona-server/).

You can contribute to the documentation in one of the following ways:

* **Forum**: Best for questions, discussions, or general feedback

* **Jira ticket**: Best for reporting issues or requesting changes that you'd like the team to handle

* **Edit yourself**: Best for making direct changes, fixing typos, or adding content

## Add a topic in the Percona Community Forum

The [Percona Community Forum](https://forums.percona.com/) is a public discussion platform where you can ask questions, share feedback, or suggest improvements to the documentation. Use the forum to start a conversation about documentation issues, request clarifications, or discuss potential changes with the community and documentation team.

To add a topic, navigate to the [Percona Product Documentation category](https://forums.percona.com/c/percona-product-documentation/71) in the Percona Community Forum and select **New Topic**. Complete the form and select **Create Topic** to add the topic to the forum.

![Create a topic](docs/_static/new-topic.png "Create a topic")

## Request a change with a Jira issue

You can report documentation issues or request changes by creating a Jira ticket. This method is useful when you want to track the issue formally or when you want the documentation team to handle the changes.

Use the following procedure to create a Jira ticket:

1. Open the [Percona Server Jira project](https://jira.percona.com/projects/PS/issues) in your browser.

2. Sign in (or create a Percona Jira account if you don't have one).

3. Click the **Create** button.

4. Fill in the required fields:

    * **Summary**: Provide a brief description of the issue.

    * **Description**: Provide more information about the issue. If needed, add a Steps To Reproduce section and information about your environment (version number, your operating system, etc.). Be detailed.

    * **Version**, **Environment**, and other relevant fields as needed.

5. Click **Create** to submit the ticket.

!!! tip "Shortcut to the issue creation screen"

    To go directly to the Create Issue form, use this URL: [https://jira.percona.com/secure/CreateIssue!default.jspa?pid=10100](https://jira.percona.com/secure/CreateIssue!default.jspa?pid=10100)

## Edit documentation yourself

Use the [Edit documentation online with GitHub](#edit-documentation-online-with-github) method or the [Edit documentation locally](#edit-documentation-locally) method to make changes to the documentation and create a pull request. 

### What you should know

Most of the documentation is in plain text, but you may use [Markdown](https://www.markdownguide.org/) to add syntax elements (notes, tables, and so on) to the documentation. 

### What happens after you create the pull request

Our team reviews your pull request and provides feedback or approval. Once approved, we merge your changes into the appropriate branch. Thank you for taking the time to improve our documentation!

!!! note

    We appreciate your work, but the PR may be revised to meet internal requirements.

### Edit documentation online with GitHub

1. Next to the page title, select **Edit this page on GitHub** to open the source file in the GitHub editor. If you haven't worked with the repository before, GitHub creates a [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) automatically.

2. Edit the page using the [Markdown](https://www.markdownguide.org/) syntax.

3. Review your changes by clicking the **Preview** tab to see how they will appear.

4. Scroll to the bottom of the page to the **Commit changes** section.

5. Add a commit message (72 characters or less) describing what you changed.

6. Select the **Create a new branch for this commit and start a pull request** option. GitHub will suggest a branch name, which you can accept or modify.

7. Click **Commit changes**.

8. GitHub creates a branch and commit for your changes, then displays a page where you can create a pull request. This page shows:

   * The base branch where you're proposing your changes

   * Your commit message

   * A visual diff of your changes

9. Review the information and click **Create pull request**.

For more information, see [Editing files in GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files). 

### Edit documentation locally

This option is for users who are comfortable with [git](https://git-scm.com/) commands.

Follow these steps:

1. Fork this repository on GitHub.

2. Clone your forked repository to your machine:

    ```shell
        git clone https://github.com/<your_github_name>/psmysql-docs.git
        cd psmysql-docs
    ```

    !!! note "SSH alternative"
    
        If you have SSH keys set up with GitHub, you can use `git@github.com:<your_github_name>/psmysql-docs.git` instead.

3. Add the upstream remote to track the original repository:

    ```shell
        git remote add upstream https://github.com/percona/psmysql-docs.git
    ```

4. Checkout the main branch and pull the latest changes from upstream:

    ```shell
        git checkout main
        git pull upstream main
    ```

5. Create a separate branch for your changes:

    ```shell
        git checkout -b <my_changes>
    ```

6. Edit the files in the `/docs` directory. Add code examples, if necessary. We recommend that you check your changes using either a Preview built into your editor (if you have one) or [build HTML on your machine](#building-the-documentation).

7. Add the changed file (replace `docs/example.md` with your actual file path):

    ```shell
        git add docs/example.md
    ```

8. Commit your changes (replace the message with a description of your changes):

    ```shell
        git commit -m 'Fixed typo in install-audit-log-filter.md'
    ```

9. Push your branch to your fork:

    ```shell
        git push -u origin <my_changes>
    ```

10. On GitHub, navigate to your fork and click **Create pull request** to open a pull request to the Percona repository.

### Building the documentation

To verify your changes, you can use MkDocs to build and preview the documentation locally.

1. Install the required dependencies:

    ```shell
        pip install -r requirements.txt
    ```

2. In the root directory, start the local development server:

    ```shell
        mkdocs serve
    ```

3. Open your browser and navigate to `http://127.0.0.1:8000/` to view the documentation. The server automatically reloads when you make changes to the files.

4. Navigate to the document you changed to verify your edits.

### Building the PDF documentation

!!! tip "Browser recommendation"

    This procedure works best in Google Chrome. Other browsers may not render the PDF correctly.

To build the PDF documentation:

1. Build the documentation site:

    ```shell
        mkdocs build
    ```

2. Open the `site/print_page.html` file in Chrome. You can do this by:

    * Navigating to the file in your file manager and double-clicking it, or

    * Opening Chrome and using **File > Open File** to navigate to `site/print_page.html`

3. In Chrome, press `Ctrl+P` (or `Cmd+P` on Mac) to open the Print dialog, or select **Print** from the menu.

4. In the Print dialog:

    * Set the **Destination** to **Save as PDF**

    * Adjust any print settings as needed (margins, paper size, etc.)

    * Click **Save** and choose where to save the PDF file
