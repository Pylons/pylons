// Establish my own namespace
var PYREPORT = PYREPORT || {};

$(document).ready(function() {
    // Manipulate DOM to add the iframe, and move things around
    var iframe = $(document.createElement("iframe"));
    parent.XMLTRACE = $('#long_xml_version textarea').html();
    iframe.addClass('service_widget');
    iframe[0].src = "http://127.0.0.1:5005/bugtracks/widget";
    var newholder = $(document.createElement("div"));
    newholder.addClass('widget_layout');
    $('div.feature-highlight').wrapAll(newholder[0])[0].appendChild(
        $('button:last').remove()[0]);
    iframe.appendTo('div.widget_layout');
});
