(function() {
  'use strict';

  angular
    .module('CouncilRecords')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {

    $log.debug('runBlock end');
  }

})();
