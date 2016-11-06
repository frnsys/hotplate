import os
import yaml
import click
from functools import reduce
from jinja2 import Environment, FileSystemLoader, meta

here = os.path.dirname(os.path.realpath(__file__))
env = Environment(
    loader=FileSystemLoader(os.path.join(here, 'templates')),
    trim_blocks=True, lstrip_blocks=True)


def load_recipe(name):
    fname = os.path.join(here, 'recipes', '{}.yml'.format(name))
    with open(fname, 'r') as f:
        return yaml.load(f)


def make(path, proj, data):
    """recursively execute the recipe project,
    creating directories and files as needed"""
    os.mkdir(path)
    for key, val in proj.items():
        if isinstance(val, dict):
            # directory, recurse
            dir = os.path.join(path, key)
            make(dir, val, data)
        else:
            # file
            tmpl = env.get_template(val)
            contents = tmpl.render(**data)
            fname = os.path.join(path, key)
            with open(fname, 'w') as f:
                f.write(contents)


def required_vars(proj):
    """gets all required vars for a recipe project"""
    vars = []
    for key, val in proj.items():
        if isinstance(val, dict):
            # directory, recurse
            vars += required_vars(val)
        else:
            # file
            vars += _template_vars(val)
    return set(vars)


def _template_vars(name):
    """gets all vars for a jinja template,
    including from extends"""
    vars = []
    src = env.loader.get_source(env, name)[0]
    parsed = env.parse(src)
    for item in parsed.body:
        if hasattr(item, 'template'):
            vars += _template_vars(item.template.value)
    vars += meta.find_undeclared_variables(parsed)
    return set(vars)


def _apply_base(base, proj):
    """takes a template 'base' directory and modifies
    the recipe project to mirror its structure & templates"""
    for path, dirs, files in os.walk(os.path.join(here, 'templates', base)):
        fullpath = path.replace(here + '/', '').split('/')
        projpath = fullpath[2:]
        tmplpath = fullpath[1:]
        data = {fname: '/'.join(tmplpath + [fname]) for fname in files}

        if projpath:
            parent = reduce(dict.get, projpath[:-1], proj)
            dir = projpath[-1]
            if dir in parent:
                parent[dir].update(data)
            else:
                parent[dir] = data

        # root
        else:
            proj.update(data)
    return proj


@click.group()
def cli(): pass


@cli.command()
@click.argument('recipe')
@click.argument('path')
def main(recipe, path):
    """generate a project from a recipe"""
    recipe = load_recipe(recipe)

    proj = recipe['proj']
    if 'base' in recipe:
        proj = _apply_base(recipe['base'], proj)


    # load variables specified by the recipe
    data = recipe['vars'] if 'vars' in recipe else {}
    del recipe['vars']

    # query user for any undefined variables
    for var in required_vars(proj):
        if var not in data:
            data[var] = input('{}: '.format(var))

    # make the project
    make(path, proj, data)
