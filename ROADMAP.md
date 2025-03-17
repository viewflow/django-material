# Django Material Development Roadmap

This file tracks the development progress of the Django Material project. As items are completed, mark them with [x].

## Core Components

- [x] Base HTML templates
- [x] Button component
  - [x] Basic implementation (filled button)
  - [x] Text button
  - [x] Outlined button
  - [x] Elevated button
  - [x] Icon button
  - [x] Segmented button
  - [x] Floating action button
- [ ] Form controls
  - [ ] Input fields
    - [ ] text.html - Basic text input
    - [ ] textarea.html - Multiline text input
    - [ ] email.html - Email input with validation
    - [ ] password.html - Secure password input
    - [ ] number.html - Numeric input
    - [ ] search.html - Search input
    - [ ] url.html - URL input with validation
    - [ ] tel.html - Telephone number input
    - [ ] color.html - Color picker
    - [ ] date.html - Date picker
    - [ ] time.html - Time picker
    - [ ] datetime.html - Combined date and time
    - [ ] file.html - File upload
    - [ ] clearable_file_input.html - File upload with clear option
    - [ ] hidden.html - Hidden input
    - [ ] multiple_hidden.html - Multiple hidden inputs
    - [ ] multiple_input.html - Multiple text inputs
    - [ ] attrs.html - Attributes helper
  - [ ] Selection controls
    - [ ] select.html - Dropdown select
    - [ ] select_date.html - Date selection widget
    - [ ] select_option.html - Individual select option
    - [ ] checkbox.html - Checkbox control
    - [ ] checkbox_option.html - Individual checkbox option
    - [ ] checkbox_select.html - Multiple checkbox selection
    - [ ] radio.html - Radio button control
    - [ ] radio_option.html - Individual radio option
  - [ ] Complex inputs
    - [ ] input_option.html - Input with options
    - [ ] multiwidget.html - Multiple widget container
    - [ ] splitdatetime.html - Split date and time inputs
    - [ ] splithiddendatetime.html - Split date/time with hidden
  - [ ] Advanced form components
    - [ ] autocomplete.html - Autocomplete text input
    - [ ] editor.html - Rich text editor
    - [ ] formset.html - Form set container
    - [ ] json.html - JSON data editor
    - [ ] select_dependent.html - Dependent/cascading select
    - [ ] total.html - Calculation total field
- [x] Card component
  - [x] Elevated card
  - [x] Filled card
  - [x] Outlined card
- [ ] Dialog/Modal
- [ ] App bar
- [x] Breadcrumbs navigation
- [ ] Navigation drawer
- [ ] Tabs
- [ ] Data table
- [ ] Snackbar/Toast notifications
- [ ] Progress indicators

## Documentation

- [x] Initial setup with MkDocs
- [x] Component usage guide
- [ ] Installation instructions
- [ ] Theme customization guide
- [ ] Accessibility guidelines
- [ ] API reference
- [ ] Example implementations

## Infrastructure

- [x] Project structure setup
- [x] Integration with django-cotton
- [ ] Testing framework
  - [ ] Unit tests for components
  - [ ] Integration tests
  - [ ] Visual regression tests
- [ ] CI/CD pipeline
- [ ] Package distribution
  - [ ] PyPI publishing
  - [ ] Release process documentation

## Demo Application

- [x] Basic Django project setup
- [ ] Component showcase
- [ ] Form handling examples
- [ ] Authentication flow demo
- [ ] CRUD operation examples
- [ ] Responsive layout examples

## Optimization & Features

- [ ] Performance optimization
- [ ] Responsive design improvements
- [ ] RTL language support
- [ ] Theme customization
  - [ ] Color schemes
  - [ ] Typography
  - [ ] Component density
- [ ] Dark mode support
- [ ] Accessibility compliance (WCAG 2.1 AA)

## Integration

- [ ] HTMX integration examples
- [ ] Alpine.js integration
- [ ] Django admin theme

***

## Next Milestone Tasks

1. Implement basic text input components (text.html, email.html, password.html)
2. Create checkbox and radio button components
3. Develop select dropdown components
4. Implement date/time input components
5. Finish installation documentation
6. Add unit tests for existing components 
7. Create form controls showcase page in demo app