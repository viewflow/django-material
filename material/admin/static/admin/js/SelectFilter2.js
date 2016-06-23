/*
SelectFilter2 - Turns a multiple-select box into a filter interface.

Requires core.js, SelectBox.js and addevent.js.
*/
(function($) {
function findForm(node) {
    // returns the node of the form containing the given node
    if (node.tagName.toLowerCase() != 'form') {
        return findForm(node.parentNode);
    }
    return node;
}

window.SelectFilter = {
    init: function(field_id, field_name, is_stacked, admin_static_prefix) {
        if (field_id.match(/__prefix__/)){
            // Don't initialize on empty forms.
            return;
        }
        var from_box = document.getElementById(field_id);
        from_box.id += '_from'; // change its ID
        from_box.className = 'filtered material-ignore';

        var ps = from_box.parentNode.getElementsByTagName('p');
        for (var i=0; i<ps.length; i++) {
            if (ps[i].className.indexOf("info") != -1) {
                // Remove <p class="info">, because it just gets in the way.
                from_box.parentNode.removeChild(ps[i]);
            } else if (ps[i].className.indexOf("help") != -1) {
                // Move help text up to the top so it isn't below the select
                // boxes or wrapped off on the side to the right of the add
                // button:
                from_box.parentNode.insertBefore(ps[i], from_box.parentNode.firstChild);
            }
        }

        // <div class="selector"> or <div class="selector stacked">
        var selector_div = quickElement('div', from_box.parentNode);
        selector_div.className = is_stacked ? 'selector stacked' : 'selector row';

        // <div class="selector-available">
        var selector_available = quickElement('div', selector_div);
        selector_available.className = 'selector-available col s12 m6';

        var filter_input = quickElement('input', selector_available, '', 'type', 'text', 'placeholder', interpolate(gettext('Available %s') + ' ', [field_name]));
        filter_input.id = field_id + '_input';

        selector_available.appendChild(from_box);



        // <ul class="selector-chooser">
        var selector_chooser = quickElement('ul', selector_div);
        selector_chooser.className = 'selector-chooser col s12';
        var add_link = quickElement('a', quickElement('li', selector_chooser), '', 'title', gettext('Choose'), 'href', 'javascript: (function(){ SelectBox.move("' + field_id + '_from","' + field_id + '_to"); SelectFilter.refresh_icons("' + field_id + '");})()', 'id', field_id + '_add_link');
        add_link.className = 'selector-add btn-floating btn-flat';
        quickElement('i', add_link, 'chevron_right').className = 'material-icons';
        var remove_link = quickElement('a', quickElement('li', selector_chooser), '', 'title', gettext('Remove'), 'href', 'javascript: (function(){ SelectBox.move("' + field_id + '_to","' + field_id + '_from"); SelectFilter.refresh_icons("' + field_id + '");})()', 'id', field_id + '_remove_link');
        quickElement('i', remove_link, 'chevron_left').className = 'material-icons';
        remove_link.className = 'selector-remove btn-floating btn-flat';

        // <div class="selector-chosen">
        var selector_chosen = quickElement('div', selector_div);
        selector_chosen.className = 'selector-chosen col s12 m6';
        quickElement('input', selector_chosen, '', 'type', 'text', 'placeholder', interpolate(gettext('Chosen %s') + ' ', [field_name]), 'disabled');

        var to_box = quickElement('select', selector_chosen, '', 'id', field_id + '_to', 'multiple', 'multiple', 'size', from_box.size, 'name', from_box.getAttribute('name'));
        to_box.className = 'filtered material-ignore';

        from_box.setAttribute('name', from_box.getAttribute('name') + '_old');

        // Set up the JavaScript event handlers for the select box filter interface
        addEvent(from_box, 'change', function(e) { SelectFilter.refresh_icons(field_id); });
        addEvent(to_box, 'change', function(e) { SelectFilter.refresh_icons(field_id); });
        addEvent(from_box, 'dblclick', function() { SelectBox.move(field_id + '_from', field_id + '_to'); SelectFilter.refresh_icons(field_id); });
        addEvent(to_box, 'dblclick', function() { SelectBox.move(field_id + '_to', field_id + '_from'); SelectFilter.refresh_icons(field_id); });
        addEvent(findForm(from_box), 'submit', function() { SelectBox.select_all(field_id + '_to'); });
        SelectBox.init(field_id + '_from');
        SelectBox.init(field_id + '_to');
        // Move selected from_box options to to_box
        SelectBox.move(field_id + '_from', field_id + '_to');

        // Initial icon refresh
        SelectFilter.refresh_icons(field_id);

        addEvent(filter_input, 'keypress', function(e) {SelectFilter.filter_key_press(e, field_id);});
        addEvent(filter_input, 'keyup', function(e) { SelectFilter.filter_key_up(e, field_id); });
        addEvent(filter_input, 'keydown', function(e) { SelectFilter.filter_key_down(e, field_id); });

    },
    refresh_icons: function(field_id) {
        var from = $('#' + field_id + '_from');
        var to = $('#' + field_id + '_to');
        var is_from_selected = from.find('option:selected').length > 0;
        var is_to_selected = to.find('option:selected').length > 0;
        // Active if at least one item is selected
        $('#' + field_id + '_add_link').toggleClass('active', is_from_selected);
        $('#' + field_id + '_remove_link').toggleClass('active', is_to_selected);
        // Active if the corresponding box isn't empty
        $('#' + field_id + '_add_all_link').toggleClass('active', from.find('option').length > 0);
        $('#' + field_id + '_remove_all_link').toggleClass('active', to.find('option').length > 0);
    },
    filter_key_up: function(event, field_id) {
        var from = document.getElementById(field_id + '_from');
        // don't submit form if user pressed Enter
        if ((event.which && event.which == 13) || (event.keyCode && event.keyCode == 13)) {
            from.selectedIndex = 0;
            SelectBox.move(field_id + '_from', field_id + '_to');
            from.selectedIndex = 0;
            return false;
        }
        var temp = from.selectedIndex;
        SelectBox.filter(field_id + '_from', document.getElementById(field_id + '_input').value);
        from.selectedIndex = temp;
        return true;
    },
    filter_key_down: function(event, field_id) {
        var from = document.getElementById(field_id + '_from');
        // right arrow -- move across
        if ((event.which && event.which == 39) || (event.keyCode && event.keyCode == 39)) {
            var old_index = from.selectedIndex;
            SelectBox.move(field_id + '_from', field_id + '_to');
            from.selectedIndex = (old_index == from.length) ? from.length - 1 : old_index;
            return false;
        }
        // down arrow -- wrap around
        if ((event.which && event.which == 40) || (event.keyCode && event.keyCode == 40)) {
            from.selectedIndex = (from.length == from.selectedIndex + 1) ? 0 : from.selectedIndex + 1;
        }
        // up arrow -- wrap around
        if ((event.which && event.which == 38) || (event.keyCode && event.keyCode == 38)) {
            from.selectedIndex = (from.selectedIndex == 0) ? from.length - 1 : from.selectedIndex - 1;
        }
        return true;
    }
}

})(django.jQuery);
