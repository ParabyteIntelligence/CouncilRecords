/* global _:false, moment:false */

import {
  config
}
from './index.config';
import {
  routerConfig
}
from './index.route';
import {
  runBlock
}
from './index.run';
import {
  Search
}
from './main/search.service.js'
import {
  MainController
}
from './main/main.controller';
angular.module('CouncilRecords', ['ngAnimate', 'ngSanitize', 'ngMessages', 'ngAria', 'ui.router', 'md.data.table', 'ngMaterial', 'toastr'])
  .constant('moment', moment)
  .config(config)
  .config(routerConfig)
  .run(runBlock)
  .controller('MainController', MainController)
  .constant('lodash', _)
  .constant('moment', moment)
  .service('Search', Search);
