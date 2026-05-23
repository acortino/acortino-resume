# acortino — Resume

Source repository for my resume.

The resume content is stored once in `resume-data.yml` and rendered into multiple LaTeX templates using Python/Jinja.

This allows the same source of truth to generate both an ATS-friendly resume and a more designed human-readable resume.

## Generated resumes

The build generates two PDF versions:

```text
dist/anthony-cortinovis-resume-ats.pdf
dist/anthony-cortinovis-resume.pdf
```

### ATS-friendly version

This version is for job portals, applicant tracking systems, and automated resume parsing.

```text
dist/anthony-cortinovis-resume-ats.pdf
```

### Design version

This version is for direct emails, referrals, portfolio links, or human readers.

```text
dist/anthony-cortinovis-resume.pdf
```

## Repository structure

```text
.
├── .github/
│   └── workflows/
│       └── build.yml
├── scripts/
│   └── render_resume.py
├── templates/
│   ├── resume-ats.tex.j2
│   └── resume-design.tex.j2
├── build/
│   ├── resume-ats.tex
│   └── resume-design.tex
├── dist/
│   ├── anthony-cortinovis-resume-ats.pdf
│   └── anthony-cortinovis-resume.pdf
├── resume-data.yml
└── README.md
```

`build/` contains generated intermediate files and can be ignored by Git.

`dist/` contains the final generated PDFs.

## Source of truth

Resume content is edited in:

```text
resume-data.yml
```

This file contains:

- Profile
- Languages
- Skills
- Experiences
- Education
- Personal projects

The LaTeX files are generated from this YAML file.

Do not manually edit files inside `build/`.

## Local build

### Requirements

System dependencies:

```text
latexmk
pdftotext
TeX Live
Python 3.12+
```

Python dependencies:

```text
pyyaml
jinja2
```

### Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install pyyaml jinja2
```

### Render LaTeX files

```bash
python scripts/render_resume.py
```

### Compile the ATS resume

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -output-directory=build \
  build/resume-ats.tex
```

### Compile the design resume

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -output-directory=build \
  build/resume-design.tex
```

### Copy generated PDFs to `dist/`

```bash
mkdir -p dist
cp build/resume-ats.pdf dist/anthony-cortinovis-resume-ats.pdf
cp build/resume-design.pdf dist/anthony-cortinovis-resume.pdf
```

## ATS text extraction check

To verify that the ATS version can be read correctly:

```bash
pdftotext dist/anthony-cortinovis-resume-ats.pdf build/ats.txt
cat build/ats.txt
```

Important information such as name, title, skills, experience, technologies, and dates should appear in a logical reading order.

Example checks:

```bash
grep -Fq "Anthony Cortinovis" build/ats.txt
grep -Fq "Senior Software Engineer" build/ats.txt
grep -Fq "Java" build/ats.txt
grep -Fq "Spring Boot" build/ats.txt
grep -Fq "Kafka" build/ats.txt
grep -Fq "gRPC" build/ats.txt
```

## GitHub Actions

The GitHub Actions workflow:

1. Checks out the repository
2. Installs LaTeX and Python dependencies
3. Renders LaTeX files from `resume-data.yml`
4. Compiles both resume templates
5. Copies the generated PDFs to `dist/`
6. Runs a basic ATS text extraction check
7. Commits updated PDFs back to the repository

Workflow file:

```text
.github/workflows/build-resume.yml
```

## Editing workflow

To update the resume:

1. Edit `resume-data.yml`
2. Push to `main`
3. Review both generated PDFs
4. Check the ATS text extraction output

## Notes

The ATS template should stay conservative. Avoid adding icons, columns, sidebars, tables, or visual-only elements to it.

The design template can be more visual, but it should still be generated from the same YAML content to avoid drift between versions.
