
var sqltable =document.getElementById("sqltable"),rIndex




function editTable(){
    document.getElementById("edit-table").style.display = 'block' ;

}

for(var i = 1; i < sqltable.rows.length; i++){
    sqltable.rows[i].onclick = function(){
        rIndex =this.rowIndex;
        console.log(rIndex);

        document.getElementById("item_number").value = this.cells[0].innerHTML;
        document.getElementById("item_description").value = this.cells[1].innerHTML;
        document.getElementById("item_commonname").value = this.cells[2].innerHTML;
        document.getElementById("item_type").value = this.cells[4].innerHTML;
        document.getElementById("item_vendor").value = this.cells[5].innerHTML;
        document.getElementById("item_productnumber").value = this.cells[6].innerHTML;
        document.getElementById("item_boxnumber").value = this.cells[7].innerHTML;
        document.getElementById("item_stock").value = this.cells[8].innerHTML;
        document.getElementById("item_restock").value = this.cells[9].innerHTML;

    }
}





