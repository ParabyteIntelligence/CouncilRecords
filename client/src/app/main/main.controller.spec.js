(function() {
  'use strict';

  describe('MainController', function() {
    var vm;
    var $scope, $log, $state;

    beforeEach(module('CouncilRecords'));
    beforeEach(inject(function(_$controller_, $rootScope, _$log_, _$state_) {
      $scope = $rootScope.$new();
      $log = _$log_;
      $state = _$state_;

      vm = _$controller_('MainController', {
        $scope: $scope,
        $log: $log,
        $state: $state
      });
    }));

    it('should initialize all the query fields', function() {
      expect(vm.query.search_query).toEqual(jasmine.any(String));
      expect(vm.query.start_date).toEqual(jasmine.any(String));
      expect(vm.query.end_date).toEqual(jasmine.any(String));
      expect(vm.query.min_amount).toEqual(jasmine.any(String));
      expect(vm.query.max_amount).toEqual(jasmine.any(String));
    })

    it('should have a function called Search', function() {
      expect(vm.search).toEqual(jasmine.any(Function));
    })

    it('should convert dates to ISO before passing it to $state.go', function() {
      spyOn($state, 'go').and.callThrough();

      vm.query.start_date = '05/15/2015';
      vm.query.end_date = '02/20/2020';
      vm.search();

      var t = {
        search_query: '',
        start_date: '2015-05-15T00:00:00-05:00',
        end_date: '2020-02-20T00:00:00-06:00',
        min_amount: '',
        max_amount: ''
      }

      expect($state.go).toHaveBeenCalledWith('search.result', t);
    })
  });
})();