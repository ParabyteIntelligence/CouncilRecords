(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .service('Records', Records);

  /** @ngInject */
  function Records($http) {
    var service = {
      search: search
    };

    return service;

    function search(query) {

      return $http.get('http://localhost:9099/search', {
        params: query
      });

    }
  }

})();