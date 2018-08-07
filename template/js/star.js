$(document).ready(function(){


$.fn.starvalue = function() {
    return $(this).each(function() {
        // Get the value
        var val = parseFloat($(this).html());
        // Make sure that the value is in 0 - 5 range, multiply to get width
        var size = Math.max(0, (Math.min(5, val))) * 20;
        // Create stars holder
        var $span = $('<span id="starsize" />').width(size);
        // Replace the numerical value with stars
        $(this).html($span);
    });
}

$('span.starvalue').starvalue();


});
