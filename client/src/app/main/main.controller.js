(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($log, $state) {
    var vm = this;

    vm.query = {
      'search_query': '',
      'start_date': '',
      'end_date': '',
      'min_amount': '',
      'max_amount': ''
    }

    vm.search = search;

    function search() {
      var t = _.clone(vm.query);
      t.start_date = moment(vm.query.start_date).format();;
      t.end_date = moment(vm.query.end_date).format();
      $state.go('search.result', t);
    }
  }
})();