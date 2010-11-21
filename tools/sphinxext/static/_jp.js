$(document).ready(function() {
    var url = document.URL.replace(/#.*/, '');
    var parts = url.split('/');

    var base = 'http://docs.python.org/2.6/';
    base += parts[parts.length-2] + '/' + parts[parts.length-1];
    $('a.headerlink').each(function() {
            var html = '<a href="' + base + $(this).attr('href') +
                       '" class="reference internal" title="原文へのリンク">原文</a>';
            $(this).after(html);
        })
});
