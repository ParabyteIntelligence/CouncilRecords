export function Search($http, $location) {
  'ngInject';
  var service = {
    search: search
  };

  return service;

  function search(query) {
    // var deferred = $q.defer();
    // var hits = []
    // for (var i = 0; i < 20; i++) {
    //   hits[i] = {
    //     date: new Date(),
    //     link: 'http://testing.com/',
    //     title: '10095-1 Purchase of Communication Tower Installation Construction Services -MOTION',
    //     amount: 500230.23,
    //     summary: "Summary: 2015-0122 - JOHNSTON TECHNICAL SERVICES, INC d/b/a JTS for Communication Tower Installation Construction Services through the Texas Department of Information Resources for the Department of Public Works & Engineering - $227,579.28 - Enterprise Fund This item should only be considered after passage of Item 14 above"
    //   }
    // }
    // deferred.resolve({
    //   hits: hits,
    //   autocomplete: ['testing', 'this']
    // });
    // return deferred.promise;
    return $http.get('http://' + $location.host() + ':8080/search', {
      params: query
    }).then(function (res) {
      return res.data;
    });

  }
}
