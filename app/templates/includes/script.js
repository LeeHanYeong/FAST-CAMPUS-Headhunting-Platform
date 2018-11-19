var app = new Vue({
  el: '#wrap',
  delimiters: ['${', '}'],
  mixins: [
    mixin
  ],
  data: {
    applicantDetail: {},
    skillList: [],
    linkList: [],

    failCount: 0
  },
  methods: {
    // ApplicantList
    toggleUserLike: function (event) {
      const vm = this;
      function addLikeClass(el) {
        console.log('addLikeClass');
        el.addClass('btn-primary');
        el.removeClass('btn-outline-primary');
      }
      function removeLikeClass(el) {
        console.log('removeLikeClass');
        el.addClass('btn-outline-primary');
        el.removeClass('btn-primary');
      }
      var el = $(event.target);
      var method = 'POST';
      var likeClass = 'btn-primary';
      var unlikeClass = 'btn-outline-primary';
      var isLiked = el.hasClass(likeClass);
      console.log(isLiked);
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
        Vue.nextTick(function () {
          el.focus();
        });
      }
    }
  }
});
