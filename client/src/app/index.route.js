(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider) {
    // Define Routes
    $stateProvider
      .state('search', {
        url: '/',
        templateUrl: '/app/main/main.html',
        controller: 'MainController',
        controllerAs: 'vm',
        abstract: true
      })
      .state('search.result', {
        url: 'query?search_query&start_date&end_date&min_amount&max_amount',
        views: {
          'results': {
            templateUrl: '/app/result/result.html',
            controller: 'ResultController',
            controllerAs: 'vm'
          }
        }
      });

    $urlRouterProvider.otherwise('/');
  }

})();