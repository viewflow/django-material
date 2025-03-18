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
  - [x] Card enhancement components
    - [x] hover_border attribute - Show border only on hover
    - [x] card_menu.html - Card action menu
    - [ ] card_menu_item.html - Menu item for card actions
    - [ ] card_actions.html - Container for card action buttons
    - [ ] card_divider.html - Visual divider for card sections
    - [ ] card_media.html - Media container for cards
    - [ ] card_content_group.html - Group related content within card
- [ ] Dialog/Modal
- [ ] App bar
- [x] Breadcrumbs navigation
- [x] Navigation drawer
  - [x] Drawer components
    - [x] container.html - Main drawer container
    - [x] header.html - Drawer header with logo/title
    - [x] group.html - Group of navigation items with title
    - [x] item.html - Navigation item with icon and label
    - [x] divider.html - Content divider
  - [x] Drawer variants
    - [x] Standard drawer - Full navigation with labels
    - [x] Rail navigation - Icon-only compact navigation
    - [x] Modal drawer - Overlay on top of content (with backdrop)
  - [x] Features
    - [x] Responsive behavior - Adapt to screen size
    - [x] Nested navigation - Expandable sections with children
    - [x] Active state - Highlight current section
    - [x] Icons support - Items with icon attribute for Material icons
    - [x] Rounded corners - Custom styling for improved design
- [ ] Tabs
- [ ] Data table
  - [ ] Core table components
    - [ ] table.html - Main table container
    - [ ] table_header.html - Table header row
    - [ ] table_body.html - Table body container
    - [ ] table_row.html - Table row component
    - [ ] table_cell.html - Table cell component
  - [ ] Data table features
    - [ ] Sorting - Column sorting with indicators
    - [ ] Filtering - Advanced filtering options
    - [ ] Pagination - Page navigation controls
    - [ ] Row actions - Action buttons/menus for rows
    - [ ] Selection - Row selection with checkboxes
    - [ ] Expandable rows - Collapsible detail views
  - [ ] Styling and behavior
    - [ ] _table.scss - Base table styling
    - [ ] _filter.scss - Filter component styling
    - [ ] _pagination.scss - Pagination controls styling
    - [ ] _actions.scss - Row actions styling
    - [ ] sort.js - Sorting behavior implementation
    - [ ] filter.js - Filtering functionality
    - [ ] pagination.js - Pagination controls handling
    - [ ] actions.js - Row actions implementation
- [x] List components
  - [x] Container component
  - [x] List items
    - [x] One-line item
    - [x] Two-line item
    - [x] Three-line item
  - [x] Supporting elements
    - [x] Leading icons/avatars/thumbnails
    - [x] Trailing actions
    - [x] Dividers
    - [x] Subheaders
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
5. Add remaining card enhancement components
   - Card actions container
   - Card media support
6. Begin data table implementation with core components
   - Basic table structure
   - Sorting functionality
   - Pagination controls
7. Implement app bar component
   - Top navigation bar
   - Search functionality
   - Responsive collapsing
8. Finish installation documentation
9. Add unit tests for existing components 
10. Create form controls, enhanced cards, and data table showcase pages in demo app