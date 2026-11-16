# Lab 5 - Static Code Analysis
## Issue Analysis
| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| SSL certificate verification disabled (B501) | High - Security | 60 | HTTP request disables SSL certificate verification. | Use default SSL certificate verification. |
| Unsafe backup command (B609, B602, B607) | High - Security | 64 | Backup uses subprocess with shell=True and a wildcard. | Replace shell execution with Python tarfile operations. |
| Missing HTTP timeout (B113) | Medium - Security | 60 | ERP request can wait indefinitely. | Add a reasonable request timeout. |
| Insecure TLS protocol (B503) | Medium - Security | 66 | TLS 1.0 is used as the default protocol. | Use a modern default SSL context. |
| Mutable default argument (W0102) | Medium - Bug | 18 | A shared dictionary may retain data between calls. | Use None and initialize a new dictionary. |
| Attendance threshold logic | Bug - Manual review | 30 | Exactly 75% is incorrectly treated as ineligible. | Change the comparison to >=. |
| Division by zero | Bug - Manual review | 27 | Empty attendance records cause a division-by-zero error. | Handle the empty-record case. |
| Incorrect latest-date comparison | Bug - Manual review | 46-47 | Dates are compared as strings instead of date values. | Parse dates before comparison. |
| Hard-coded API key | Security - Manual review | 12 | Credential-like value is stored directly in source code. | Read the key from an environment variable. |
| Unused imports (F401) | Code Quality | 1, 4, 6 | Unused modules are imported. | Remove unused imports or use them where appropriate. |
| Missing encoding and file handling (W1514) | Code Quality | 50 | CSV file is opened without explicit encoding or a context manager. | Use with open and encoding="utf-8". |
| Style violations (E302, E305, E501, E712) | Code Quality | Multiple | Blank lines, line lengths and Boolean comparisons violate style rules. | Apply PEP 8 formatting. |
## Baseline Results
- Pylint score: 4.55/10
- Bandit: 2 High, 3 Medium, 3 Low findings
- Flake8: Multiple style and unused-import findings
