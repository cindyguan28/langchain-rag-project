# LangChain RAG Project

## Overview

This repository is a personal learning project based on the original [pixegami/langchain-rag-tutorial](https://github.com/pixegami/langchain-rag-tutorial).

The original tutorial uses a book-based example. In this fork, the project has been adapted for an AWS guidance knowledge base, focusing on common troubleshooting topics around:

* AWS Glue crawler permissions
* Amazon Athena query issues
* Amazon QuickSight access troubleshooting
* AWS Lake Formation permissions
* S3 KMS encryption
* Official AWS / Terraform / LangChain source references

The goal of this project is to practice a local RAG workflow:

```text
→ Load documents
→ Split documents into chunks
→ Create local embeddings
→ Store chunks in Chroma
→ Retrieve relevant context
→ Generate an answer with a local Ollama model
```

## Note

This fork is used for personal learning and experimentation.

Original project:

* <https://github.com/pixegami/langchain-rag-tutorial>

This version contains self-created learning notes and mock troubleshooting documentation.

## Project structure

```text
langchain-rag-project/
├── data/
│   └── aws-guidance/
│       ├── athena-query-issues.md
│       ├── glue-crawler-permissions.md
│       ├── lake-formation-permissions.md
│       ├── quicksight-access-troubleshooting.md
│       ├── s3-kms-encryption.md
│       └── sources.md
├── create_database.py
├── query_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Knowledge base

The knowledge base is stored under:

```text
data/aws-guidance/
```

Each Markdown file follows a similar structure:

```text
# Title

## Purpose

## Common symptoms

## Root causes

## Required permissions or configuration

## Troubleshooting checklist

## Example user questions
```

The `sources.md` file contains official reference links to AWS, Terraform, and LangChain documentation.

## Python environment

It is recommended to use a local virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then upgrade pip:

```bash
python -m pip install --upgrade pip setuptools wheel
```

## Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If the `requirements.txt` file is not available yet, install the core dependencies manually:

```bash
pip install -U langchain langchain-community langchain-text-splitters langchain-core langchain-chroma chromadb langchain-huggingface sentence-transformers langchain-ollama
```

This project currently uses local Hugging Face embeddings:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Therefore, an OpenAI API key is not required for creating the local Chroma vector database.

## Install Ollama

This project uses Ollama to run a local LLM for answer generation.

Install Ollama from the official website:

```text
https://ollama.com/download
```

After installation, check that the CLI works:

```bash
ollama --version
```

Pull the local model used by this project:

```bash
ollama pull llama3.2:3b
```

Test the model:

```bash
ollama run llama3.2:3b
```

Exit the Ollama chat with:

```text
/bye
```

The current `query_data.py` uses:

```text
llama3.2:3b
```

If you use another Ollama model, update the model name in `query_data.py`.

## Create the Chroma database

Run:

```bash
python create_database.py
```

This script will:

1. Load Markdown files from `data/aws-guidance/`
2. Split the documents into smaller chunks
3. Generate embeddings with a local Hugging Face embedding model
4. Store the chunks in a local Chroma database under:

```text
chroma/
```

Example output:

```text
Loaded 6 documents.
Split 6 documents into 130 chunks.
Saved 130 chunks to chroma.
```

The first run may take longer because the Hugging Face model needs to be downloaded. After that, the model is usually cached locally.

## Query the database

After creating the Chroma database and installing Ollama, query the local RAG system with:

```bash
python query_data.py "Why does a Glue crawler fail on KMS encrypted S3 data?"
```

You can also retrieve more chunks by passing `--k`:

```bash
python query_data.py "What is the difference between IAM and Lake Formation permissions?" --k 5
```

The query script will:

1. Embed the user question with the local Hugging Face embedding model
2. Search the local Chroma vector database
3. Retrieve the most relevant chunks
4. Send the retrieved context to the local Ollama model
5. Generate an answer based only on the retrieved context
6. Print the answer and source documents

Example questions for this knowledge base:

```text
Why does Athena fail even though the IAM role has S3 access?
What permissions does a Glue crawler need for KMS encrypted data?
What is the difference between IAM permissions and Lake Formation permissions?
Why can a QuickSight user see a dashboard but not load the visuals?
What should I check if S3 access works but kms:Decrypt fails?
```

## Local-only setup

This project can run locally without an OpenAI API key:

* Embeddings: local Hugging Face model
* Vector database: local Chroma database
* LLM answer generation: local Ollama model

This makes the project suitable for learning and experimentation without sending prompts to an external LLM provider.

## OpenAI API key

This project currently does not require an OpenAI API key.

If you later switch to OpenAI embeddings or OpenAI chat models, create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit `.env` to Git.

## Files that should not be committed

The following files and folders should stay local:

```text
.venv/
.env
chroma/
__pycache__/
*.pyc
.DS_Store
```

Make sure they are included in `.gitignore`.

Example `.gitignore`:

```gitignore
.venv/
.env
chroma/
__pycache__/
*.pyc
.DS_Store
```

## Important note about `.venv`

The `.venv/` folder contains local Python packages and binaries. It should never be committed to Git.

If `.venv/` appears in the Git changes list, remove it from Git tracking:

```bash
git rm -r --cached .venv
```

Then make sure `.venv/` is listed in `.gitignore`.

## Important note about `chroma/`

The `chroma/` folder contains the local vector database generated from the source documents. It can be recreated by running:

```bash
python create_database.py
```

For this reason, `chroma/` should usually not be committed.

## Development workflow

After changing documents or code:

```bash
git status
git add .
git commit -m "friendly text"
git push origin main
```

Before committing, always check that `.venv/`, `.env`, and `chroma/` are not included.

A safer add command is:

```bash
git add README.md requirements.txt create_database.py query_data.py data/aws-guidance/ .gitignore
```

## Troubleshooting

### Ollama command not found

If this happens:

```text
zsh: command not found: ollama
```

Install Ollama from:

```text
https://ollama.com/download
```

Then restart the terminal and run:

```bash
ollama --version
```

### Ollama model not found

If the query script cannot find the model, pull it first:

```bash
ollama pull llama3.2:3b
```

### Chroma database not found

If `query_data.py` cannot find the local vector database, create it first:

```bash
python create_database.py
```

### `.venv` appears in Git changes

Make sure `.venv/` is listed in `.gitignore`, then run:

```bash
git rm -r --cached .venv
```

## Original tutorial

This project is based on the following tutorial:

[RAG + LangChain Python Project: Easy AI Chat For Your Docs](https://www.youtube.com/watch?v=tcqEUSNCn8I&ab_channel=pixegami)
