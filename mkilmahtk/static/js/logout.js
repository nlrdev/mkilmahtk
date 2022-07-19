$(function () {
    t = 6000
    i = 1000
    e = 1
    setTimeout(function () {
        window.location.href = "http://mkilmahtk.localhost/";
    }, t);
    start = performance.now();
    setInterval(function () {
        l = "0123456789ABCDEF";
        c = '';
        for (var x = 0; x < 6; x++)
            c += l[(Math.floor(Math.random() * 16))];
        $("#timer").html(Math.floor((t - (performance.now() - start)) / i) + e).fadeIn(e).fadeOut(i).css({
            'cssText': 'font-size:10rem !important',
            'color': "#" + c
        });
    }, i);
});