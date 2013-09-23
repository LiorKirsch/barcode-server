
function fillDataTable(data)
{
	var r = new Array(), j = -1;
	var itemsIds = new Array();
	var addingDate,barcode,description,expiresInDays, percentExpired;
	var lastProdcutBarCode = null;
	var sameProductGrouped = new Array();
	var currentBarCode;
        var numberOfGroup = 1;
	 for (var key=0, size=data.length; key<size; key++){

	    currentBarCode = data[key].fields.product.barcode;
	    if (!lastProdcutBarCode  | ( lastProdcutBarCode == currentBarCode & key < (data.length -1) ) ) {
		sameProductGrouped.push( data[key]);
		}
	    else {
	        r.push ( createProductTableRow(sameProductGrouped ,numberOfGroup)  );
		itemsIds.push ( currentBarCode );

		numberOfGroup ++;
		sameProductGrouped = new Array();
		}
	    lastProdcutBarCode = currentBarCode;

	 }

	 $('#dataTableBody').html(r.join(''));

	 var barcodeId;
	 var title;
	 for (var key=0, size=itemsIds.length; key<size; key++){
		barcodeId = "#barcode-" + itemsIds[key];
	        title = 'update item ' + barcode;
	 	$( barcodeId ).popover({ title: title, content: createProductUpdateForm(barcode) ,html:true, placement:'right'});
	}

	$('.progress .bar').progressbar();           // bootstrap 2
	$('.progress .progress-bar').progressbar();  // bootstrap 3
} 

function createFreshnessBar(percentExpired)
{
	if (percentExpired < 33) {
		barStyle = "bar-info";
	}
	else if (percentExpired < 66) {
		barStyle = "bar-warning";
	}
	else{
		barStyle = "bar-danger";
	}

        var barHTML = 	'<div class="progress "> <div class="bar '+ barStyle + '" style="width: ' + percentExpired + '%;"> </div> ';
	return barHTML;
}

function createHistogram(histogramCounts) {

	var barHTML = new Array(), j = -1;
	barHTML[++j] = 	'<div class="histogram">';
	barHTML[++j] = 	'<div class="progress vertical bottom"> <div class="bar bar-info" aria-valuetransitiongoal="' + histogramCounts[0] +'"> </div>  </div>';
	barHTML[++j] = 	'<div class="progress vertical bottom"> <div class="bar bar-warning" aria-valuetransitiongoal="' + histogramCounts[1] +'"> </div>  </div>';
	barHTML[++j] = 	'<div class="progress vertical bottom"> <div class="bar bar-danger" aria-valuetransitiongoal="' + histogramCounts[2] +'"> </div> </div> ';
	barHTML[++j] = 	'</div>';
	return barHTML.join('');;
}

function countFreshnessHistogram(productDataArray)
{
	var infoCount=0;
	var warningCount=0;
	var dangerCount=0;
	var totalCount=0;

	for (var key=0, size=productDataArray.length; key<size; key++){
		productData = productDataArray[key];
		addingDate = productData.fields.addingDate;
		expiresInDays = productData.fields.product.expiresInDays;
		percentExpired = getFreshnessBar(addingDate, expiresInDays)
		
		if (percentExpired < 33) {
			infoCount ++;
		}
		else if (percentExpired < 66) {
			warningCount++;
		}
		else{
			dangerCount++;
		}
		totalCount++;
	}
	var counts = new Array(), j = -1; 
	counts[++j] = infoCount / totalCount * 100 +5;
	counts[++j] = warningCount / totalCount * 100 +5;
	counts[++j] = dangerCount / totalCount * 100 +5;
	return counts;
}

function createProductTableRow(productDataArray,index) 
{

	var tableRowHTML = new Array(), j = -1;
	var numberOfItemsInGroup = productDataArray.length;
	barcode = productDataArray[0].fields.product.barcode;
	description = productDataArray[0].fields.product.description;

	histogramCounts = countFreshnessHistogram(productDataArray);

	tableRowHTML[++j] ='<tr data-toggle="collapse" data-target="#demo' + index + '" id="accordian2" class="accordion-toggle"><td class="itemNumberTD">' + numberOfItemsInGroup + '</td><td class="whatever1">';
	tableRowHTML[++j] = '<a href="#" id="barcode-' + barcode +'" class="btn">Update</a> ' + description ;
	tableRowHTML[++j] = '</td><td class="smallTD">' + createHistogram( histogramCounts ) + '</td></tr>';
	tableRowHTML[++j] = '<tr><td></td><td><div class="accordian-body collapse" data-parent="#accordion2" id="demo' + index + '">'; 
	for (var key=0, size=productDataArray.length; key<size; key++){

		
		productData = productDataArray[key];
		addingDate = productData.fields.addingDate;
		expiresInDays = productData.fields.product.expiresInDays;
		percentExpired = getFreshnessBar(addingDate, expiresInDays)
		tableRowHTML[++j] = '<li>' + addingDate + ' ' + createFreshnessBar(percentExpired) + '</li>';
	}
	tableRowHTML[++j] = '</div></td></tr>';
	return tableRowHTML.join('');
}

function createProductUpdateForm(productBarCode)
{
	var htmlData;
	htmlData = '<div class="form-group"><form action="/barcodeServer/addProductDetails/' + productBarCode + '" method="get">'
	htmlData += '<input type="text" name="description" class="form-control" placeholder="This is a…">'
	htmlData += '<input type="text" name="expiresInDays" class="form-control" placeholder="Expires in X days…">'
	htmlData += '<button type="submit" class="btn btn-default btn-block">Update</button>'
	htmlData += '</form></div>'

	htmlData = htmlData.replace(/"/g, '\'');
	return htmlData
}

function DateDiff(date1,  date2) {

    var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds

    var firstDate = new Date(date1);
    var secondDate = new Date(date2);
    return (firstDate - secondDate) / (oneDay) ;
}

function getFreshnessBar(addingDate, expiresInDays)
{
	var today = new Date();
	dateDifferance = DateDiff(today, addingDate);
	var percentExpired = dateDifferance / expiresInDays;
	percentExpired = percentExpired + 0.01;
	percentExpired = Math.min(Math.round(percentExpired * 100), 100);
	return percentExpired
}
