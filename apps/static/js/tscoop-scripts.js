$(document).ready(function () {
    const keywords = [];

    $('#keyword-input').on('keypress', function (e) {
        if (e.which === 13) {
            e.preventDefault();
            const keywordInput = $(this);
            const keywordValue = keywordInput.val().trim();
            if (keywordValue) {
                const keywordArray = keywordValue.split(','); // Split the keywords by comma
                keywordArray.forEach(function (keyword) {
                    keyword = keyword.trim();
                    if (keyword && !keywords.includes(keyword)) {
                        keywords.push(keyword);
                        $('#keywords-wrapper').append(`<span class="keyword-bubble">${keyword}<span class="remove">x</span></span>`);
                    }
                });
                keywordInput.val('');
                updateHiddenKeywords();
            }
        }
    });

    $(document).on('click', '.keyword-bubble .remove', function () {
        const keyword = $(this).parent().text().slice(0, -1);
        const index = keywords.indexOf(keyword);
        if (index > -1) {
            keywords.splice(index, 1);
        }
        $(this).parent().remove();
        updateHiddenKeywords();
    });

    function updateHiddenKeywords() {
        $('input[name="keywords"]').val(keywords.join(','));
    }
});