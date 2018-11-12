var app = new Vue({
  el: '#wrap',
  delimiters: ['${', '}'],
  data: {
    applicantDetail: {},
    skillList: [],
    linkList: []
  },
  methods: {
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
        url: '/members/applicant/2/'
      }).done(function (response) {
        vm.applicantDetail = response;
      }).fail(function (response) {
        console.log('fail');
        console.log(response);
      });
    }
  }
});
