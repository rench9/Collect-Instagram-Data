type = ['', 'info', 'success', 'warning', 'danger'];


demo = {
    initPickColor: function () {
        $('.pick-class-label').click(function () {
            var new_class = $(this).attr('new-class');
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if (display_div.length) {
                var display_buttons = display_div.find('.btn');
                display_buttons.removeClass(old_class);
                display_buttons.addClass(new_class);
                display_div.attr('data-class', new_class);
            }
        });
    },

    initChartist: function () {

        var dataSales = {
            labels: ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
            series: [
                [287, 385, 490, 492, 554, 586, 698, 695, 752, 788, 846, 944],
                [67, 152, 143, 240, 287, 335, 435, 437, 539, 542, 544, 647],
                [23, 113, 67, 108, 190, 239, 307, 308, 439, 410, 410, 509]
            ]
        };

        var optionsSales = {
            lineSmooth: false,
            low: 0,
            high: 800,
            showArea: true,
            height: "245px",
            axisX: {
                showGrid: false,
            },
            lineSmooth: Chartist.Interpolation.simple({
                divisor: 3
            }),
            showLine: false,
            showPoint: false,
        };

        var responsiveSales = [
            ['screen and (max-width: 640px)', {
                axisX: {
                    labelInterpolationFnc: function (value) {
                        return value[0];
                    }
                }
            }]
        ];

        Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);


        var data = {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            series: [
                [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
                [412, 243, 280, 580, 453, 353, 300, 364, 368, 410, 636, 695]
            ]
        };

        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };

        var responsiveOptions = [
            ['screen and (max-width: 640px)', {
                seriesBarDistance: 5,
                axisX: {
                    labelInterpolationFnc: function (value) {
                        return value[0];
                    }
                }
            }]
        ];

        Chartist.Bar('#chartActivity', data, options, responsiveOptions);

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };

        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };

        Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        Chartist.Pie('#chartPreferences', {
            labels: ['62%', '32%', '6%'],
            series: [62, 32, 6]
        });
    },

    initGoogleMaps: function () {
        var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
        var mapOptions = {
            zoom: 13,
            center: myLatlng,
            scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
            styles: [{
                "featureType": "water",
                "stylers": [{"saturation": 43}, {"lightness": -11}, {"hue": "#0088ff"}]
            }, {
                "featureType": "road",
                "elementType": "geometry.fill",
                "stylers": [{"hue": "#ff0000"}, {"saturation": -100}, {"lightness": 99}]
            }, {
                "featureType": "road",
                "elementType": "geometry.stroke",
                "stylers": [{"color": "#808080"}, {"lightness": 54}]
            }, {
                "featureType": "landscape.man_made",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ece2d9"}]
            }, {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ccdca1"}]
            }, {
                "featureType": "road",
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#767676"}]
            }, {
                "featureType": "road",
                "elementType": "labels.text.stroke",
                "stylers": [{"color": "#ffffff"}]
            }, {"featureType": "poi", "stylers": [{"visibility": "off"}]}, {
                "featureType": "landscape.natural",
                "elementType": "geometry.fill",
                "stylers": [{"visibility": "on"}, {"color": "#b8cb93"}]
            }, {"featureType": "poi.park", "stylers": [{"visibility": "on"}]}, {
                "featureType": "poi.sports_complex",
                "stylers": [{"visibility": "on"}]
            }, {"featureType": "poi.medical", "stylers": [{"visibility": "on"}]}, {
                "featureType": "poi.business",
                "stylers": [{"visibility": "simplified"}]
            }]

        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            title: "Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);
    },

    showNotification: function (from, align) {
        color = Math.floor((Math.random() * 4) + 1);

        $.notify({
            icon: "pe-7s-gift",
            message: "Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer."

        }, {
            type: type[color],
            timer: 4000,
            placement: {
                from: from,
                align: align
            }
        });
    }


};

