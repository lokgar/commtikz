#!/usr/bin/env python3
"""Compile the visual assertions and verify unsupported fixed topologies fail."""
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(tempfile.gettempdir()) / 'commtikz-check'
LATEX = shlex.split(os.environ.get('LATEX', 'pdflatex'))
FLAGS = shlex.split(os.environ.get('LATEXFLAGS', '-interaction=nonstopmode -halt-on-error'))


def compile_tex(source, directory):
    result = subprocess.run(
        [*LATEX, *FLAGS, f'-output-directory={directory}', str(source)],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return result.returncode, result.stdout


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    code, output = compile_tex(ROOT / 'tests/components.tex', OUTPUT)
    if code or 'commtikz component checks passed.' not in output:
        raise SystemExit(output)
    cases = []
    for style, west, east in [
        ('splitter', 1, 2), ('combiner', 2, 1), ('dcoupler', 2, 2),
        ('hybrid90', 2, 4), ('bpd', 2, 1), ('ringmod', 1, 1),
        ('pm', 1, 1), ('mzm', 1, 1), ('iqm', 1, 1), ('opamp', 2, 1),
    ]:
        cases.extend([
            (f'\\node[{style},numW={west + 1}] {{}};', f'Fixed topology requires numW={west}'),
            (f'\\node[{style},ports={{E={east + 1}}}] {{}};', f'Fixed topology requires numE={east}'),
        ])
    cases.extend([
        (r'\node[hybrid90,port order=bottom to top] {};', 'top-to-bottom port order'),
        (r'\node[bpd,port span y=0.5] {};', 'full-height port span'),
        (r'\node[dcoupler] (d) {}; \draw (d.E2) -- ++(1,0);', 'Port E2 is outside this fixed topology'),
        (r'\node[ringmod] (r) {}; \draw (r.drop in) -- ++(-1,0);', 'Drop ports require add drop=true'),
    ])
    with tempfile.TemporaryDirectory(prefix='commtikz-invalid-') as directory:
        for index, (body, expected) in enumerate(cases):
            source = Path(directory) / f'invalid-{index}.tex'
            source.write_text(
                '\\documentclass{article}\n\\usepackage{commtikz}\n'
                '\\begin{document}\\begin{tikzpicture}\n'
                + body + '\n\\end{tikzpicture}\\end{document}\n'
            )
            code, output = compile_tex(source, directory)
            if code == 0 or expected not in output:
                raise SystemExit(f'Expected rejection: {expected}\n{output}')
    print(f'Component assertions passed; {len(cases)} invalid topology cases rejected.')
    print(f'Visual sheets: {OUTPUT / "components.pdf"}')


if __name__ == '__main__':
    main()
