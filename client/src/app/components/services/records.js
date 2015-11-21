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

      var params = {};
      if (query.start_date && query.start_date !== 'Invalid date') {
        params.start_date = query.start_date;
      }
      if (query.end_date && query.end_date !== 'Invalid date') {
        params.end_date = query.end_date;
      }
      params.search_query = query.search_query;
      if (params.min_amount) {
        params.min_amount = query.min_amount;
      }
      if (params.max_amount) {
        params.max_amount = query.max_amount;
      }
      params.num_hits = 50;

      return $http.get('http://' + $location.host() + ':8080/search', {
        params: params
      }).then(function(res) {
        return res.data;
      });

    }
  }

})();