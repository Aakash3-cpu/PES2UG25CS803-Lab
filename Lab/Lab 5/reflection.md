# Lab 5 - Reflection
## 1. What is static code analysis?
Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, and coding style problems before the software is deployed.
## 2. What is the difference between Pylint, Bandit, and Flake8?
Pylint checks code quality, naming conventions, unused imports, and possible programming mistakes. Bandit identifies security issues such as disabled SSL verification and unsafe shell execution. Flake8 checks Python formatting and PEP 8 style guidelines.
## 3. What problems did you identify and fix?
I fixed the mutable default argument, incorrect 75% eligibility condition, division-by-zero possibility, and date comparison issue. I also improved security by enabling SSL verification, adding request timeouts, removing shell-based command execution, and moving the API key to an environment variable.
## 4. What did you learn from this lab?
I learned that different static analysis tools identify different categories of problems. Using all three tools improved the quality, readability, and security of my attendance tracker. I also learned that manual testing is important because some logical errors may not be detected by static analysis tools.
## Final Results
- Pylint: 10.00/10
- Bandit: No issues identified
- Flake8: No issues identified