var dashboard = {
    loadcounts: function () {
        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/tablecount",
            data: {},
            success: function (data) {
                $("#c_usersinfo").html(data['data']['usersinfo']);
                $("#c_brands").html(data['data']['brands']);
                $("#c_followers").html(data['data']['followers']);
                $("#c_hashtags").html(data['data']['hashtag']);
                $("#c_posts").html(data['data']['post']);
                $("#c_timeseries").html(data['data']['timeseries']);
                console.log(data)
            }

        });
    },
};

var accounts = {
    login: function () {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/accountslogin",
            data: {
                un: $("#username").val(),
                pw: $("#password").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                location.reload(true)
            }

        });


    }
}

var notification = {
    load: function (category) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/logs",
            data: {
                id: $('.notification-card').last().data('id') ? $('.notification-card').last().data('id') : 0,
                category: category,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {

                console.log(data)
                data['data'].forEach(function (d) {
                    var i = $('<div data-id="' + d['id'] + '" class="alert alert-with-icon notification-card">\n' +
                        '<button type="button" data-time="' + d['timestamp'] + '" aria-hidden="true" class="close">×</button>\n' +
                        '<span data-notify="icon" class="pe-7s-bell"></span>\n' +
                        '<span><b> ' + d['title'] + ' - </b> ' + d['desc'] + '</span>\n' +
                        '</div>');


                    if (d['code'] == 1)
                        $(i).addClass('alert-info');
                    else if (d['code'] == 2)
                        $(i).addClass('alert-warning');
                    else if (d['code'] == 3)
                        $(i).addClass('alert-danger');
                    else if (d['code'] == 4)
                        $(i).addClass('alert-success');


                    $("#loader").before(i)
                });
                loader.hide($('.loader'));
            }

        });
    }
}

var scrapping = {
    scrape: function (e) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/scrape",
            data: {
                un: $("#id_username").val(),
                category: $("input[name='user_radio']:checked").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                console.log(data)
                if (data['data']) {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "Done !"

                    }, {
                        type: 'info',
                        timer: 500
                    });
                    loader.resetButton(e);
                }
                else {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "Error !"

                    }, {
                        type: 'info',
                        timer: 500
                    });
                    loader.resetButton(e);
                }
            }

        });
    },
    massScrape: function (category, e) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/massscrape",
            data: {
                category: category,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                console.log(data)
                if (data['data']) {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "Done !"

                    }, {
                        type: 'info',
                        timer: 500
                    });
                    loader.resetButton(e);
                }
                else {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "Error !"

                    }, {
                        type: 'info',
                        timer: 500
                    });
                    loader.resetButton(e);
                }
            }

        });

    }
}

var importExport = {

    _import: function () {
        var form = new FormData()

        form.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
        form.append('file', $('input[name="csvfile"]')[0].files[0])

        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/import",
            data: form,
            success: function (data) {
                console.log(data)
            },
            cache: false,
            contentType: false,
            processData: false,


        });
    },
    _export: function () {
        window.location = "/post/export?name=" + $('#file-name').val()
    }
}

