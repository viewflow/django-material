# Components

Django Material provides a variety of UI components based on Google's Material Design guidelines. Each component is designed to be accessible, responsive, and customizable.

## Using Components

Django Material components use the django-cotton component system, which allows for a modern, HTML-like syntax for component inclusion.

### Component Organization and Namespacing

Components in subfolders can be called using dot notation to represent folder levels. The `cotton` directory is the base directory for all components and is not included in the component name:

```html
<!-- A component in templates/cotton/sidebar/menu/link.html would be included with: -->
<c-sidebar.menu.link>Home</c-sidebar.menu.link>

<!-- A component in templates/cotton/button/filled.html is included with: -->
<c-button.filled>Click me</c-button.filled>
```

## Buttons

Buttons allow users to take actions and make choices with a single tap.

### Button Variants

Django Material offers different button variants with varying levels of emphasis:

#### Filled Button

The standard filled button with high emphasis:

```html
<c-button.filled>
  Submit
</c-button.filled>
```

#### Elevated Button

A button with a subtle shadow that provides a raised appearance:

```html
<c-button.elevated>
  Continue
</c-button.elevated>
```

#### Outlined Button

A medium-emphasis button with an outline border:

```html
<c-button.outlined>
  Cancel
</c-button.outlined>
```

#### Text Button

A low-emphasis button with no background or border:

```html
<c-button.text>
  Learn More
</c-button.text>
```

#### Icon Button

A compact, circular button that displays only an icon:

```html
<c-button.icon 
  icon="settings" 
  aria_label="Settings">
</c-button.icon>
```

#### Segmented Button

A button used in a group to create a segmented control:

```html
<div class="flex">
  <c-button.segment start>Day</c-button.segment>
  <c-button.segment selected>Week</c-button.segment>
  <c-button.segment end>Month</c-button.segment>
</div>
```

Segmented buttons support these specific parameters:
- `start`: Applies rounded corners to the left side (first button)
- `end`: Applies rounded corners to the right side (last button)
- `selected`: Marks a segment as selected/active
- `icon`: Add an icon to the segment
- `color`: Apply color theme (primary, secondary, tertiary)

For example, with icons and more segments:

```html
<div class="flex">
  <c-button.segment start icon="format_align_left">Left</c-button.segment>
  <c-button.segment icon="format_align_center">Center</c-button.segment>
  <c-button.segment icon="format_align_right" end>Right</c-button.segment>
</div>
```

#### Floating Action Button (FAB)

A circular button that represents the primary action in an application:

```html
<c-button.fab icon="add" aria_label="Create new item"></c-button.fab>
```

FAB buttons support these specific parameters:
- `size`: Size of the button ("small", "regular" (default), or "large")
- `icon`: The icon to display (defaults to "add")
- `color`: Apply color theme (primary, secondary, tertiary)

FAB buttons can be extended with text:

```html
<c-button.fab icon="create" aria_label="Compose">
  Compose
</c-button.fab>
```

### Button with Icon

You can add a Material Icon to text and container button variants:

```html
<c-button.filled icon="add">
  Add Item
</c-button.filled>

<c-button.outlined icon="bookmark">
  Bookmark
</c-button.outlined>

<c-button.text icon="share">
  Share
</c-button.text>
```

Note that the icon button is a separate component designed specifically for icon-only buttons, while these examples show text buttons with accompanying icons.

### Button Colors

Buttons support primary (default), secondary, and tertiary colors:

```html
<c-button.outlined>
  Primary Button
</c-button.outlined>

<c-button.outlined color="secondary">
  Secondary Button
</c-button.outlined>

<c-button.outlined color="tertiary">
  Tertiary Button
</c-button.outlined>
```

### Button Types

You can specify the button type for form submissions:

```html
<c-button.filled type="submit">
  Submit Form
</c-button.filled>
```

### Accessibility Features

All button components include built-in accessibility features:

#### ARIA Labels

Provide descriptive labels for screen readers with `aria_label`:

```html
<c-button.filled aria_label="Submit application form">
  Submit
</c-button.filled>

<!-- Required for icon buttons -->
<c-button.icon icon="settings" aria_label="Open settings"></c-button.icon>
```

#### Keyboard Navigation

Buttons have visible focus states for keyboard navigation:
- Each button has a distinct focus style using background color changes
- Focus states maintain the same color theme as the button
- Focus is more prominent than hover for better visibility

#### Disabled State

Buttons can be disabled with the `disabled` attribute:

