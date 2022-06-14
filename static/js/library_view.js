

export function set_display_by_click(view_id, target_id) {

    let view = document.getElementById(view_id);
    let target = document.getElementById(target_id);

    if (view == null || target == null) {
        return;
    }

    view.addEventListener("click", function () {

        if (target.style.display == 'none') {
            target.style.display = 'block';
        } else {
            target.style.display = 'none';
        }
    });
}