var profiles = {
    append: function () {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/profiles",
            data: {
                sort: $("input[name='filter-sort']:checked").val(),
                private: $("#filter-private").prop('checked'),
                public: $("#filter-public").prop('checked'),
                brands: $("#filter-brand").prop('checked'),
                order: $("input[name='user_order']:checked").val(),
                lastuser: $('.user-card').last().data('username'),
                lastactive: $('.user-card').last().data('lastactive'),
                followers: $('.user-card').last().data('followers'),
                engagement: $('.user-card').last().data('engagement'),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                range: $("#followers-range").prop("value"),
                list: $("#list").val(),
            },
            success: function (data) {
                console.log(data);
                data['data'].forEach(function (d) {
                    $('#showmoreusers').before('<div class="col-md-3 col-sm-6 col-xs-12 user-card" data-fullname="' + d['fullname'] + '" data-id="' + d['row_id'] + '" data-engagement="' + d['engagement'] + '" data-username="' + d['username'] + '" data-userid="' + d['userid'] + '" data-isprivate="' + d['isprivate'] + '" data-isbusiness="' + d['email'] + '" data-followers="' + d['followed_by'] + '" data-following="' + d['follows'] + '" data-cmnt="' + d['comments_count'] + '" data-like="' + d['likes_count'] + '">\n' +
                        '<div class="card card-user">\n' +
                        '<div class="image">\n' +
                        '<i data-userid="' + d['userid'] + '" class="card-close pe-7s-close"></i><i data-id="' + d['row_id'] + '" class="card-stat pe-7s-graph1"></i>\n' +
                        '<img onerror="profiles.altImg(this)" src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '</div>\n' +
                        '<div class="content" >\n' +
                        '<div class="author">\n' +
                        '<a href="#">\n' +
                        '<img  onerror="profiles.altImg(this)" class="avatar border-gray"\n' +
                        ' src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '\n' +
                        '<h4 class="title">' + d['fullname'] + '<br>\n' +
                        '<small>' + d['username'] + (d['is_verified'] ? '<i title="Verified" style="color: #3897f0;" class="fa fa-check-circle"></i>' : '') + (d['is_business'] ? '<i title="Business" style="color: #7a3838;" class="fa fa-briefcase"></i>' : '') + '</small>\n' +
                        '</h4>\n' +
                        '</a>\n' +
                        '</div>\n' +
                        '<hr style="margin-left: 0px;margin-right: 0px;">\n' +
                        '<div class="card-stats" >\n' +
                        '<h6>Followers: <span style="float: right;">' + d['followed_by'] + '</span></h6>\n' +
                        '<h6>Following: <span style="float: right;">' + d['follows'] + '</span></h6>\n' +
                        '<h6>Comments: <span style="float: right;">' + d['comments_count'] + '</span></h6>\n' +
                        '<h6>Likes: <span style="float: right;">' + d['likes_count'] + '</span></h6><h6>Engagement: <span style="float: right;">' + d['engagement'] + '</span></h6>\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '<hr>\n' +
                        '<div class="text-center">\n' +
                        '<a target="_blank" href="/profile?un=' + d['username'] + '" class="btn btn-simple"><i class="fa fa-circle"></i>\n' +
                        'VISIT PROFILE\n' +
                        '</a>\n' +
                        '\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '</div>')

                });
                // loader.hide($('.loader'))

            }

        });
    },
    altImg: function (e) {
        e.src = 'http://via.placeholder.com/800x800';
    },
    search: function (query) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/profiles/search",
            data: {
                cat: $("#search-query").val(),
                query: query,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                console.log(data);
            }

        });

    },
    appendProfile: function (username) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/profile",
            data: {
                un: username,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                console.log(data);
                data['data'].forEach(function (d) {
                    $('#profiles').append('<div class="col-md-3 col-sm-6 col-xs-12 user-card" data-fullname="' + d['fullname'] + '" data-id="' + d['row_id'] + '" data-engagement="' + d['engagement'] + '" data-username="' + d['username'] + '" data-userid="' + d['userid'] + '" data-isprivate="' + d['isprivate'] + '" data-isbusiness="' + d['email'] + '" data-followers="' + d['followed_by'] + '" data-following="' + d['follows'] + '" data-cmnt="' + d['comments_count'] + '" data-like="' + d['likes_count'] + '">\n' +
                        '<div class="card card-user">\n' +
                        '<div class="image">\n' +
                        '<i data-userid="' + d['userid'] + '" class="card-close pe-7s-close"></i><i data-id="' + d['row_id'] + '" class="card-stat pe-7s-graph1"></i>\n' +
                        '<img onerror="profiles.altImg(this)" src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '</div>\n' +
                        '<div class="content" >\n' +
                        '<div class="author">\n' +
                        '<a href="#">\n' +
                        '<img  onerror="profiles.altImg(this)" class="avatar border-gray"\n' +
                        ' src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '\n' +
                        '<h4 class="title">' + d['fullname'] + '<br>\n' +
                        '<small>' + d['username'] + (d['is_verified'] ? '<i title="Verified" style="color: #3897f0;" class="fa fa-check-circle"></i>' : '') + (d['is_business'] ? '<i title="Business" style="color: #7a3838;" class="fa fa-briefcase"></i>' : '') + '</small>\n' +
                        '</h4>\n' +
                        '</a>\n' +
                        '</div>\n' +
                        '<hr style="margin-left: 0px;margin-right: 0px;">\n' +
                        '<div class="card-stats" >\n' +
                        '<h6>Followers: <span style="float: right;">' + d['followed_by'] + '</span></h6>\n' +
                        '<h6>Following: <span style="float: right;">' + d['follows'] + '</span></h6>\n' +
                        '<h6>Comments: <span style="float: right;">' + d['comments_count'] + '</span></h6>\n' +
                        '<h6>Likes: <span style="float: right;">' + d['likes_count'] + '</span></h6><h6>Engagement: <span style="float: right;">' + d['engagement'] + '</span></h6>\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '<hr>\n' +
                        '<div class="text-center">\n' +
                        '<a target="_blank" href="/profile?un=' + d['username'] + '" class="btn btn-simple"><i class="fa fa-circle"></i>\n' +
                        'VISIT PROFILE\n' +
                        '</a>\n' +
                        '\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '</div>')

                });

            }

        });


    },
}

