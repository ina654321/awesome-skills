# Scenario Examples

## 9.1 Scenario: Submitting a New Skill

**User:** "I want to create a new skill for home brewing beer. How do I submit it to the repository?"

**Project Developer:**
> **Here's the process for submitting a new skill:**
> 
> **Step 1: Proposal (Open Issue)**
> Create a GitHub issue with:
> - Skill name: home-brewing or beer-brewing
> - Category: Likely crafts or special
> - Description: 50-500 characters
> - Author: Your name/handle
> - Trigger words: "home brew", "beer brewing", etc.
> 
> **Step 2: Wait for Approval**
> Maintainers will review for:
> - Does a similar skill already exist?
> - Is the category appropriate?
> - Does it meet domain requirements?
> 
> **Step 3: Create the Skill**
> After approval:
> 1. Create branch: feature/home-brewing
> 2. Copy template and fill in SKILL.md
> 3. Add 4 reference files minimum
> 4. Self-assess quality score honestly
> 
> **Step 4: Submit PR**
> - Follow PR template exactly
> - Include testing notes
> - Ensure all CI checks pass
> - Respond to reviewer feedback
> 
> **Key Requirements:**
> - 16 H2 sections in SKILL.md
> - System prompt with clear role definition
> - Real resources, no placeholder URLs
> - Domain-specific terminology

---

## 9.2 Scenario: Quality Gate Failure

**User:** "My PR failed CI checks saying 'broken link detected' but I didn't add any links. What should I do?"

**Project Developer:**
> **Troubleshooting broken link failures:**
> 
> **Common causes:**
> 
> **1. Existing broken links in referenced files**
> - The CI checks ALL files in skills/, not just yours
> - Your change may have exposed a pre-existing broken link
> - Check the CI log for which file/URL is failing
> 
> **2. Relative path issues**
> - Images or files referenced with wrong paths
> - Example: Using /images instead of ../images
> - Verify all links are correct
> 
> **3. External resource unavailable**
> - The link you added goes to a site that's down
> - Find alternative resource or remove if not critical
> 
> **How to investigate:**
> 1. Check the CI log ( Actions tab in GitHub)
> 2. Find the specific failing URL
> 3. Test it in your browser
> 4. Fix or replace with valid URL
> 
> **How to fix:**
> - Update the broken link
> - Use Internet Archive (web.archive.org) for archived content
> - Remove non-essential links if no alternative exists

---

## 9.3 Scenario: Upgrading an Existing Skill

**User:** "I found that one of the skills in the repo has outdated information. The skill version is 1.0.0 but the content is clearly old. How do I upgrade it?"

**Project Developer:**
> **Here's how to upgrade an existing skill:**
> 
> **Step 1: Assess the Changes Needed**
> - Read current SKILL.md vs. template
> - Identify what sections need updating
> - Check if resources are still valid
> - Note the current version number
> 
> **Step 2: Create Upgrade Branch**
> - Branch name: upgrade/[skill-name]
> - Example: upgrade/legacy-api-integration
> 
> **Step 3: Make Changes**
> - Update frontmatter: version bump (e.g., 1.0.0 to 2.0.0)
> - Refresh outdated sections
> - Fix broken links
> - Add new reference materials
> - Preserve original attribution
> 
> **Step 4: Document Changes**
> - In PR, list what changed and why
> - Note any breaking changes
> - Update quality score if content improved
> 
> **Version Bump Guidelines:**
> | Change Type | Version Bump |
> |------------|-------------|
> | Bug fixes, typos | Patch (1.0.x to 1.0.1) |
> | New features, content additions | Minor (1.0.0 to 1.1.0) |
> | Breaking changes, restructure | Major (1.0.0 to 2.0.0) |
> 
> **Important:** Don't remove original author attribution even when upgrading significantly.