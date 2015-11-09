var page = new WebPage(),
  addr = 'http://houston.novusagenda.com/agendapublic',
  listOfDocuments = [];

page.onConsoleMessage = function(msg, lineNum, sourceId) {
  console.log('CONSOLE: ' + msg + ' (from line #' + lineNum + ' in "' + sourceId + '")');
};

function setInitialFields() {
  page.evaluate(function() {
    // SET FORM VALUES
    $("#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_ddlDateRange").val("lyr").change();
    $("#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_ctl00").val("1").change();
  })
}


function completeFormInput() {
  setTimeout(function() {
    listOfDocuments = page.evaluate(function() {
      $("#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_ctl01").val("14").change();
      // HIT THE SEARCH BUTTON
      $("#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_imageButtonSearch").click()

      var num_of_pages = parseInt($("#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_radGridItems_ctl00_ctl03_ctl01_PageSizeComboBox_Input").val());
      var docList = [];
      for (var i = 0; i < num_of_pages; i++) {
        console.log("Parsing Page: ", i);
        var item_grid = $("#ctl00_ContentPlaceHolder1_SearchAgendasMeetings_radGridItems_ctl00");
        var items = item_grid.find('tr.rgRow');
        console.log("Found ", items.length, " Items");
        for (var i = 0; i < items.length; i++) {
          var d = items[i];
          var fields = $(d).find('td');
          var date = fields[0].innerText;
          var title = fields[1].innerText;
          var link_attributes = $(d).find('a').attr('onclick').split('?')[1].split('&');
          var item_id = link_attributes[0].split('=')[1];
          var meeting_id = link_attributes[1].split("'")[0].split('=')[1];
          docList.push({
            'date': date,
            'title': title,
            'item_id': item_id,
            'meeting_id': meeting_id
          });
        }
        var next_page = item_grid.find('a[title="Next Page"]');
        if(next_page.length===0) {
          return docList;
        }
        next_page.click();
      }
      return docList;
    });
    var fs = require('fs');

    var path = 'output.json';
    fs.write(path, JSON.stringify(listOfDocuments), 'w');
    phantom.exit();
  }, 1000);
}

page.open(addr, function(status) {
  if (status === 'success') {
    console.log("Success!");

    setInitialFields();
    completeFormInput();

  } else {
    console.log("Fail!");
    phantom.exit();
  }
})
