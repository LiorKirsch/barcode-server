
function fillDataTable(data)
{
	var r = new Array(), j = -1;
	 for (var key=0, size=data.length; key<size; key++){
	     r[++j] ='<tr><td>';
	     r[++j] = data[key].fields.addingDate;
	     r[++j] = '</td><td class="whatever1">';
	     r[++j] = data[key].fields.product.description;
	     r[++j] = '</td><td class="whatever2">';
	     r[++j] = '<a href=http://www.upcdatabase.com/item/' + data[key].fields.product.barcode + '  target="_new">' + data[key].fields.product.barcode + '</a>';
	     r[++j] = '</td><td class="whatever3"><div class="progress"> <div class="bar bar-danger" style="width: 35%;"></div>';
	     r[++j] = '</td></tr>';
	 }
	 $('#dataTableBody').html(r.join(''));
} 
