# Development Guidelines for Django Material

## Build & Development Commands
- `npm run build:css`: Build CSS files from TailwindCSS
- `npm run build:js`: Bundle JavaScript with esbuild
- `npm run dev`: Start development server with file watching
- `npm run test`: Run Django tests
- `npm run lint`: Run pyright type checking
- `npm run format`: Format code with ruff and black
- `npm run provision`: Setup project on a new server
- `npm run deploy`: Update project on an existing server
- Use `uv` instead of pip for Python package management
- To run python tests for a specific module use: `nom run test path.to.module`

## Code Style
- Use TailwindCSS for components
- Follow Google style docstrings for Python code
- Follow Material Design 3 guidelines for component styling
- Use uv to run python
- Component-specific styling guidelines are in `material/templates/cotton/CLAUDE.md`

## Django-Cotton Component System

Detailed component development guidelines are documented in `material/templates/cotton/CLAUDE.md`.

## Comment Guidelines
- Module docstrings: 1-2 lines explaining core purpose/function
- Class docstrings: Single line explaining role/responsibility
- Method docstrings: Brief description of function and parameters
- Inline comments: Only for non-obvious code or key functionality
- Use concise language, avoid excessive verbosity
- For form renderers, document template context variables

## Project Structure
- Place components in material/templates/cotton/{component_type}/
- Demo code in demo/ directory:
  - demo/templates/demo/index.html - Main landing page
  - Dedicated pages for each component category (buttons.html, cards.html, etc.)
  - Each demo page should have consistent navigation
- Component development guidelines are in `material/templates/cotton/CLAUDE.md`

## Component Design & Naming
- Component design principles and naming conventions are detailed in `material/templates/cotton/CLAUDE.md`

## Git Workflow
- To commit, always use this exact format with `--author` flag:
  ```
  git commit --author="Claude AI <claude@anthropic.com>" -m "Commit message"
  ```
- IMPORTANT: 
  - The `--author="Claude AI <claude@anthropic.com>"` flag MUST be included exactly as shown
  - This is required for GitHub to properly attribute commits to Claude
  - DO NOT use Co-Authored-By trailers instead of `--author`, as they don't change the commit author
- All feature/fix commits should be done under Claude's name
- Run `npm run build:css` before committing CSS changes
- Update _dumb.html component when using new implicit {{ color }} class names in components