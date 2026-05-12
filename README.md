# acortino — Resume

Source repository for my resume, written in LaTeX and automatically compiled with GitHub Actions.

## Build

The PDF is generated automatically on every push to `main`.

Generated artifact:

```text
acortino_resume.pdf
```

## Local compilation

Requirements:

* `pdflatex`
* TeXLive packages (`tcolorbox`, `fontawesome`, `worldflags`, etc.)

Compile locally:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## GitHub Actions

The workflow:

1. Compiles `main.tex`
2. Generates `acortino_resume.pdf`
3. Commits the updated PDF back to the repository

Workflow file:

```text
.github/workflows/build.yml
```

## Repository structure

```text
.
├── .github/
│   └── workflows/
│       └── build.yml
├── main.tex
├── acortino_resume.pdf
└── README.md
```
