var
  page = require('webpage').create(),
  fs = require('fs'),
  output_file = 'doc-list.json',
  page_address = 'http://houston.novusagenda.com/agendapublic',
  listOfDocuments = [],
  numOfPages = 0;

// page.onConsoleMessage = function(msg, lineNum, sourceId) {
//   console.log('CONSOLE: ' + JSON.stringify(msg) + ' (from line #' + lineNum + ' in "' + sourceId + '")');
// };

// Inject Selectors using external JS
page.injectJs('lodash.js');

page.open(page_address, function(status) {
  if (status !== 'success') {
    console.log('ERROR: Failed to load the page: ', page_address);
    console.log('INFO: Exiting Crawler')
    phantom.exit();
  } else {
    getDocuments();
  }
});


function waitForBrowser() {
  do {
    phantom.page.sendEvent('mousemove');
  } while (page.loading);
}

function getDocuments() {
  page.evaluate(function() {
    window.DATE_RANGE = "#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_ddlDateRange";
    window.DATE_RANGE_TYPE = "lyr";
    window.MEETING = "#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_ctl00";
    window.MEETING_TYPE = "1";
    window.DOCUMENT_CATEGORY = "#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_ctl01";
    window.DOCUMENT_CATEGORY_TYPE = "14";
    window.SEARCH_BUTTON = "#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_imageButtonSearch";
    window.NUM_OF_PAGES = "#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_radGridItems_ctl00_ctl03_ctl01_PageSizeComboBox_Input";
    window.NEXT_PAGE = "a[title='Next Page']";
    window.ITEM_TABLE = "#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_radGridItems_ctl00";
    window.ITEM_TABLE_WRAP = "#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_ItemsPageView";
  });

  queryFormSetup1();

  setTimeout(function() {

    queryFormSetup2();

    setTimeout(function() {

      queryFormSetup3();

      setTimeout(function() {
        showItemTable();
        getAllItems();
      }, 1000);

    }, 1000);


  }, 1000);

}

function showItemTable() {
  page.evaluate(function() {
    $(window.ITEM_TABLE_WRAP).show();
  });
}

function getAllItems() {
  setTimeout(function() {
    var newItems = getItemsOnCurrentPage();
    if (((listOfDocuments.length === 0) || (listOfDocuments[listOfDocuments.length - 1].item_id !== newItems[newItems.length - 1].item_id)) && getNextPage()) {
      numOfPages = numOfPages + 1;
      listOfDocuments.push.apply(listOfDocuments, newItems);
      getAllItems();
    } else {
      listOfDocuments.push.apply(listOfDocuments, newItems);
      fs.write(output_file, JSON.stringify(listOfDocuments), 'w');
      phantom.exit();
    }
  }, 5000);
}

function getItemsOnCurrentPage() {
  return page.evaluate(
    function() {
      var itemTable = $(window.ITEM_TABLE);

      var items = itemTable.find('tr.rgRow');
      var itemsLength = items.length;
      var docList = [];
      for (var i = 0; i < itemsLength; i++) {
        var item = items[i];
        var fields = $(item).find('td');
        var date = fields[0].innerText;
        var title = fields[1].innerText;
        var link_attributes = $(item).find('a').attr('onclick').split('?')[1].split('&');
        var item_id = link_attributes[0].split('=')[1];
        var meeting_id = link_attributes[1].split('\'')[0].split('=')[1];
        docList.push({
          'date': date,
          'title': title,
          'item_id': item_id,
          'meeting_id': meeting_id
        });
      }
      return docList;
    }
  );
}

function queryFormSetup1() {
  return page.evaluate(
    function() {
      // Set Date Range
      $(window.DATE_RANGE).val(window.DATE_RANGE_TYPE).change();

      return true;
    }
  );
}

function queryFormSetup2() {
  return page.evaluate(function() {
    // Set Meeting Type
    $(window.MEETING).val(window.MEETING_TYPE).change();

    return true;
  })
}

function queryFormSetup3() {
  return page.evaluate(
    function() {
      // Set Document Category
      $(window.DOCUMENT_CATEGORY).val(window.DOCUMENT_CATEGORY_TYPE).change();

      // Click the Search Button
      $(window.SEARCH_BUTTON).click();

      return true;
    }
  )
}

function getNextPage() {
  return page.evaluate(
    function() {
      var codeToNextPage = $(window.ITEM_TABLE).find(window.NEXT_PAGE).prop('href');
      if (codeToNextPage) {
        eval(codeToNextPage.split(':')[1]);
        return true;
      } else {
        return false;
      }
    }
  );
}