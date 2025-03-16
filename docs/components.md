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

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-card.basic>
  <c-slot name="title">Card Title</c-slot>
  <c-slot name="content">
    <p>Card content goes here.</p>
  </c-slot>
  <c-slot name="actions">
    <c-button.text>Action</c-button.text>
  </c-slot>
</c-card.basic>
```

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

> ⚠️ **Coming Soon** - This component is not yet implemented.

```html
<c-table.data :data="data">
  <c-slot name="headers">
    <th>Name</th>
    <th>Email</th>
  </c-slot>
  <c-slot name="rows">
    {% for item in data %}
      <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.email }}</td>
      </tr>
    {% endfor %}
  </c-slot>
</c-table.data>
```

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