var loader = {
    show: function (e) {
        e.css('visibility', 'visible');
    },
    hide: function (e) {
        e.css('visibility', 'hidden');
    },
    isVisible: function (e) {
        $.fn.isOnScreen = function () {

            var win = $(window);

            var viewport = {
                top: win.scrollTop(),
                left: win.scrollLeft()
            };
            viewport.right = viewport.left + win.width();
            viewport.bottom = viewport.top + win.height();

            var bounds = this.offset();
            bounds.right = bounds.left + this.outerWidth();
            bounds.bottom = bounds.top + this.outerHeight();

            return (!(viewport.right < bounds.left || viewport.left > bounds.right || viewport.bottom < bounds.top || viewport.top > bounds.bottom));

        };

        if (e.isOnScreen() && e.css('visibility') == 'hidden')
            return true;
        else
            return false;


    },
    loadButton: function (e) {
        $(e).button('loading');
    },
    resetButton: function (e) {
        $(e).button('reset');
    }


}

var schedule = {
    trigger: function (elem, cat, event) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/schedule",
            data: {
                cat: cat,
                event: event,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                if (data['data']) {
                    if (cat == 'ts') {
                        if (event == 'start') {

                            $(elem).addClass('hidden');
                            $('#sd-pause, #sd-stop').removeClass('hidden');

                        }
                        else if (event == 'stop') {
                            $(elem).addClass('hidden');
                            $('#sd-pause, #sd-resume').addClass('hidden');
                            $('#sd-start').removeClass('hidden');

                        }
                        else if (event == 'pause') {
                            $(elem).addClass('hidden');
                            $('#sd-resume').removeClass('hidden');

                        }
                        else if (event == 'resume') {
                            $(elem).addClass('hidden');
                            $('#sd-pause').removeClass('hidden');

                        }

                    }
                    else if (cat == 'ui') {
                        if (event == 'start') {
                            $(elem).addClass('hidden');
                            $('#ui-pause, #ui-stop').removeClass('hidden');

                        }
                        else if (event == 'stop') {
                            $(elem).addClass('hidden');
                            $('#ui-pause, #ui-resume').addClass('hidden');
                            $('#ui-start').removeClass('hidden');

                        }
                        else if (event == 'pause') {
                            $(elem).addClass('hidden');
                            $('#ui-resume').removeClass('hidden');

                        }
                        else if (event == 'resume') {
                            $(elem).addClass('hidden');
                            $('#ui-pause').removeClass('hidden');

                        }
                    }
                }
            }

        });


    },
    loadMessage: function (oid, elem) {
        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/output",
            data: {
                oid: oid,
                lid: isNaN(parseInt($(elem).attr('data-lid'))) ? 0 : parseInt($(elem).attr('data-lid')),
                // lid: $(elem).data('lid') ? $(elem).data('lid') : 0,
            },
            success: function (data) {
                data['data'].forEach(function (d) {
                    if (parseInt($(elem).data('lid')) < d['id'] || isNaN(parseInt($(elem).data('lid')))) {
                        $(elem).attr('data-lid', d['id'])
                    }

                    date = new Date(d['timestamp']);
                    $(elem).prepend('<tr>\n' +
                        '<td>' + d['message'] + '</td>\n' +
                        '<td>' + $.datepicker.formatDate("yy-mm-dd " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds(), date) + '</td>\n' +
                        '</tr>');
                });

            }

        });

    }
}

