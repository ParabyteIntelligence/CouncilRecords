"use strict";
(function() {
  //==========================
  // Calendar Directive
  //==========================
  angular
    .module('CouncilRecords')
    .directive('dateselector', dateselector);

  function dateselector() {
    return {
      require: 'ngModel',
      link: function(scope, el, attr, ngModel) {
        angular.element(el).datepicker({
          dateFormat: 'mm-dd-yyyy',
          onSelect: function(dateText) {
            scope.$apply(function() {
              ngModel.$setViewValue(dateText);
            });
          }
        });
      }
    };
  }

})();