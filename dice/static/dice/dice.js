var platform = $('#platform');

function dado() {
    platform.removeClass('stop').addClass('playing');
    var number = Math.floor(Math.random() * 6) + 1;
    $('input#side').val(number);
    setTimeout(function () {
        platform.removeClass('playing').addClass('stop');
        var letters = ['B', 'A', 'C', 'E', 'F', 'D'];
        var x = 0, y = 20, z = -20;
        switch (number) {
            case 1:
                x = 0;
                y = 20;
                z = -20;
                break;
            case 2:
                x = -100;
                y = -150;
                z = 10;
                break;
            case 3:
                x = 0;
                y = -100;
                z = -10;
                break;
            case 4:
                x = 0;
                y = 100;
                z = -10;
                break;
            case 5:
                x = 80;
                y = 120;
                z = -10;
                break;
            case 6:
                x = 0;
                y = 200;
                x = 10;
                break;
        }

        $('#dice').css({
            'transform': 'rotateX(' + x + 'deg) rotateY(' + y + 'deg) rotateZ(' + z + 'deg)'
        });

        platform.css({
            'transform': 'translate3d(0,0, 0px)'
        });

        $('#outcome').text(letters[number - 1]);
    }, 1120);
}