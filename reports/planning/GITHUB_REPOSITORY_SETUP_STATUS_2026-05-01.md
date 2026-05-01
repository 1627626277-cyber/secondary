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

The GitHub connector is authenticated, but it currently exposes repository listing, file, branch, PR, and issue operations only. It did not expose a create-new-repository operation in this Codex session.

Repository listing later confirmed the user-created repository:

- `1627626277-cyber/secondary`
- URL: `https://github.com/1627626277-cyber/secondary`

The local git remote has been set to:

- `https://github.com/1627626277-cyber/secondary.git`

Local command-line `git push` has not completed yet. The latest non-interactive attempt failed with `Could not resolve host: github.com`.

Connector-side repository initialization:

- `README.md` updated through the GitHub connector.
- `CODE_AVAILABILITY.md` created through the GitHub connector.

This establishes the intended code-availability URL, but it does not replace the full local repository push.

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

After command-line GitHub authentication and network resolution are working, the local repository can be pushed with:

```powershell
& 'D:\二区\tools\PortableGit\cmd\git.exe' remote set-url origin https://github.com/1627626277-cyber/secondary.git
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
