
/* 
    v1.0, 210712

    함수 목록
    load_url(url)
    load_by_ajax_get(url, on_success, on_fail)
    load_by_ajax_post(url, post_data, on_success, on_fail)
*/

export function load_url(url) {

    location.href = url;
}

/*
1. url : ajax 통신할 url
2. on_success : 통신 성공했을 때 실행할 함수, data를 정보로 받는다.(JSONResponse)
3. on_fail : 통신 실패했을 때 실행할 함수
*/
export function load_by_ajax_get(url, on_success, on_fail) {

    let xhr = new XMLHttpRequest();
    xhr.open('get', url, true);
    xhr.onreadystatechange = function () {

        // 통신 완료.
        if (this.readyState == 4) {

            const data = JSON.parse(xhr.responseText);

            // 성공.
            if (this.status === 200) {
                if (on_success != null) {
                    on_success(data);
                }
            } else {
                if (on_fail != null) {
                    on_fail();
                }
            }
        }
    }
    xhr.send(null);
}


/*
1. url : ajax 통신할 url
2. post_data : post로 전송할 데이터.

post_data = "key1=" + "value1"
        + "&key2=" + "value2"
        + ...

3. on_success(data) : 통신 성공했을 때 실행할 함수, data를 정보로 받는다.(JSONResponse)
4. on_fail() : 통신 실패했을 때 실행할 함수
*/
export function load_by_ajax_post(url, post_data, on_success, on_fail) {

    let xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    // django에서 post 방식은 csrftoken 꼭 받아야 함.
    let csrftoken = getCookie('csrftoken');

    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onreadystatechange = function () {

        // 통신 완료.
        if (this.readyState == 4) {

            // 성공.
            if (this.status === 200) {

                if (on_success != null) {

                    let data = null;

                    if (xhr.responseText != null) {
                        data = JSON.parse(xhr.responseText);
                    }

                    if (on_success != null) {
                        on_success(data);
                    }
                }
            } else {
                if (on_fail != null) {
                    on_fail();
                }
            }
        }
    }
    xhr.send(post_data);
}

export function set_button_for_posting_short(button_id, url, on_check, on_success, on_fail) {

    set_button_for_posting(button_id, "등록하시겠습니까?", "등록중..", url, on_check, on_success, on_fail);
}

export function set_button_for_posting(button_id, message, alt_text, url, on_check, on_success, on_fail) {

    if (button_id == null || url == null || on_check == null) {
        return;
    }

    let button = document.getElementById(button_id);

    if (button == null) {
        return;
    }

    let origin_text = button.innerText;
    let clickEventListner = function (event) {

        let post_data = on_check();

        if (post_data == null) {
            return;
        }

        let wanna_posting = confirm("등록하시겠습니까?");

        if (!wanna_posting) {
            return;
        }

        button.innerText = alt_text;
        button.removeEventListener("click", clickEventListner);

        let on_success_new = function (data) {

            button.innerText = origin_text;
            button.addEventListener("click", clickEventListner);

            if (on_success != null) {
                on_success(data);
            }
        }

        let on_fail_new = function () {

            button.innerText = origin_text;
            button.addEventListener("click", clickEventListner);

            if (on_fail != null) {
                on_fail();
            }
        }

        load_by_ajax_post(url, post_data, on_success_new, on_fail_new);
    }
    button.addEventListener("click", clickEventListner);
}


/* 내부에서만 사용하는 함수. */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}