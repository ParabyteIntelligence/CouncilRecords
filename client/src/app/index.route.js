(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('search', {
        url: '/',
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'vm'
      })
      .state('search.result', {
        url: '/query?search_query&start_date&end_date&min_amount&max_amount',
        templateUrl: 'app/main/result.html',
        controller: 'ResultController',
        controllerAs: 'vm'
      });

    $urlRouterProvider.otherwise('/');
  }

})();