```html
<c-button.filled disabled>
  Cannot Submit
</c-button.filled>
```

This applies:
- Visual styling (reduced opacity)
- `aria-disabled="true"` for screen readers
- The `disabled` HTML attribute
- Pointer events disabled to prevent interaction

#### Screen Reader Support

- Icon-only buttons always require an `aria_label`
- Icon decorations within text buttons use `aria-hidden="true"`
- All buttons maintain proper contrast ratios for readability

## Cards

Cards contain content and actions about a single subject.

### Card Variants

Django Material offers different card variants with varying levels of emphasis:

#### Elevated Card

A card with a drop shadow that provides a raised appearance:

```html
<c-card.elevated title="Card Title" subtitle="Optional subtitle">
  <p>Card content goes here.</p>
  
  <c-slot name="footer">
    <div class="flex justify-end space-x-2">
      <c-button.text>Cancel</c-button.text>
      <c-button.filled>Save</c-button.filled>
    </div>
  </c-slot>
</c-card.elevated>
```

#### Filled Card

A high-emphasis card with a colored background:

```html
<c-card.filled 
  title="Promotional Offer" 
  subtitle="Limited time" 
  color="secondary">
  <p>Card content goes here.</p>
  
  <c-slot name="footer">
    <div class="flex justify-end">
      <c-button.text>Action</c-button.text>
    </div>
  </c-slot>
</c-card.filled>
```

#### Outlined Card

A medium-emphasis card with a colored outline:

```html
<c-card.outlined title="Information Card">
  <p>Card content goes here.</p>
  
  <c-slot name="footer">
    <div class="flex justify-between items-center">
      <span class="text-sm">Additional info</span>
      <c-button.text>Dismiss</c-button.text>
    </div>
  </c-slot>
</c-card.outlined>
```

### Card Properties

Cards support these parameters:
- `title`: Main heading text for the card
- `subtitle`: Secondary text displayed below the title
- `color`: Apply color theme (primary, secondary, tertiary) - affects background or border depending on card type

### Named Slots

Cards support the following slot:
- `footer`: Content to display in the card footer section, typically containing actions

## Forms

Forms allow users to enter and submit data.

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-form.basic :form="form">
  <c-slot name="submit">
    <c-button.filled>Custom Submit</c-button.filled>
  </c-slot>
</c-form.basic>
```

## Dialogs

Dialogs inform users about a task and can contain critical information, require decisions, or involve multiple tasks.

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-dialog.basic id="my-dialog">
  <c-slot name="title">Dialog Title</c-slot>
  <c-slot name="content">
    <p>Dialog content goes here.</p>
  </c-slot>
  <c-slot name="actions">
    <c-button.text dismiss>Cancel</c-button.text>
    <c-button.filled>OK</c-button.filled>
  </c-slot>
</c-dialog.basic>

<!-- Button to open the dialog -->
<c-button.filled data-target="my-dialog">Open Dialog</c-button.filled>
```

## Navigation

### Breadcrumbs

Breadcrumbs provide a navigation aid that helps users keep track of their location within the website's hierarchy.

```html
<c-breadcrumbs.container>
  <c-breadcrumbs.item href="/" first>Home</c-breadcrumbs.item>
  <c-breadcrumbs.item href="/products">Products</c-breadcrumbs.item>
  <c-breadcrumbs.item>Current Page</c-breadcrumbs.item>
</c-breadcrumbs.container>
```

Breadcrumbs support these specific parameters:
- `href`: The URL for the breadcrumb link (omit for current page)
- `icon`: Add a Material Icon to the breadcrumb item
- `first`: Indicates this is the first item (no separator before it)

You can also add icons to breadcrumb items:

```html
<c-breadcrumbs.container>
  <c-breadcrumbs.item href="/" icon="home" first>Home</c-breadcrumbs.item>
  <c-breadcrumbs.item href="/products" icon="category">Products</c-breadcrumbs.item>
  <c-breadcrumbs.item icon="shopping_bag">Current Page</c-breadcrumbs.item>
</c-breadcrumbs.container>
```

### Drawer

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-drawer.navigation>
  <c-slot name="items">
    <c-drawer.navigation.item url="home" icon="home">Home</c-drawer.navigation.item>
    <c-drawer.navigation.item url="settings" icon="settings">Settings</c-drawer.navigation.item>
  </c-slot>
</c-drawer.navigation>
```

### App Bar

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-appbar.top>
  <c-slot name="title">App Title</c-slot>
  <c-slot name="actions">
    <c-button.icon icon="account_circle"></c-button.icon>
  </c-slot>
</c-appbar.top>
```

