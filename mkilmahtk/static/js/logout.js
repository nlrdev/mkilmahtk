$(function () {
    t = 6000
    i = 1000
    e = 1
    setTimeout(function () {
        window.location.href = "http://dochost.localhost/";
    }, t);
    start = performance.now();
    setInterval(function () {
        $("#timer").html(Math.floor((t - (performance.now() - start)) / i) + e).fadeIn(e).fadeOut(i)
    }, i);
});