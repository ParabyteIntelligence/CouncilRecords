(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .service('Records', Records);

  /** @ngInject */
  function Records($http, $location) {
    var service = {
      search: search
    };

    return service;

    function search(query) {

      return $http.get('http://' + $location.host() + ':9099/search', {
        params: query
      }).then(function(res) {
        return res.data;
      });

    }
  }

})();