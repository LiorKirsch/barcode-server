
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

        var barHTML = 	'<div class="progress"> <div class="bar '+ barStyle + '" style="width: ' + percentExpired + '%;"> </div> ';
	return barHTML;
}
function createProductTableRow(productDataArray,index) 
{

	var tableRowHTML = new Array(), j = -1;
	var numberOfItemsInGroup = productDataArray.length;
	barcode = productDataArray[0].fields.product.barcode;
	description = productDataArray[0].fields.product.description;


	tableRowHTML[++j] ='<tr data-toggle="collapse" data-target="#demo' + index + '" id="accordian2" class="accordion-toggle"><td class="itemNumberTD">' + numberOfItemsInGroup + '</td><td class="whatever1">';
	tableRowHTML[++j] = '<a href="#" id="barcode-' + barcode +'" class="btn">Update</a> ' + description ;
	tableRowHTML[++j] = '</td><td></td></tr>';
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
