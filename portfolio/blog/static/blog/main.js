var headings_exist = false;
setup_heading_links();

$(document).ready(() => {
    update_hash_on_click('#post-content :header a');
    update_hash_on_click('#toc a');
});

/* Adjust the URL fragment on click on heading. */
function update_hash_on_click(selector) {
    $(selector).on('click', function(event) {
        event.preventDefault();
        window.location.hash = $(this).attr("href");
    });
}

/* Turn headings into links. */
function setup_heading_links() {
    $("h1, h2, h3, h4, h5, h6").each((idx, heading) => {
        if (idx === 0) return;  // post title
        $(heading).wrapInner("<a href='#" + $(heading).attr("id") + "'></a>");
        headings_exist = true;
    });
}

