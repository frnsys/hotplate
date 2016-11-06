# Hotplate
### A simple boilerplate system

There are two main components:

- _templates_: arbitrary jinja templates
- _recipes_: yaml files that define...
    - project directory structure
    - what files to create from what templates
    - default variable values

## Usage

    hotplate <recipe name> <project path>

`hotplate` will parse all the required variables and prompt you to enter them. At present these variables are all treated as strings.

## Recipes

### Basics

Recipes define the project structure and which templates to use.

For example:

```yaml
proj:
    index.html: threejs.html
    css:
        main.sass: main.sass
```

This will result in the following project structure:

```
.
├── index.html
└── css
    └── main.sass
```

Where `index.html` is created from the `templates/threejs.html` template and `main.sass` is created from the `templates/main.sass` template.

### Recipe variables

Recipes can also define variables to pass to templates.

For instance, say I have a template for `package.json` and I want to create a recipe for `three.js` projects. For this recipe I want to include `three` as a dependency, but I want to it exclude it otherwise.

I could make `templates/package.json` like so:

```jinja
{
  "name": "{{ project_name }}",
  "version": "0.0.0",
  "dependencies": {
    {% if three %}
    "three": "latest",
    {% endif %}
    "underscore": "latest"
  }
}
```

Then, in my `three.js` recipe, which I'd create at `recipes/three.yml`, I'd include (just showing the relevant `package.json` bit here):

```yaml
proj:
    package.json: package.json
vars:
    three: true
```

### Recipe bases

It can be annoying to manually map every project file to a template if you want to basically copy over a template directory.

For example, say I have the following template directory, `templates/three`:

```
.
├── app
│   └── Scene.js
├── css
│   └── main.sass
├── index.html
└── main.js
```

I don't want to have to do something like this for my recipe:

```yaml
proj:
    package.json: package.json
    index.html: three/index.html
    main.js: three/main.js
    app:
        Scene.js: three/app/Scene.js
    css:
        main.sass: three/css/main.sass
```

That's too redundant. Instead, you can specify a "base" template directory, which is automatically mirrored to the new project:

```yaml
proj:
    package.json: package.json
base: three
```

Here, `base: three` tells `hotplate` to mirror `templates/three` as a starting point.