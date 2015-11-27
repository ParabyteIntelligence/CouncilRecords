export function routerConfig($stateProvider, $urlRouterProvider) {
  'ngInject';
  $stateProvider
    .state('home', {
      url: '/?search=&startDate=&endDate=&minAmt=&maxAmt=',
      templateUrl: 'app/main/main.html',
      controller: 'MainController',
      controllerAs: 'vm'
    });

  $urlRouterProvider.otherwise('/');
}
