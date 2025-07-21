# PoCAdaptation

## 🔍 Overview

**PoCAdaptation** is a curated repository of **adapted Proof-of-Concept (PoC) exploits** migrated across multiple versions of real-world Java libraries. It aims to identify **false negatives** in existing CVE reports—specifically, vulnerable versions that were previously undetected or misclassified—by adapting PoCs that initially fail due to software evolution.




## 📖 Background

Directly reusing existing PoCs on alternative library versions often fails due to:

- **Triggering condition changes** (e.g., API refactorings)
- **Environment-level breakages** (e.g., build or runtime errors)

These failures make it difficult to confirm whether a version is truly unaffected, especially when manual adaptation is costly and error-prone.


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

├── Diffploit/                  # Core implementation of the Diffploit migration framework
│   ├── diff_manager.py         # Handles diff extraction and filtering for migration
│   ├── error_manager.py        # Diagnoses reproduction failures and categorizes errors
│   ├── exploit_adapter.py      # Performs LLM-based exploit adaptation
│   ├── exploit_executor.py     # Executes PoCs and captures reproduction results
│   ├── exploit_preparer.py     # Prepares the execution environment and dependencies
│   ├── exploit_repair.py       # Applies fixes based on adaptation context
│   ├── llm_client.py           # Interfaces with the LLM for adaptation guidance
│   ├── logger.py               # Unified logging utility
│   ├── main_process.py         # Entry point for coordinating the full migration pipeline
│   ├── version_analyzer.py     
│   └── version_selector.py     

├── Result/                     # Evaluation results of different adaptation strategies
│   ├── Diffploit/              # Default Diffploit results
│   ├── Diffploit-Annealing/   # Diffploit + simulated annealing exploration
│   ├── Diffploit-Causing/     # Diffploit using only causing diffs
│   ├── Diffploit-ChatGPT-only/
│   ├── Diffploit-Deepseek-only/
│   ├── Diffploit-Supporting/  # Diffploit using only supporting diffs
│   └── abalation.json         # Aggregated ablation results

``````

## 

## ▶️ How to Reproduce Diffploit

> ⚠️ *Diffploit is containerized via Docker. A Docker image will be released after the review process to support full reproducibility.*

This section describes the **local environment setup** required to run Diffploit.

### ✅ Prerequisites

Before running `Diffploit`, please make sure the following dependencies are properly installed:

#### ☕ Java (Required)

```
java version "11" 2018-09-25  
Java(TM) SE Runtime Environment 18.9 (build 11+28)  
Java HotSpot(TM) 64-Bit Server VM 18.9 (build 11+28, mixed mode)
```

#### 🛠 Maven (Reference Version)

```
Apache Maven 3.8.8
```

#### 🐍 Python (Reference Version)

```
Python 3.8.10 (default, Nov 22 2023)
```

------

## 🔑 LLM API Key Setup

We provide a temporary **DeepSeek API key** for review purposes. To use it, modify the following line in `Diffploit/llm_client.py`:

```
self.api_key = "Your_API_Key_Here"  # Replace with your actual API key
```

Replace it with:

```
self.api_key = "sk-13da5a223e92430eb79d38eadda31699"
```

> 🔒 *This key is only intended for **review use**. It may be revoked after the review process.*



## 🔧 Step 1: Set Absolute Path to Project Root

The Diffploit implementation currently uses **absolute paths** for referencing data, especially the `PoCAdaptation` directory.

After cloning the project to your local machine, you **must replace all hardcoded occurrences** of `/PoCAdaptation` in the `Diffploit/` source files with your **actual local path**.

### ✅ Example

If you cloned the project to:

```
/home/username/projects/PoCAdaptation
```

Then you should **replace** all instances of:

```
/PoCAdaptation
```

with:

```
/home/username/projects/PoCAdaptation
```



## ▶️ Step 2: Run Migration for a Specific Exploit

Once your environment and paths are correctly set up, you can test the migration of a single exploit by directly executing `main_process.py` with a specific CVE ID.

### ✅ Example

```
python Diffploit/main_process.py CVE-2021-XXXXX
```

This will trigger the full migration pipeline for the specified CVE, including:

- Reference-target version selection
- Diff extraction and context construction
- LLM-based adaptation
- Validation and reproduction logging

All intermediate logs and final adapted exploits will be saved under the corresponding subdirectory in `Adapted/`.

------

## ▶️ Step 3: Batch Migration & Ablation Study

To run **batch migration experiments** (including **ablation variants**) across all CVEs and multiple adaptation strategies, execute the following script:

```
python scripts/run.py
```



## ▶️ How to Reproduce an Adapted PoC 

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