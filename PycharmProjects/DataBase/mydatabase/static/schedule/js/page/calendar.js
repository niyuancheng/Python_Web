/*

Project     : DAdmin - Responsive Bootstrap HTML Admin Dashboard
Version     : 1.1
Author      : ThemeLooks
Author URI  : http://www.bootstrapmb.com/item/2664

*/

(function ($) {
     var event = [];
     $.ajax({
           url:"/handle/",
           type:'post',
           data:{"mes":"开始处理"},
           success:function(res){
                var data = res['data'];
                for(var i=0;i < data.length;i++){
                    event.push({
                         id:   data[i].id,
                         title: data[i].schedule,
                         start: data[i].sdate
                    });
                }
           }
     });
    "use strict";
    
    /* ------------------------------------------------------------------------- *
     * COMMON VARIABLES
     * ------------------------------------------------------------------------- */
    var $wn = $(window),
        $document = $(document),
        $body = $('body');

    $(function () {
        /* ------------------------------------------------------------------------- *
         * CALENDAR EVENTS
         * ------------------------------------------------------------------------- */
        var $calendarEvents = $('.calendar--events'),
            $calendarEventsEl = $calendarEvents.children('.fc-events'),
            $calendarEventEl = $calendarEventsEl.children('.fc-event'),
            $calendarEventsInput = $calendarEvents.find('.form-check-input');

        if ( $calendarEvents.length ) {
            $calendarEventEl.each(function () {
                var $el = $(this),
                    bgColor = $el.css('background-color');

                $el.draggable({
                        revert: true,
                        revertDuration: 0,
                        zIndex: 999,
                        cursor:"move"
                    })
                    .css({
                        'border-color': bgColor
                    })
                    .data('event', {
                        title: $el.text(),
                        color: bgColor,
                        stick: true
                    });
            });
        }

        $calendarEvents.on('click', '.calendar--event__colors li', function () {
            var $el = $(this);

            $el.addClass('active').siblings().removeClass('active');
        });
       
        $calendarEvents.on('submit', 'form', function (e) {
            alert("行程创建成功")
            e.preventDefault();
            var $el = $(this),
                $input = $el.children('input'),
                $event = $('<div></div>'),
                $colorClass = $calendarEvents.find('.calendar--event__colors .active'),
                $bdColor = $colorClass.css('background-color');

            $event.draggable({
                    revert: true,
                    revertDuration: 0,
                    zIndex: 999,
                    cursor:"move"

                })
                .css({
                    'border-color': $bdColor
                })
                .data('event', {
                    title: $input.val(),
                    color: $bdColor,
                    stick: true
                })
                .addClass( ' fc-event ' + $colorClass.attr('class') )
                .text( $input.val() )
                .appendTo($calendarEventsEl);
            
        });

        /* ------------------------------------------------------------------------- *
         * CALENDAR APP
         * ------------------------------------------------------------------------- */
        var $calendarApp = $('#calendarApp');

        if ( $calendarApp.length ) {
            $calendarApp.fullCalendar({
                header: {
                    left: '',
                    center: 'prev next title',
                    right: 'today basicDay basicWeek month',
                    title:'日历'
                },
                locale:'zh-cn',
                editable: true,
                droppable: true,
                stick:true,
                events:event,
                drop: function(date,draggedEI) {
                    var content = $(this).text();
                    if ( $calendarEventsInput.is(':checked') ) {
                        $(this).remove();
                    }
                    alert("行程添加成功");
                    //console.log(content);
                    var useDate = date.format('YYYY-MM-DD');
                    $.ajax({
                        type:"post",
                        url:"/schedule/",
                        data:{"date":useDate,"sche":content},
                        success:function(res){
                            data = res['data']

                            console.log("发送成功");
                        }
                    });
                },

               // eventClick:function(info){
               //     alert(info.event.title);
                //},

                eventDrop:function(event,dayDelta){
                     alert("行程修改成功");
                     var content = event.title;
                     var date = dayDelta;
                     console.log(thing);
                     $.ajax({
                        type:"get",
                        url:"/schedule/",
                        data:{"date_offset":date,"a_sche":content},
                        success:function(){
                            console.log("传送成功");
                        }
                    });
                },
                timeFormat: 'h(:mm)a',
            });
        }
        //删除事件
        $(document).on('click', '.btn_del', function (event) {
            alert("删除日程成功");
            console.log(event.id);
            //console.log($(this).data('id'));
            /*$.ajax({
                url:'/del/',
                type:'post',
                data:{"schedule":sche},
                success:function(res){
                    $calendarApp.fullCalender('removeEvents',res.id);
                    alert("删除日程成功");
                }

            });*/

            //$calendarApp.fullCalendar('removeEvents',1);
            //下面是删除某个，加载事件的时候添加id
            //id可以取数据库里的唯一编号
            //$calendarApp.fullCalendar('removeEvents',event.id);
        });
    });
}(jQuery));
