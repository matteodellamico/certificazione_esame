#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import os.path
import shutil
from string import Template
import subprocess
import tempfile

FILENAME_DATE_FORMAT = '%y%m%d'

course_abbreviations = {
    'DC': "Distributed Computing",
    'DS': "Decentralized Systems",
    'PROG1': "Programmazione 1"
}

parser = argparse.ArgumentParser(
    description='Create a letter according to the given LaTeX template',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('name', type=str, help='Name')
parser.add_argument('course', type=str, help='Course name')
parser.add_argument('--template', type=str, help='Path to the template file', default='template.tex')
parser.add_argument('--output', type=str, help='Path to the output PDF file')
parser.add_argument('--date', type=str, help='Date of the letter')
parser.add_argument('--docdate', type=str, help='Date of the document')
parser.add_argument('--letterhead', type=str, help='Path to the letterhead PDF', default='dibris_lh.pdf')
args = parser.parse_args()

with open(args.template, 'r') as f:
    template = Template(f.read())

course = course_abbreviations.get(args.course, args.course)
now = datetime.now()

if args.date is None:
    date = '\\today{}'
    output_date = datetime.now().strftime(FILENAME_DATE_FORMAT)
else:
    date = args.date
    output_date = datetime.strptime(args.date, '%d/%m/%Y').strftime(FILENAME_DATE_FORMAT)

docdate = args.docdate if args.docdate is not None else '\\today{}'

tex_source = template.substitute(name=args.name, date=date, docdate=docdate, course=course)

if args.output is None:
    texfile = f"{output_date}_{args.name.split()[-1].lower()}_{args.course.lower()}.tex"
    output = texfile.replace('.tex', '.pdf')
else:
    texfile = args.output.replace('.pdf', '.tex')
    output = args.output

# Write tex_source to a file and compile it with pdflatex
with tempfile.TemporaryDirectory() as tmpdir:
    texfilepath = os.path.join(tmpdir, texfile)
    with open(texfilepath, 'w') as f:
        f.write(tex_source)
    shutil.copy(args.letterhead, os.path.join(tmpdir, 'letterhead.pdf'))
    subprocess.run(['pdflatex', texfilepath], cwd=tmpdir)
    shutil.move(texfilepath.replace('.tex', '.pdf'), output)

print(f"Letter saved to {output}")