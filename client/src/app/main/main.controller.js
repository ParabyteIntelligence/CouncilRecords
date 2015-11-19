(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($log, $state, _, moment) {
    var vm = this;

    vm.query = $state.params || {
      search_query: '',
      start_date: '',
      end_date: '',
      min_amount: '',
      max_amount: ''
    }

    if (vm.query.start_date != '') {
      vm.query.start_date = moment(vm.query.start_date).format('L');
    }

    if (vm.query.end_date != '') {
      vm.query.end_date = moment(vm.query.end_date).format('L');
    }

    vm.search = search;

    function search() {
      var t = _.clone(vm.query);
      t.start_date = moment(vm.query.start_date, 'MM-DD-YYYY').format();
      t.end_date = moment(vm.query.end_date, 'MM-DD-YYYY').format();
      $state.go('search.result', t);
    }
  }
})();