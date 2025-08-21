from jinja2 import Environment, FileSystemLoader
import subprocess
import os

def make_pdf(data, folder, fileName):

    for i in range(1, 4): data[f"MotiveCol{i}"] = [] # add motive cols

    for i, motive in enumerate(data["Motives"]):
        data[f"MotiveCol{i % 3 + 1}"].append(motive)

    # Setup Jinja2 environment with custom delimiters
    env = Environment(
        loader=FileSystemLoader('.'),
        variable_start_string='(',
        variable_end_string=')',
        block_start_string='%{',
        block_end_string='}%',
        autoescape=False
    )

    template = env.get_template('template.tex')
    full_path = os.path.join(folder, fileName)
    filled_tex = template.render(data)

    with open(f'{full_path}.tex', 'w+', encoding="utf-8") as f:
        f.write(filled_tex)

    subprocess.run(['pdflatex', f'{full_path}.tex', f'-aux-directory={folder}/auxiliary', f"-output-directory", folder])