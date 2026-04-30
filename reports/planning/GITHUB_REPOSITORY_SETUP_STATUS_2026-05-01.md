# GitHub Repository Setup Status

Date: 2026-05-01

## Current Status

The local project folder `D:\二区` has been initialized as a git repository.

- Local repository: `D:\二区\.git`
- Current branch: `main`
- Local git binary: `D:\二区\tools\PortableGit\cmd\git.exe`
- Initial local commit: `93910dd` (`Initial manuscript project snapshot`)
- GitHub app login detected: `1627626277-cyber`
- GitHub account email detected: `1627626277@qq.com`
- GitHub app installation detected for the user account.

## GitHub Remote Status

The GitHub connector is authenticated, but it currently exposes repository listing, file, branch, PR, and issue operations only. It does not expose a create-new-repository operation in this Codex session.

Repository listing returned zero accessible repositories:

- Accessible repositories: none

Therefore, a remote GitHub repository has not yet been created from Codex.

## Repository Hygiene

`.gitignore` has been configured to prevent accidental tracking of large or regenerable files:

- raw SRA / FASTQ / BAM / CRAM files
- spatial archives and extracted matrix containers
- reference genomes and BLAST databases
- local toolchains
- external raw-data caches
- downloaded PDF files
- compressed intermediate result tables
- run logs

This keeps the repository suitable for scripts, reports, manuscript files, compact result tables, and figure assets.

## Local Commit Status

An initial local manuscript-project snapshot has been committed.

Commit:

- `93910dd Initial manuscript project snapshot`

The commit includes:

- project logs and report index
- analysis scripts
- compact result tables
- manuscript drafts
- figure files
- validation and review reports
- reference-library metadata

The commit excludes:

- raw external datasets
- reference genomes
- local toolchains
- downloaded full-text PDFs
- SRA/FASTQ/BAM/H5 matrix containers
- compressed intermediate tables and run logs

## Required User-Side Action To Push To GitHub

Because the connector cannot create a new repository, one of the following is required before Codex can push the project online:

1. Create an empty GitHub repository manually under `1627626277-cyber`.
   - Recommended repository name: `mm-plasma-secretory-spatial-q2`
   - Visibility: private until manuscript submission
   - Do not initialize with README, `.gitignore`, or license, because the local repository already contains project files.

2. Or install and authenticate GitHub CLI (`gh`) so Codex can create the remote repository from the command line.

After an empty remote exists, the local repository can be connected with:

```powershell
& 'D:\二区\tools\PortableGit\cmd\git.exe' remote add origin https://github.com/1627626277-cyber/mm-plasma-secretory-spatial-q2.git
& 'D:\二区\tools\PortableGit\cmd\git.exe' push -u origin main
```

## Current Project Stage

The project has entered manuscript submission-preparation, not final submission.

Ready components:

- manuscript target draft for BMC Medical Genomics
- main figures and figure legends
- cross-cohort evidence table
- reference library and formal numbered references
- Cox adjusted models
- Cox proportional hazards assumption screening
- stage-2 numeric integrity review

Remaining before actual journal upload:

- author list and affiliations
- ethics/data availability/conflict/funding statements
- final figure format and supplement packaging
- citation cross-check against in-text numbering
- cover letter
- target-journal portal metadata
