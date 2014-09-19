jQuery(document).ready(function($) {

    // softscrolling on internal links
    init_soft_scrolling();

    function init_soft_scrolling() {
        $('a.soft_scroll[href^="#"]').on('click',function (e) {
            if($(this).hasClass('carousel-control') === false) {
                e.preventDefault();
                var target = this.hash,
                $target = $(target);
                $('html, body').stop().animate({
                    'scrollTop': $target.offset().top
                }, 900, 'swing', function () {
                    window.location.hash = target;
                });
            }
        });
    }

});