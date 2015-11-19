(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .controller('ResultController', ResultController);

  /** @ngInject */
  function ResultController($log, $state, Records) {
    var vm = this;

    vm.results = [];

    Records.search($state.params).then(function(data) {
      vm.results = data.hits;
    }, function(error) {
      $log.error(error);
    })
  }
})();