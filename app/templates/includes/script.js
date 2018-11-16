var app = new Vue({
  el: '#wrap',
  delimiters: ['${', '}'],
  data: {
    applicantDetail: {},
    skillList: [],
    linkList: []
  },
  methods: {
    // ApplicantList

    // ApplicantUpdate
    getSkillLinkList: function () {
      const vm = this;
      $.ajax({
        method: 'GET',
        url: '/members/skill/'
      }).done(function (response) {
        vm.skillList = response;
      }).fail(function (response) {
        console.log(response);
      });

      $.ajax({
        method: 'GET',
        url: '/members/link/'
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
        url: '/members/applicant/profile/'
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
        url: '/members/applicant/profile/',
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
            url: '/members/applicant/profile/',
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
  }
});
