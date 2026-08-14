# Phase 2 — UAT Checklist

## Mempool Congestion Visualizer

**PoC ID:** POC-88
**Phase:** Phase 2
**Developer:** Aswin Sankar P.S.
**Application:** Mempool Congestion Visualizer
**Data Source:** Mempool.space API

---

## 1. User Acceptance Testing

User Acceptance Testing (UAT) verifies that the Phase 2 application meets the expected functional, usability, reliability, and data requirements.

---

## 2. UAT Test Cases

| UAT ID  | Test Scenario             | Expected Result                            | Status |
| ------- | ------------------------- | ------------------------------------------ | ------ |
| UAT-001 | Launch application        | Application loads successfully             | ☐      |
| UAT-002 | Load dashboard            | Dashboard displays correctly               | ☐      |
| UAT-003 | Fetch mempool data        | Current mempool data is retrieved          | ☐      |
| UAT-004 | Display transaction count | Transaction count is displayed correctly   | ☐      |
| UAT-005 | Display mempool size      | Current mempool size is displayed          | ☐      |
| UAT-006 | Fetch fee data            | Fee information is retrieved successfully  | ☐      |
| UAT-007 | Display fee information   | Fee values are displayed correctly         | ☐      |
| UAT-008 | Calculate congestion      | Congestion score/level is generated        | ☐      |
| UAT-009 | Display congestion level  | Correct congestion classification is shown | ☐      |
| UAT-010 | Display congestion chart  | Chart renders correctly                    | ☐      |
| UAT-011 | Fetch recent blocks       | Recent Bitcoin blocks are displayed        | ☐      |
| UAT-012 | Display block statistics  | Block metrics are displayed correctly      | ☐      |
| UAT-013 | Display fee analysis      | Fee-market analysis is displayed           | ☐      |
| UAT-014 | Display intelligence      | Network intelligence is displayed          | ☐      |
| UAT-015 | Refresh data              | Latest available network data is retrieved | ☐      |
| UAT-016 | API failure               | Application displays a meaningful error    | ☐      |
| UAT-017 | Invalid API response      | Application handles invalid data safely    | ☐      |
| UAT-018 | Backend unavailable       | Frontend shows appropriate error state     | ☐      |
| UAT-019 | Loading state             | Loading indicator appears during requests  | ☐      |
| UAT-020 | Navigation                | Dashboard sections are accessible          | ☐      |
| UAT-021 | Chart validation          | Charts display valid data                  | ☐      |
| UAT-022 | Data consistency          | Dashboard data matches API data            | ☐      |
| UAT-023 | Responsive design         | Interface works on supported screen sizes  | ☐      |
| UAT-024 | Security check            | Sensitive credentials are not exposed      | ☐      |
| UAT-025 | Complete workflow         | Full user workflow operates successfully   | ☐      |

---

## 3. Functional Acceptance Criteria

* [ ] Application starts without critical errors.
* [ ] Dashboard loads successfully.
* [ ] Mempool data is retrieved.
* [ ] Transaction information is displayed.
* [ ] Mempool size is displayed.
* [ ] Fee information is available.
* [ ] Congestion analysis works.
* [ ] Congestion classification is displayed.
* [ ] Recent block information is available.
* [ ] Charts render correctly.
* [ ] Network intelligence is available.
* [ ] Refresh functionality works.
* [ ] API errors are handled gracefully.
* [ ] Invalid data does not crash the application.
* [ ] Frontend and backend communicate correctly.

---

## 4. Usability Acceptance Criteria

* [ ] Dashboard is easy to understand.
* [ ] Important metrics are clearly visible.
* [ ] Charts are readable.
* [ ] Congestion status is easy to identify.
* [ ] Fee information is understandable.
* [ ] Error messages are meaningful.
* [ ] Navigation is intuitive.
* [ ] Layout is responsive.

---

## 5. Data Acceptance Criteria

* [ ] API data is retrieved successfully.
* [ ] Data is processed correctly.
* [ ] Displayed values are consistent with API responses.
* [ ] Numerical values use appropriate data types.
* [ ] Invalid or missing values are handled.
* [ ] Data timestamps are recorded correctly where applicable.

---

## 6. Error Handling Acceptance Criteria

The application should gracefully handle:

* API timeout
* API unavailable
* Network failure
* Invalid API response
* Missing data
* Backend failure
* Frontend/backend connection failure

The application should display a user-friendly message instead of crashing.

---

## 7. Security Acceptance Criteria

* [ ] No private Bitcoin keys are used.
* [ ] No wallet credentials are stored.
* [ ] Sensitive API credentials are not committed to GitHub.
* [ ] `.env` files are excluded where required.
* [ ] No sensitive information is exposed in the frontend.
* [ ] API requests are handled securely.

---

## 8. UAT Result

### Overall Status

```text
[ ] PASS
[ ] PASS WITH MINOR ISSUES
[ ] FAIL
```

### Issues Identified

| Issue ID | Description | Severity | Resolution | Status |
| -------- | ----------- | -------- | ---------- | ------ |
| —        | —           | —        | —          | —      |

---

## 9. Final Sign-Off

| Role         | Name             | Status  | Date | Signature |
| ------------ | ---------------- | ------- | ---- | --------- |
| Developer    | Aswin Sankar P.S | Pending | —    | —         |
| Reviewer     | —                | Pending | —    | —         |
| Project Lead | —                | Pending | —    | —         |

---

## 10. UAT Completion Criteria

Phase 2 UAT is considered complete when:

1. All critical test cases have been executed.
2. All critical defects have been resolved.
3. Core application functionality works correctly.
4. API integration has been verified.
5. Dashboard analytics have been validated.
6. Security checks have been completed.
7. Final reviewer approval has been obtained.
