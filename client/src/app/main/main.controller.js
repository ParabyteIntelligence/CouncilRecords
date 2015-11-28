export class MainController {
  constructor($document, $log, $state, $timeout, $mdDialog, $mdMedia, lodash, moment, Search) {
    'ngInject';

    var vm = this;

    this.results = [];
    this.delay = 1000;
    this.minAmt = parseFloat($state.params.minAmt);
    this.maxAmt = parseFloat($state.params.maxAmt);
    this.startDate = lodash.isUndefined($state.params.startDate) ? '' : moment($state.params.startDate, "YYYYMMDD").toDate();
    this.endDate = lodash.isUndefined($state.params.endDate) ? '' : moment($state.params.endDate, "YYYYMMDD").toDate();
    this.search = $state.params.search;
    this.page = 1;
    this.limit = 5;

    this.showInfo = showInfo;
    this.findResults = findResults;
    this.doSearch = doSearch;

    function findResults() {
      var query = {
        num_hits: 1000,
        search_query: vm.search
      };
      if (lodash.isNumber(vm.minAmt) && vm.minAmt >= 0) {
        query.min_amount = vm.minAmt;
      }
      if (lodash.isNumber(vm.maxAmt) && vm.maxAmt >= 0) {
        query.max_amount = vm.maxAmt;
      }
      if (lodash.isDate(vm.startDate)) {
        query.start_date = vm.startDate;
      }
      if (lodash.isDate(vm.endDate)) {
        query.end_date = vm.endDate;
      }
      return Search.search(query).then(function (data) {
        vm.results = data.hits;
        return data.autocomplete;
      })
    }

    function doSearch() {
      var goParams = {
        search: vm.search,
        minAmt: vm.minAmt,
        maxAmt: vm.maxAmt
      }
      if (lodash.isDate(vm.startDate)) {
        goParams['startDate'] = moment(vm.startDate).format('YYYYMMDD');
      }
      if (lodash.isDate(vm.endDate)) {
        goParams['endDate'] = moment(vm.endDate).format('YYYYMMDD');
      }
      $state.go('.', goParams);
    }



    function showInfo(ev) {
      $mdDialog.show({
        controller: DialogController,
        templateUrl: 'app/main/dialog.tmpl.html',
        parent: angular.element($document.body),
        targetEvent: ev,
        clickOutsideToClose: true,
        fullscreen: $mdMedia('sm')
      })
    }
  }
}

function DialogController($scope, $mdDialog) {
  $scope.hide = function () {
    $mdDialog.hide();
  };
  $scope.cancel = function () {
    $mdDialog.cancel();
  };
  $scope.answer = function (answer) {
    $mdDialog.hide(answer);
  };
}