var search = {
    appendProfile: function (username) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/profile",
            data: {
                un: username,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                console.log(data);
                data['data'].forEach(function (d) {
                    $('#profiles').append('<div class="col-md-3 col-sm-6 col-xs-12 user-card" data-fullname="' + d['fullname'] + '" data-id="' + d['row_id'] + '" data-engagement="' + d['engagement'] + '" data-username="' + d['username'] + '" data-userid="' + d['userid'] + '" data-isprivate="' + d['isprivate'] + '" data-isbusiness="' + d['email'] + '" data-followers="' + d['followed_by'] + '" data-following="' + d['follows'] + '" data-cmnt="' + d['comments_count'] + '" data-like="' + d['likes_count'] + '">\n' +
                        '<div class="card card-user">\n' +
                        '<div class="image">\n' +
                        '<i data-userid="' + d['userid'] + '" class="card-close pe-7s-close"></i><i data-id="' + d['row_id'] + '" class="card-stat pe-7s-graph1"></i>\n' +
                        '<img onerror="profiles.altImg(this)" src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '</div>\n' +
                        '<div class="content" >\n' +
                        '<div class="author">\n' +
                        '<a href="#">\n' +
                        '<img  onerror="profiles.altImg(this)" class="avatar border-gray"\n' +
                        ' src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '\n' +
                        '<h4 class="title">' + d['fullname'] + '<br>\n' +
                        '<small>' + d['username'] + (d['is_verified'] ? '<i title="Verified" style="color: #3897f0;" class="fa fa-check-circle"></i>' : '') + (d['is_business'] ? '<i title="Business" style="color: #7a3838;" class="fa fa-briefcase"></i>' : '') + '</small>\n' +
                        '</h4>\n' +
                        '</a>\n' +
                        '</div>\n' +
                        '<hr style="margin-left: 0px;margin-right: 0px;">\n' +
                        '<div class="card-stats" >\n' +
                        '<h6>Followers: <span style="float: right;">' + d['followed_by'] + '</span></h6>\n' +
                        '<h6>Following: <span style="float: right;">' + d['follows'] + '</span></h6>\n' +
                        '<h6>Comments: <span style="float: right;">' + d['comments_count'] + '</span></h6>\n' +
                        '<h6>Likes: <span style="float: right;">' + d['likes_count'] + '</span></h6><h6>Engagement: <span style="float: right;">' + d['engagement'] + '</span></h6>\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '<hr>\n' +
                        '<div class="text-center">\n' +
                        '<a target="_blank" href="/profile?un=' + d['username'] + '" class="btn btn-simple"><i class="fa fa-circle"></i>\n' +
                        'VISIT PROFILE\n' +
                        '</a>\n' +
                        '\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '</div>')

                });

            }

        });


    },
    save_list: function () {
        _list = [];
        $.each($('.user-card'), function (index, item) {
            _list.push($(item).data('username'));
        });
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/createlist",
            data: {
                action: 'save',
                list: $('#list-name').data('name'),
                values: _list.toString(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                if (data['status'] == "updated" || data['status'] == "created") {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "List <b>" + $('#list-name').data('name') + "</b> saved!"

                    }, {
                        type: 'info',
                        timer: 500
                    });

                }
            }

        });

    },
    del_list: function () {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/createlist",
            data: {
                action: 'del',
                list: $('#list-name').data('name'),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                if (data['status'] == 'deleted') {
                    if (data['status'] == "deleted") {
                        $.notify({
                            icon: 'pe-7s-info',
                            message: "List <b>" + $('#list-name').data('name') + "</b> deleted!"

                        }, {
                            type: 'info',
                            timer: 500
                        });

                    }
                    $('#create-link, #load-link').removeClass("hidden");
                    $('#list-link,#del-list,#save-list').addClass("hidden");
                    $('#list-name').removeData('name');
                    $('#list-name').text('');


                }
            }

        });

    },
    load_list: function () {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/createlist",
            data: {
                action: 'load',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                $('#loadList tbody').empty();

                data['data'].forEach(function (d, i) {
                    $('#loadList tbody').append('<tr>\n' +
                        '    <td>' + (i + 1) + '</td>\n' +
                        '    <td><a class="list-links" href="" data-name="' + d['name'] + '">' + d['name'] + '</a></td>\n' +
                        '    <td>' + d['items'].split(',').length + '</td>\n' +
                        '\n' +
                        '</tr>')

                });
                $("#loadList").modal();
            }

        });

    },
    loadProfiles: function (listname) {
        $.ajax({
            type: 'POST',
            async: true,
            url: "./post/createlist",
            data: {
                action: 'loadprofiles',
                ln: listname,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                window._lists[listname] = data['data']
                $("#loadList").modal("hide");
                $('#create-link').addClass("hidden");
                $('#load-link').addClass("hidden");
                $('#list-link,#del-list,#save-list').removeClass("hidden");
                $('#list-name').data('name', data['ln']);
                $('#list-name').text(data['ln']);
                $('#profiles').empty();
                console.log(data);
                data['data'].forEach(function (d) {
                    $('#profiles').append('<div class="col-md-3 col-sm-6 col-xs-12 user-card" data-fullname="' + d['fullname'] + '" data-id="' + d['row_id'] + '" data-engagement="' + d['engagement'] + '" data-username="' + d['username'] + '" data-userid="' + d['userid'] + '" data-isprivate="' + d['isprivate'] + '" data-isbusiness="' + d['email'] + '" data-followers="' + d['followed_by'] + '" data-following="' + d['follows'] + '" data-cmnt="' + d['comments_count'] + '" data-like="' + d['likes_count'] + '">\n' +
                        '<div class="card card-user">\n' +
                        '<div class="image">\n' +
                        '<i data-userid="' + d['userid'] + '" class="card-close pe-7s-close"></i><i data-id="' + d['row_id'] + '" class="card-stat pe-7s-graph1"></i>\n' +
                        '<img onerror="profiles.altImg(this)" src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '</div>\n' +
                        '<div class="content" >\n' +
                        '<div class="author">\n' +
                        '<a href="#">\n' +
                        '<img  onerror="profiles.altImg(this)" class="avatar border-gray"\n' +
                        ' src="' + d['profilepicture'] + '"\n' +
                        ' alt="...">\n' +
                        '\n' +
                        '<h4 class="title">' + d['fullname'] + '<br>\n' +
                        '<small>' + d['username'] + (d['is_verified'] ? '<i title="Verified" style="color: #3897f0;" class="fa fa-check-circle"></i>' : '') + (d['is_business'] ? '<i title="Business" style="color: #7a3838;" class="fa fa-briefcase"></i>' : '') + '</small>\n' +
                        '</h4>\n' +
                        '</a>\n' +
                        '</div>\n' +
                        '<hr style="margin-left: 0px;margin-right: 0px;">\n' +
                        '<div class="card-stats" >\n' +
                        '<h6>Followers: <span style="float: right;">' + d['followed_by'] + '</span></h6>\n' +
                        '<h6>Following: <span style="float: right;">' + d['follows'] + '</span></h6>\n' +
                        '<h6>Comments: <span style="float: right;">' + d['comments_count'] + '</span></h6>\n' +
                        '<h6>Likes: <span style="float: right;">' + d['likes_count'] + '</span></h6><h6>Engagement: <span style="float: right;">' + d['engagement'] + '</span></h6>\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '<hr>\n' +
                        '<div class="text-center">\n' +
                        '<a target="_blank" href="/profile?un=' + d['username'] + '" class="btn btn-simple"><i class="fa fa-circle"></i>\n' +
                        'VISIT PROFILE\n' +
                        '</a>\n' +
                        '\n' +
                        '</div>\n' +
                        '</div>\n' +
                        '</div>')

                });

            }

        });


    },
    loadStats: function (elem, duration) {


        user = $('.user-card[data-id="' + $(elem).data('id') + '"]');
        $('#modalstats .modal-title').text(user.data('fullname'));
        $('#modalstats .modal-title').data('id', user.data('id'));

        $('#modalstats a.duration').each(function (e, obj) {

            $(obj).attr("data-id", user.data('id'));
        });


        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/stats",
            data: {
                row_id: user.data('id'),
                duration: duration,
            },
            success: function (data) {
                updateStatsModal(data);
            }

        });


    }
}

