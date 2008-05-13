$(document).ready(function() {
    var getProxyJSON = function(host, path, data, callback) {
        data['host'] = host;
        data['path'] = path;
        var uri = TRACEBACK.uri+'/relay';
        $.getJSON(uri, data, callback);
    };
    
    // Manipulate DOM to add the iframe, and move things around
    var newholder = $(document.createElement("div")).addClass('widget_layout');
    $('div.feature-highlight').wrapAll(newholder[0])[0].appendChild(
        $('button:last').remove()[0]);
    $('div.widget_layout')[0].appendChild(document.getElementById('service_widget'));
    
    var data = {
        q:'list:com.googlegroups.pylons-discuss list:python ' + $('code.main-exception').text(),
        mode:'json',
        page:1
    };
    
    $('#service_widget a.submit_traceback').click(function () {
        var uri = TRACEBACK.uri+'/post_traceback?debugcount='+debug_count
            +'&host='+encodeURIComponent(TRACEBACK.host)
            +'&path='+encodeURIComponent(TRACEBACK.traceback);
        $.getJSON(uri, function(data, textStatus) {
            var iframe = document.createElement("iframe");
            iframe.style.display = "none";
            document.body.appendChild(iframe);
            iframe.src = 'http://'+TRACEBACK.host+TRACEBACK.traceback
                +'/'+encodeURIComponent(data.traceback.link.replace(/\.xml/, ''))
                +'/reown?uuid='+encodeURIComponent(data.traceback.uuid);
            
            stuff = data;
        });
        return false;
    });
    // var searchResults = getProxyJSON('markmail.org', '/results.xqy', data,
    //     function(data, textStatus) {
    //         stuff = data;
    //     });
});
