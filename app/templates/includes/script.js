var app = new Vue({
  el: '#wrap',
  delimiters: ['${', '}'],
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
    },

    // ApplicantUpdate
    getSkillLinkList: function () {
      const vm = this;
      $.ajax({
        method: 'GET',
        url: "{{ url('api:members:skill-list') }}"
      }).done(function (response) {
        vm.skillList = response;
      }).fail(function (response) {
        console.log(response);
      });

      $.ajax({
        method: 'GET',
        url: "{{ url('api:members:link-list') }}"
      }).done(function (response) {
        vm.linkList = response;
      }).fail(function (response) {
        console.log(response);
      });
    },
    getApplicantProfile: function () {
      const vm = this;
      console.log('getApplicantProfile');
      $.ajax({
        method: 'GET',
        url: "{{ url('api:members:profile') }}"
      }).done(function (response) {
        vm.applicantDetail = response;
      }).fail(function (response) {
        console.log('fail');
        console.log(response);
      });
    },
    updateApplicantProfile: function () {
      const vm = this;
      var obj = $.extend({}, vm.applicantDetail);
      delete obj.img_profile;
      $.ajax({
        method: 'PATCH',
        url: "{{ url('api:members:profile') }}",
        data: JSON.stringify(obj),
        contentType: 'application/json',
        processData: false,
        dataType: 'JSON'
      }).done(function (response) {
        var formData = new FormData();
        var file = $('#id-img-profile')[0].files[0];
        if (file) {
          formData.append('img_profile', file);
          console.log(formData);
          $.ajax({
            method: 'PATCH',
            url: "{{ url('api:members:profile') }}",
            data: formData,
            processData: false,
            contentType: false,
          }).done(function (response) {
            vm.applicantDetail = response;
            $('#id-img-profile').val('');
          });
        } else {
          vm.applicantDetail = response;
        }
      }).fail(function (response) {
        console.log(response);
      });
    }
  },
  computed: {
    
  }
});
