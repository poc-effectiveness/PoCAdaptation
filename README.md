# PoCAdaptation

## 🔍 Overview

**PoCAdaptation** is a repository for storing **adapted Proof-of-Concept (PoC) exploits** derived from known CVE reports. The goal is to identify **potential false negatives (missed detections)** in existing CVE reports by adjusting or adapting PoCs to work under different versions, environments, or configurations.



## 📖 Background

This repository uses PoCs from the dataset published alongside the paper  
[*"Vision: Identifying Affected Library Versions for Open Source Software Vulnerabilities"*](https://ieeexplore.ieee.org/document/10764837).

In many cases, the original PoCs no longer work in certain library versions—even though those versions may still be vulnerable. By analyzing dependency-level code diffs, we adapt these PoCs to restore their effectiveness and reveal **potentially vulnerable versions that were missed or excluded in the original CVE disclosures**.



## 📁 Repository Structure

``````
.
├── Origin/       # Original public PoCs
│   └── CVE-xxxx-xxxx/
│       └── exploit/
│           └── ... original test code, pom.xml, etc.

├── Adapted/      # Adapted PoCs organized by CVE and version
│   └── CVE-xxxx-xxxx/
│       └── <Version>/
│           └── exploit/
│               └── ... modified test code, execution results, etc.

└── README.md     # Project description

``````



## ▶️ How to Reproduce

To reproduce an adapted PoC for a specific CVE and version:

1. Navigate to the corresponding `exploit/` directory.  
   For example:
   ```bash
   cd Adapted/CVE-2019-16869/5.0.0.Alpha1/exploit

2. Run the following command to execute the test:

   ``````bash
   mvn test
   ``````

Maven will compile and run the test case. Results will be displayed in the terminal and recorded in `target/surefire-reports/`.

> ✅ Make sure you have Java and Maven properly installed.



## ⚠️ Disclaimer

This project is intended for **research and academic purposes only**.

 All PoCs are derived from publicly available sources.

 Please ensure any testing is done in isolated, controlled environments.

 **Do not** use these PoCs in production or against systems you do not own or have explicit permission to test.



## 📝 Our PRs to GitHub Advisory Database

We actively contribute to improving the accuracy of CVE records by identifying overlooked affected versions and submitting them to the [GitHub Advisory Database](https://github.com/github/advisory-database).

- [PR #5774 – Add affected version `5.0.0.Alpha1` to CVE-2019-16869](https://github.com/github/advisory-database/pull/5774)
