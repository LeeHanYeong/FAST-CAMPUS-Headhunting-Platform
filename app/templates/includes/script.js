function goToSection(id, offsetTop) {
    if (typeof offsetTop === 'undefined') {
        offsetTop = 30;
    }
    $('html, body').animate({
        scrollTop: $(id).offset().top - offsetTop
    }, 10);
}

var app = new Vue({
    el: '#wrap',
    delimiters: ['${', '}'],
    mixins: [
        mixin
    ],
    data: {
        showNavMenu1: false,
        failCount: 0,
        modalSpinner: undefined
    },
    mounted: function () {
        this.modalSpinner = $('#id-spinner-modal');
    },
    methods: {
        // Common
        modal: function (options) {
            var elModal = $('#id-modal');
            var btnFirst = elModal.find('.btn-first');
            if (typeof options.title !== 'undefined') {
                elModal.find('.modal-title').text(options.title);
            }
            if (typeof options.content !== 'undefined') {
                elModal.find('.modal-body').text(options.content);
            }
            if (typeof options.firstFunction !== 'undefined') {
                btnFirst.show();
                btnFirst.click(function () {
                    options.firstFunction();
                    elModal.hide();
                });
            } else {
                btnFirst.hide();
            }
            if (typeof options.secondFunction !== 'undefined') {
                elModal.find('.btn-second').click(function () {
                    options.secondFunction();
                    elModal.hide();
                });
            }
            elModal.modal();
        },
        modalInfo: function (options) {
            var elModal = $('#id-modal-info');
            if (typeof options.title !== 'undefined') {
                elModal.find('.modal-title').text(options.title);
            }
            elModal.modal();
        },
        showModalSpinner: function (title) {
            this.modalSpinner.find('#id-spinner-modal-title').text(title);
            this.modalSpinner.modal('show');
        },
        changeModalSpinnerTitle: function (title) {
            this.modalSpinner.find('#id-spinner-modal-title').text(title);
        },
        hideModalSpinner: function (time) {
            const vm = this;
            function hideProcess() {
                vm.modalSpinner.modal('hide');
            }
            if (time !== undefined) {
                setTimeout(function () {
                    hideProcess();
                }, time);
            } else {
                setTimeout(function () {
                    hideProcess();
                }, 500);
            }
        },
        // Header


        // ApplicantList
        bookmarkImageSrc: function (applicantPk) {
            var isLike = $('#img-applicant-' + applicantPk).attr('data-is-like');
            return isLike === 'True' ? "{{ static('images/bookmark_active.svg') }}" : "{{ static('images/bookmark_normal.svg') }}";
        },
        toggleUserLike: function (event) {
            const vm = this;
            var el = $(event.target);
            var method = 'POST';
            var applicantPk = el.attr('data-user-pk');
            var isLike = el.attr('data-is-like');
            if (isLike === 'True') {
                method = 'DELETE';
            }
            $.ajax({
                method: method,
                url: "{{ url('api:members:userlike') }}",
                data: {
                    to_user: el.attr('data-user-pk')
                }
            }).done(function (response) {
                if (isLike === 'True') {
                    el.attr('data-is-like', 'False');
                    el.attr('src', "{{ static('images/bookmark_normal.svg') }}");
                } else {
                    el.attr('data-is-like', 'True');
                    el.attr('src', "{{ static('images/bookmark_active.svg') }}");
                }
            }).fail(function (response) {
                console.log(response);
                vm.failCount += 1;
                if (vm.failCount > 2) {
                    location.reload();
                }
            });
        }
    },
    computed: {},
    directives: {
        focus: {
            inserted: function (el) {
                // Vue.nextTick(function () {
                //   el.focus();
                // });
            }
        }
    }
});