var profile = {
    loadStat: function (userId, duration) {

        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/stats",
            data: {
                row_id: userId,
                duration: duration,
            },
            success: function (data) {
                updateStatsModal(data);

            }

        });

    }
}

var list = {
    load_saveList: function () {
        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/list",
            data: {
                action: "load",
                sub_action: 'save'
            },
            success: function (data) {
                var i = 0;
                $('#loadList tbody').empty();
                data['data'].forEach(function (d) {
                    i = i + 1;
                    $('#loadList tbody').append('<tr>\n' +
                        '<td>' + (i) + '</td>\n' +
                        '<td><a class="list-add" href="" data-name="' + d['name'] + '">' + d['name'] + '</a></td>\n' +
                        '<td>' + (d['items'] == null ? 0 : d['items'].split(',').length) + '</td>\n' +
                        '</tr>');
                });
            }

        });

    },
    load_delList: function (items) {
        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/list",
            data: {
                action: "load",
                sub_action: 'del',
                items: items.toString()
            },
            success: function (data) {
                var i = 0;
                $('#loadList tbody').empty();
                data['data'].forEach(function (d) {
                    i = i + 1;
                    $('#loadList tbody').append('<tr>\n' +
                        '<td>' + (i) + '</td>\n' +
                        '<td><a class="list-del" href="" data-name="' + d['name'] + '">' + d['name'] + '</a></td>\n' +
                        '<td>' + d['items'].split(',').length + '</td>\n' +
                        '</tr>');
                });
            }

        });

    },
    save: function (name, items) {
        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/list",
            data: {
                action: "save",
                name: name,
                items: items.toString()
            },
            success: function (data) {
                if (data['data'] == 'updated' || data['data'] == 'created') {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "<b>" + items.toString() + "</b> " + data['data'] + " to list " + name

                    }, {
                        type: 'info',
                        timer: 500
                    });

                }
            }

        });

    },
    delete: function (name, items) {
        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/list",
            data: {
                action: "del",
                name: name,
                items: items.toString()
            },
            success: function (data) {

                if (data['data'] == 'deleted') {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "<b>" + items.toString() + "</b> deleted from list " + name

                    }, {
                        type: 'info',
                        timer: 500
                    });

                }

            }

        });

    },
    create: function (name) {

        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/list",
            data: {
                action: "create",
                name: name,
                // items: items.toString()
            },
            success: function (data) {
                if (data['data'] == 'exist' || data['data'] == 'created') {
                    $.notify({
                        icon: 'pe-7s-info',
                        message: "<b>" + name + "</b> list " + data['data'] + '!'

                    }, {
                        type: 'info',
                        timer: 500
                    });

                }

            }

        });
    },
    updateListProfiles: function () {
        $.ajax({
            type: 'GET',
            async: true,
            url: "./get/list",
            data: {
                action: "load",
                sub_action: 'save'
            },
            success: function (data) {
                var i = 0;
                $('#filter-lists').empty();
                data['data'].forEach(function (d) {
                    i = i + 1;
                    $('#filter-lists').append('<li><a href="#" data-name="' + d['name'] + '">' + d['name'] + '</a></li>');
                    // $('#loadList tbody').append('<tr>\n' +
                    //     '<td>' + (i) + '</td>\n' +
                    //     '<td><a class="list-add" href="" data-name="' + d['name'] + '">' + d['name'] + '</a></td>\n' +
                    //     '<td>' + (d['items'] == null ? 0 : d['items'].split(',').length) + '</td>\n' +
                    //     '</tr>');
                });
                $('#filter-lists').append('<li class="divider"></li>');
                $('#filter-lists').append('<li><a href="#" data-name="_all">Whole</a></li>');

            }

        });
    }
}

