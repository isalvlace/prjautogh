var Controller = {
    init: function() {
        $(document).on('click', '#sidebar-toggle', Controller.toggleSidebar);
    },

    toggleSidebar: function(event) {
        event.preventDefault();
        $('#sidebar').toggleClass('collapsed');
    }
};

$(document).ready(function() {
    Controller.init();
});