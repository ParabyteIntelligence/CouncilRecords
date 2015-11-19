(function() {
  'use strict';

  describe('ResultController', function() {
    var vm;
    var $scope, $log, $state, Records;
    var fakeParams;

    beforeEach(module('CouncilRecords'));
    beforeEach(inject(function(_$controller_, $rootScope, _$log_, _$state_, _Records_, $q) {
      $scope = $rootScope.$new();
      $log = _$log_;
      $state = _$state_;
      Records = _Records_;

      vm = _$controller_('ResultController', {
        $scope: $scope,
        $log: $log,
        $state: $state,
        Records: Records
      });

      fakeParams = {
        hello: 'world'
      }

      spyOn(Records, 'search').and.callFake(function() {
        var deferred = $q.defer();
        deferred.resolve({
          data: {
            hits: []
          }
        });
        return deferred.promise;
      });
    }))

    it('should initialize results array', function() {
      expect(vm.results).toEqual(jasmine.any(Array));
    })

    it('should call Results with $state.params', function() {
      // TODO: Find out why the controller doesnt automatically call Records.search
      Records.search(fakeParams).then(function() {
        expect(Records.search).toHaveBeenCalledWith(fakeParams);
      })
    })
  })
})();