function updateStatsModal(data) {
    _label = []
    _f = []
    _l = []
    _c = []


    data['data'].forEach(function (d) {
        date = new Date(d['timestamp']);
        _label.push($.datepicker.formatDate("dd-M-y", date));
        _f.push(d['followed_by']);
        _l.push(d['likes_count']);
        _c.push(d['comments_count']);

    });
    var getMax = function (_array) {

        num = Math.max.apply(Math, _array);
        if (num.toString().length > 2) {
            ceil = Math.floor(num / (Math.pow(10, (num.toString().length - 2 )))) + 1
            return ceil * (Math.pow(10, (num.toString().length - 2 )));
        }
        else {

            return (Math.floor(num / 10) + 1) * 10
        }
    };

    var getMin = function (_array) {

        num = Math.min.apply(Math, _array);
        if (num.toString().length > 2) {
            ceil = Math.floor(num / (Math.pow(10, (num.toString().length - 2 )))) - 1
            return ceil * (Math.pow(10, (num.toString().length - 2 )));
        }
        else {
            if (num < 10)
                return (Math.floor(num / 10)) * 10
            else
                return (Math.floor(num / 10) - 1) * 10
        }
    }


    window.fChart.config.data.datasets[0].data = _f;
    window.lChart.config.data.datasets[0].data = _l;
    window.cChart.config.data.datasets[0].data = _c;

    window.fChart.config.data.labels = _label;
    window.lChart.config.data.labels = _label;
    window.cChart.config.data.labels = _label;

    window.fChart.config.options.scales.yAxes[0].ticks.min = getMin(_f);
    window.fChart.config.options.scales.yAxes[0].ticks.max = getMax(_f);
    window.fChart.config.options.scales.yAxes[0].ticks.stepSize = (getMax(_f) - getMin(_f) ) / 10;

    window.lChart.config.options.scales.yAxes[0].ticks.min = getMin(_l);
    window.lChart.config.options.scales.yAxes[0].ticks.max = getMax(_l);
    window.lChart.config.options.scales.yAxes[0].ticks.stepSize = (getMax(_l) - getMin(_l) ) / 10;

    window.cChart.config.options.scales.yAxes[0].ticks.min = getMin(_c);
    window.cChart.config.options.scales.yAxes[0].ticks.max = getMax(_c);
    window.cChart.config.options.scales.yAxes[0].ticks.stepSize = (getMax(_c) - getMin(_c) ) / 10;

    window.fChart.update();
    window.cChart.update();
    window.lChart.update();
    if (_label.length > 0) {
        $('#modalstats').modal()
    } else {
        $.notify({
            icon: 'pe-7s-attention',
            message: "User don't have any TimeSeries data"

        }, {
            type: 'warning',
            timer: 500
        });
    }

}


/* new methods */

var _search = {
    populateList: function () {

    },

}

var _list = {
    loadList: function () {
        $.ajax({
            type: "GET",
            async: true,
            url: "./get/list",
            data: {
                action: "load",
                sub_action: 'save'
            },
            success: function (data) {
                window._lists = data['data'];

            }
        })
    }
}