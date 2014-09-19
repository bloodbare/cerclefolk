function visibilitat_inscripcions() {
    if ($('input#form-widgets-inscriptions_available-0').attr("checked")) {
      $("div#formfield-form-widgets-start_inscription").show("slow");
      $("div#formfield-form-widgets-end_inscription").show("slow");
    }
    else {
        $("div#formfield-form-widgets-start_inscription").hide("fast");
        $("div#formfield-form-widgets-end_inscription").hide("fast");
    }
}

jQuery(document).ready(function($) {

    // inscription fields visibility on add Esdeveniment form

    visibilitat_inscripcions();
    $('input#form-widgets-inscriptions_available-0').change(function() {
        visibilitat_inscripcions();
    });


    // quan canviem url via ajax, recarreguem links de compartir

    if (window.addthis) {
        $(window).on('hashchange', function(e){

            // horizontal links under page results
            $('.addthis_toolbox_faceted').attr('addthis:url', window.location);
            addthis.toolbox('.addthis_toolbox_faceted');

        });
    }

});
