(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($log, Records) {
    var vm = this;

    vm.query = {
      'search_query': '',
      'start_date': '',
      'end_date': '',
      'min_amount': '',
      'max_amount': ''
    }
    vm.search_results = [];

    vm.search = search;

    function search() {
      $log.log('test');
      Records.search(vm.query).then(function(data) {
        $log.log(data);
        vm.search_results = data.data;
      })
    }
  }
})();