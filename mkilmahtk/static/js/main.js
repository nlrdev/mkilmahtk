$(function () {
    var minlength = 1;
    var req = null;
    $("#item_search").keyup(function () {
        clearInterval(itimer);
        t = 200
        i = 200
        e = 1
        start = performance.now();
        var timer
        var itimer = setInterval(function () {
            timer = Math.floor((t - (performance.now() - start)) / i) + e
            console.log(timer)
        }, i);
        setTimeout(function () {
            clearInterval(itimer);
            $("#search_load").show();
            // pretent to look busy incase email takes a sec...
            val = 0
            var loading_stuff = setInterval(function () {
                val += 1
                $(".progress-bar").css("width", val + "%").attr("aria-valuenow", val);
                if (val > 110) {
                    val = 0
                }
            }, 10);
            value = $("#item_search").val();
            if (value.length >= minlength && timer <= 0) {
                if (req != null) req.abort();
                req = $.ajax({
                    type: "POST",
                    data: {
                        action: "item_search",
                        search_value: value,
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').attr(
                            "value"
                        ),
                    },
                    dataType: "json",
                    error: function (request, error) {
                        console.log(arguments);
                        console.log(" Can't do because: " + error);
                    },
                    success: function (data) {
                        $("#search_load").hide();
                        console.log(loading_stuff)
                        clearInterval(itimer);
                        $("#search_wrapper").html(data.html);
                        $('[data-bs-toggle="tooltip"]').tooltip()
                    },
                });
            }
        }, t + 1);
    });

    $("#item_search_exact").keyup(function () {
        clearInterval(itimer);
        t = 200
        i = 200
        e = 1
        start = performance.now();
        var timer
        var itimer = setInterval(function () {
            timer = Math.floor((t - (performance.now() - start)) / i) + e
            console.log(timer)
        }, i);
        setTimeout(function () {
            clearInterval(itimer);
            $("#search_load").show();
            // pretent to look busy incase email takes a sec...
            val = 0
            var loading_stuff = setInterval(function () {
                val += 1
                $(".progress-bar").css("width", val + "%").attr("aria-valuenow", val);
                if (val > 110) {
                    val = 0
                }
            }, 10);
            value = $("#item_search_exact").val();
            if (value.length >= minlength && timer <= 0) {
                if (req != null) req.abort();
                req = $.ajax({
                    type: "POST",
                    data: {
                        action: "item_search_exact",
                        search_value: value,
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').attr(
                            "value"
                        ),
                    },
                    dataType: "json",
                    error: function (request, error) {
                        console.log(arguments);
                        console.log(" Can't do because: " + error);
                    },
                    success: function (data) {
                        $("#search_load").hide();
                        console.log(loading_stuff)
                        clearInterval(itimer);
                        $("#search_wrapper").html(data.html);
                        $('[data-bs-toggle="tooltip"]').tooltip()
                    },
                });
            }
        }, t + 1);
    });
});