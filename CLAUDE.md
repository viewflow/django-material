# Development Guidelines for Django Material

## Build & Development Commands
- `npm run build:css`: Build CSS files from TailwindCSS
- `npm run build:js`: Bundle JavaScript with esbuild
- `npm run dev`: Start development server with file watching
- `npm run test`: Run Django tests
- `npm run lint`: Run pyright type checking
- Use `uv` instead of pip for Python package management


## Code Style
- Use TailwindCSS for components
- Follow Google style docstrings for Python code
- Follow Material Design 3 guidelines for component styling
- Always provide ARIA attributes for accessibility
- Use CSS custom properties for theming with primary/secondary/tertiary color schemes
- Implement proper hover and focus states for interactive elements
- Components with text content should use slot content directly instead of label attributes
- Required attributes should have sensible defaults whenever possible
- Use uv to run python

## Django-Cotton Component System

### File Structure & Naming
- Component files in `templates/cotton/{component_type}/`
- Component filenames use snake_case: `button.html`, `card_list.html`
- Component variants in subfolders or with descriptive names: `button/filled.html`
- Components are used with kebab-case prefixed by 'c-': `<c-my-component>`
- Component variants use dot notation: `<c-button.filled>`

### Basic Usage Patterns

#### Default Slot Content
```html
<!-- In component definition -->
<a href="/" class="...">{{ slot }}</a>

<!-- In view usage -->
<c-button>Contact</c-button>

<!-- HTML output -->
<a href="/" class="...">Contact</a>
```
- Everything between opening and closing tags is provided as `{{ slot }}`
- The slot can contain any content: text, HTML, or Django template expressions

#### Named Slots
```html
<c-card.filled>
  <c-slot name="title">Card Title</c-slot>
  Main content here
  <c-slot name="footer">Footer content</c-slot>
</c-card.filled>
```

#### Default Values with `<c-vars>`
```html
<!-- In component definition -->
<c-vars
  type="text"
  class="border rounded px-4 py-2" />
  
<input 
  type="{{ type }}" 
  class="{{ class }}" 
  {{ attrs }} />
```
- `<c-vars>` defines default values that can be overridden by explicit attributes

#### Attribute Passing with `{{ attrs }}`
```html
<!-- Example usage -->
<c-input placeholder="Enter your name" />
<c-input type="email" required class="border-blue-500" />

<!-- HTML output -->
<input type="text" class="border rounded px-4 py-2" placeholder="Enter your name" />
<input type="email" class="border-blue-500" required />
```
- `{{ attrs }}` contains all attributes passed to the component
- Attributes passed explicitly override defaults from `<c-vars>`

#### Boolean Attributes
```html
<c-button.filled disabled>Cannot Click</c-button.filled>
```

#### Dynamic Values
```html
<!-- Template variables with colon prefix -->
<c-button.filled :disabled=is_disabled>Dynamic Button</c-button.filled>

<!-- Python data types with colon prefix -->
<c-table.container :columns="[{'label': 'Name', 'sortable': True}]"></c-table.container>

<!-- Dynamic components -->
<c-component :is="component_type"></c-component>
```

## Comment Guidelines
- Module docstrings: 1-2 lines explaining core purpose/function
- Class docstrings: Single line explaining role/responsibility
- Method docstrings: Brief description of function and parameters
- Inline comments: Only for non-obvious code or key functionality
- Use concise language, avoid excessive verbosity
- For form renderers, document template context variables

## Project Structure
- Place components in material/templates/cotton/{component_type}/
- Document components in docs/components.md
- Demo code in demo/ directory:
  - demo/templates/demo/index.html - Main landing page
  - Dedicated pages for each component category (buttons.html, cards.html, etc.)
  - Each demo page should have consistent navigation

## Timeless Component Design Principles
- Use semantic HTML elements for proper accessibility
- Keep component APIs simple and intuitive
- Be consistent with attribute naming across similar components
- Minimize required JavaScript dependencies
- Design for mobile-first, responsive experiences
- Ensure keyboard navigability for all interactive elements
- Provide visual feedback for all interactive states
- Design components to be composable with other components
- Follow progressive enhancement principles
- Ensure components work well with screen readers

## Naming Conventions
- Use consistent parameter names across similar components
- Component variants follow Material Design 3 naming: filled, outlined, elevated, etc.
- For component demos, use semantic IDs that match component types
- Demo templates should have same structure with breadcrumbs, and concise, descriptive titles
- Prefer shorter component names (e.g., c-nav instead of c-navigation)
- Use standard attribute names (e.g., icon, title, variant) consistently

## Git Workflow
- To commit, always use:
  ```
  git commit --author="Claude AI <claude@anthropic.com>" -m "Commit message"
  ```
- IMPORTANT: The `--author` flag is required for GitHub to recognize Claude as a contributor
- DO NOT use Co-Authored-By trailers alone, as they don't change the commit author
- All feature/fix commits should be done under Claude's name
- Run `npm run build:css` before committing CSS changes
- Update _dumb.html compoment when using new implicity {{ color }} class names in compoments