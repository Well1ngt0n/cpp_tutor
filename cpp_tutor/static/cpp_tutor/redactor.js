var cur = 0;
var mx = 0;
var last = '';
var cur_letter = 0;
var lines = [""];
var paste = false;


var entityMap = {
    ' ': '&#8287;',
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
    '`': '&#x60;',
    '=': '&#x3D;'
};

function escapeHtml(string) {
    return String(string).replace(/[&<>"'`=\/]/g, function (s) {
        return entityMap[s];
    });
}

function getWidthOfText(txt) {
    $("#text").text(txt);
    return $("#text").width();
}

//$("#input").bind("paste", function(event){
//event.preventDefault();
//var text = window.clipboardData.getData("Text");
//console.log(text);
//});
$("#input").on('input', function () {
    console.log(2);
    text = lines[cur];
    if (!paste) {
        lines[cur] = text.substr(0, cur_letter) + $("#input").val() + text.substr(cur_letter, text.length);
        cur_letter += $("#input").val().length;
    } else {
        var p = $("#input").val().split('\n');
        for (let i = 0; i < p.length; i++) {
            p[i] = p[i].replace(String.fromCharCode(9), "    "); // Заменяем странные табы, которые ломают редактор
        }
        console.log(p);
        if (p.length >= 2) {
            lines[cur] = text.substr(0, cur_letter) + p[0];
            if (p.length >= 2) {
                for (let i = 1; i < p.length; i++) {
                    lines.splice(cur + i, 0, p[i]);
                }
            }
            lines[cur + p.length - 1] += text.substr(cur_letter);
            cur_letter = p[p.length - 1].length;
        } else {
            lines[cur] = text.substr(0, cur_letter) + p[0] + text.substr(cur_letter);
            cur_letter += p[p.length - 1].length;
        }
        cur = cur + p.length - 1;
        console.log(lines);
    }
    $("#input").val('');
    print_to_editor();
});
$("#input").keydown(function (event) {
    paste = false;
    $("#input").focus();
    if (event.key == "v" && event.ctrlKey) {
        paste = true;
        console.log(cur);
        return;
    }
    //event.preventDefault();
    if (event.key == "Tab") {
        event.preventDefault();
        lines[cur] = lines[cur].substr(0, cur_letter) + '    ' +
            lines[cur].substr(cur_letter + 1, lines[cur].length);
        cur_letter += 4;
    } else if (event.key == "Enter") {
        event.preventDefault();
        mx++;
        var enter_str = lines[cur].substr(cur_letter);
        lines[cur] = lines[cur].substr(0, cur_letter);
        cur_letter = enter_str.length;
        var nw = lines.slice(0, cur + 1);
        nw.push(enter_str);
        nw = nw.concat(lines.slice(cur + 1));
        lines = nw;
        cur_letter = 0;
        cur++;
    } else if (event.key == "Backspace") {
        event.preventDefault();
        cur_letter--;
        if (cur_letter == -1) {
            cur--;
            if (cur != -1) {
                cur_letter = lines[cur].length - 1;
                lines[cur] += lines[cur + 1];
                lines = lines.slice(0, cur + 1).concat(lines.slice(cur + 2));
                // Эта строка не работает
                //lines = lines.slice(0, cur + 1).concat(lines.slice(cur + 2, lines.length));
            } else {
                cur++;
            }
            cur_letter++;
        } else {
            lines[cur] = lines[cur].substr(0, cur_letter) + lines[cur].substr(cur_letter + 1);
        }
    } else if (event.key == "ArrowUp") {
        cur = Math.max(cur - 1, 0);
        cur_letter = Math.min(cur_letter, lines[cur].length);
    } else if (event.key == "ArrowDown") {
        cur = Math.min(lines.length - 1, cur + 1);
        cur_letter = Math.min(cur_letter, lines[cur].length);
    } else if (event.key == "ArrowRight") {
        cur_letter++;
        if (cur_letter > lines[cur].length) {
            if (cur < lines.length - 1) {
                cur++;
                cur_letter = 0;
            } else {
                cur_letter--;
            }
        }
    } else if (event.key == "ArrowLeft") {
        if (cur_letter == 0) {
            if (cur != 0) {
                cur--;
                cur_letter = lines[cur].length;
            }
        } else {
            cur_letter--;
        }
    }
    //else if (event.key.length == 1){
    //console.log(event.key);
    //text = lines[cur];
    //lines[cur] = text.substr(0, cur_letter) + event.key + text.substr(cur_letter, text.length);
    //cur_letter += event.key.length;
    //}
    print_to_editor();
});

