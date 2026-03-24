## § 8 · Workflow

### Phase 1: Analysis & Classification

**Objective:** Understand what type of documentation is needed and where it fits in the Diátaxis framework.

**Key Activities:**
1. **Identify the Documentation Type** — Is this a Tutorial, How-To Guide, Explanation, or Reference?
2. **Determine Audience** — What's the reader's technical level? What do they already know?
3. **Gather Inputs** — What source material is available? (specs, code, interviews, existing docs)
4. **Assess Freshness Risk** — Will this content drift quickly? (UI steps, version numbers, screenshots)

**Questions to Ask:**
- "What will the reader be able to do after reading this?"
- "What assumed knowledge must the reader have?"
- "How will this content be maintained?"

**✓ Done Criteria:**
- [✓] Documentation type clearly identified
- [✓] Target audience defined
- [✓] Source materials collected
- [✓] Maintenance plan for high-drift content

### Phase 2: Drafting

**Objective:** Produce the initial documentation following the identified type's conventions.

**Key Activities:**
1. **Structure First** — Create heading hierarchy before writing content
2. **Code Examples First** — Write the code sample, then prose to explain it
3. **Apply Style Guide** — Follow Google or Microsoft style guide conventions
4. **Use Proper Admonitions** — Note, Warning, Tip, Danger blocks for callouts

**Reference Documentation Template:**
```
## Endpoint Name

Brief description of what this endpoint does.

### Request

- **Method:** GET/POST/etc.
- **URL:** `/endpoint/path`
- **Authentication:** Required/Optional

### Request Body (if applicable)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| | | | |

### Response

#### 200 OK

| Field | Type | Description |
|-------|------|-------------|
| | | |

#### Error Responses

| Code | Description | Resolution |
|------|-------------|------------|
| 400 | Bad Request | ... |
| 401 | Unauthorized | ... |

### Example

\`\`\`bash
curl -X GET "https://api.example.com/endpoint" \
  -H "Authorization: Bearer YOUR_TOKEN"
\`\`\`
```

**✓ Done Criteria:**
- [✓] All sections populated
- [✓] Code examples present and valid
- [✓] Style guide applied
- [✓] Heading hierarchy logical

### Phase 3: Review & Verification

**Objective:** Verify the documentation is accurate, complete, and usable.

**Key Activities:**
1. **Stranger Test** — Have someone unfamiliar with the system try to use the docs
2. **Code Verification** — Test all code examples in CI pipeline
3. **Fact Check** — Verify API specs, version numbers, and links are current
4. **Readability Check** — Run Hemingway or similar to check complexity
5. **Accessibility Check** — Ensure proper heading hierarchy, alt text, and links work

**✓ Done Criteria:**
- [✓] Stranger test passed
- [✓] All code examples tested
- [✓] Links functional
- [✓] Readability target met (Grade Level < 10)
- [✓] Accessibility check passed

### Phase 4: Publication & Maintenance

**Objective:** Deploy documentation and establish maintenance workflows.

**Key Activities:**
1. **Deploy to Production** — Publish to docs site
2. **Set Up Alerts** — Configure monitoring for broken links, search failures
3. **Document Inputs** — Note where source material lives and how to update
4. **Establish Review Cadence** — Schedule periodic reviews for accuracy

**✓ Done Criteria:**
- [✓] Documentation live
- [✓] Monitoring active
- [✓] Update process documented
- [✓] Review schedule established

---
