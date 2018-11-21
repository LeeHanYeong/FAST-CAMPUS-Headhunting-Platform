function goToSection (id, offsetTop) {
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
    failCount: 0
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
    // ApplicantList
    toggleUserLike: function (event) {
      const vm = this;
      function addLikeClass(el) {
        el.addClass('btn-primary');
        el.removeClass('btn-outline-primary');
      }
      function removeLikeClass(el) {
        el.addClass('btn-outline-primary');
        el.removeClass('btn-primary');
      }
      var el = $(event.target);
      var method = 'POST';
      var likeClass = 'btn-primary';
      var unlikeClass = 'btn-outline-primary';
      var isLiked = el.hasClass(likeClass);
      if (isLiked) {
        method = 'DELETE';
        removeLikeClass(el);
      } else {
        addLikeClass(el);
      }
      $.ajax({
        method: method,
        url: "{{ url('api:members:userlike') }}",
        data: {
          to_user: el.attr('data-user-pk')
        }
      }).done(function (response) {

      }).fail(function (response) {
        console.log(response);
        vm.failCount += 1;
        if (isLiked) {
          addLikeClass(el);
        } else {
          removeLikeClass(el);
        }
        if (vm.failCount > 2) {
          location.reload();
        }
      });
    }
  },
  computed: {
    
  },
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