function print_to_editor() {
    $("#cursor").css("left", getWidthOfText(lines[cur].substr(0, cur_letter)) + "px");
    //.log(cur_letter);
    $("#lines").empty();
    for (let i = 0; i < lines.length; i++) {
        let text = lines[i];
        let array = text.split(" ");
        let blue = ["if", "for", "while", "else", "namespace", "using"];
        let red = ["int", "long", "double", "string", "vector", "set", "map"];
        let orange = ["#include"];
        let res = '';
        for (let j = 0; j < array.length; j++) {
            let word = escapeHtml(array[j]);
            if (blue.indexOf(word) !== -1) {
                res += "<span class='blue'>" + word + "</span>";
            } else if (red.indexOf(word) !== -1) {
                res += "<span class='red'>" + word + "</span>";
            } else if (orange.indexOf(word) !== -1) {
                res += "<span class='orange'>" + word + "</span>";
            } else if (word !== "") {
                res += "<span class='gray'>" + word + "</span>";
            }
            if (j !== array.length - 1) {
                res += "<pre class='tab'> </pre>";
            }

        }

        $("#lines").append("<div class='line' id='#line-" + i + "'>" + res + "</div>");
        last = event.key;
    }
    //console.log(cur);
    $("#cursor").css("top", 15 * cur + "px");
}

$("#editor").on("click", function () {
    $("#input").focus();
});
$("#editor").on('click', '.line', function (e) {
    var c = this.id.split("-");
    cur = c[c.length - 1];
    //console.log(cur);
    $("#cursor").css("top", 15 * cur + "px");
    var len_str = "";
    var pos = $(this).offset();
    var elem_left = pos.left;

    var mn = Math.abs(0 - e.pageX + elem_left);
    var mn_id = 0;
    for (let i = 0; i < lines[cur].length; i++) {
        len_str += lines[cur][i];
        if (Math.abs(getWidthOfText(len_str) - e.pageX + elem_left) < mn) {
            mn = Math.abs(getWidthOfText(len_str) - e.pageX + elem_left);
            mn_id = i + 1;
        }
        cur_letter = mn_id;
        $("#cursor").css("left", getWidthOfText(lines[cur].substr(0, cur_letter)) + "px");
    }
    // Меняем текущую строку, достаем координаты курсора
    // Создаем span в который последовательно добавляем элементы
    // Таким образом ищем положение курсора
    // Вы гениальны
});

$("#start-testing-btn").on("click", function () {
    // $("#testing-system-answer").empty();
    $("#testing-system-answer").prepend("<p>На проверке...</p>");
    $.ajax({
        url: '/handler/',
        type: 'POST',
        data: {
            action: 'check-task',
            id_task: $("#id-task").text(),
            script: lines.join("\n"),
        }
    }).done(function (data) {
        location.reload()
        // $("#testing-system-answer").empty();
        // if (data.verdict === "complete solution") {
        //     $("#testing-system-answer").append("<p>complete solution</p>");
        // } else {
        //     $("#testing-system-answer").append("<p>" + data.verdict + "</p>");
        //     $("#testing-system-answer").append("<p>Input: " + data.input_p + "</p>");
        //     $("#testing-system-answer").append("<p>Program output: " + data.output_p + "</p>");
        //     $("#testing-system-answer").append("<p>Correct output: " + data.correct_output + "</p>");
        // }

    });
});

$("#start-btn").on("click", function(){
    $.ajax({
        url: '/handler/',
        type: 'POST',
        data: {
            action: 'run-code',
            script: lines.join('\n'),
            inpt: $("#input-block").val(),
        }
    }).done(function(data){
        if (data.answer === "error"){
            $("#output").text(data.error);
            $("#output-check").prop('checked', true);
        }
        else{
            $("#output").text(data.output);
            $("#output-check").prop('checked', true);
        }
    });
});