## Data Display

### Tables

Tables provide an organized way to display structured data in rows and columns.

#### Basic Table

A simple table to display data:

```html
<c-table.container :columns="[
  {'label': 'Name', 'key': 'name', 'sortable': True},
  {'label': 'Position', 'key': 'position', 'sortable': True},
  {'label': 'Office', 'key': 'office', 'sortable': True}
]" header>
  <c-table.row>
    <c-table.cell font_medium>Tiger Nixon</c-table.cell>
    <c-table.cell>System Architect</c-table.cell>
    <c-table.cell>Edinburgh</c-table.cell>
  </c-table.row>
  <c-table.row>
    <c-table.cell font_medium>Garrett Winters</c-table.cell>
    <c-table.cell>Accountant</c-table.cell>
    <c-table.cell>Tokyo</c-table.cell>
  </c-table.row>
</c-table.container>
```

#### Table with Selectable Rows

Enables row selection with checkboxes:

```html
<c-table.container :columns="[
  {'label': 'Name', 'key': 'name', 'sortable': True},
  {'label': 'Position', 'key': 'position', 'sortable': True}
]" header selectable>
  <c-table.row selectable row_id="1">
    <c-table.cell>Tiger Nixon</c-table.cell>
    <c-table.cell>System Architect</c-table.cell>
  </c-table.row>
  <c-table.row selectable row_id="2">
    <c-table.cell>Garrett Winters</c-table.cell>
    <c-table.cell>Accountant</c-table.cell>
  </c-table.row>
</c-table.container>
```

#### Table with Pagination

Adds pagination controls for navigating through large datasets:

```html
<c-table.container :columns="[
  {'label': 'Name', 'key': 'name', 'sortable': True},
  {'label': 'Position', 'key': 'position', 'sortable': True}
]" header :pagination="{
  'start': 1,
  'end': 10,
  'total': 57,
  'prev_disabled': True,
  'next_disabled': False
}">
  <!-- Table rows -->
</c-table.container>
```

#### Table Components

The table system consists of three components:

1. **container.html** - The main table wrapper
   - `columns`: List of column objects with properties:
     - `label`: Display name of the column
     - `key`: Unique identifier for sorting
     - `sortable`: Boolean indicating if column can be sorted
   - `header`: Boolean to show/hide the header row
   - `selectable`: Boolean to enable row selection with checkboxes
   - `pagination`: Object with pagination information:
     - `start`: Starting row number being displayed
     - `end`: Ending row number being displayed
     - `total`: Total number of rows in the dataset
     - `prev_disabled`: Boolean to disable previous button
     - `next_disabled`: Boolean to disable next button

2. **row.html** - Individual table rows
   - `selectable`: Boolean to enable checkbox for this row
   - `row_id`: Unique identifier for the row (required when selectable is true)

3. **cell.html** - Individual table cells
   - `font_medium`: Boolean to apply medium font weight (useful for primary cells)
   - `whitespace_nowrap`: Boolean to prevent text wrapping
   - Supports all HTML attributes via `{{ attrs }}`

#### Accessibility Features

The table components include built-in accessibility features:
- Semantic HTML table structure
- ARIA attributes for improved screen reader compatibility
- Clear visual indicators for sortable columns
- Keyboard navigation support for interactive elements
- Proper focus states for all interactive elements

### Lists

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-list.basic>
  <c-slot name="items">
    {% for item in items %}
      <c-list.item :text="item.text" :secondary-text="item.secondary_text"></c-list.item>
    {% endfor %}
  </c-slot>
</c-list.basic>
```

## Feedback

### Snackbar

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-snackbar.basic message="Item saved."></c-snackbar.basic>
```

### Progress

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-progress.circular></c-progress.circular>

<!-- Progress with value -->
<c-progress.linear :value="50"></c-progress.linear>
```

## Advanced Usage

### Passing attributes

All HTML attributes can be passed directly to components:

```html
<c-button.filled 
  id="save-button" 
  class="custom-class" 
  aria-label="Save document"
  data-testid="save-btn">
  Save
</c-button.filled>
```

### Boolean attributes

For boolean attributes, simply include the attribute name without a value:

```html
<c-button.filled disabled>Can't Click Me</c-button.filled>
```

### Template variables

Use the colon prefix to pass template variables:

```html
<c-button.filled :disabled="is_disabled">
  Dynamic State
</c-button.filled>
```