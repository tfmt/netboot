$(function() {
    var activeNavId = $('body').data('active-nav-id');

    if (activeNavId) {
        $('[data-nav-id="' + activeNavId + '"]').addClass('uk-active');
    }
});
