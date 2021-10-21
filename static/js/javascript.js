var table =document.getElementById("table"),rIndex;



for(var i = 1; i < table.rows.length; i++){
    table.rows[i].onclick = function(){
        rIndex =this.rowIndex;
        console.log(rIndex);

        document.getElementById("itemNumber1").value = this.cells[0].innerHTML;
        document.getElementById("itemDescription").value = this.cells[1].innerHTML;
        document.getElementById("itemBoxNumber").value = this.cells[2].innerHTML;
        document.getElementById("itemStock").value = this.cells[3].innerHTML;


    }
}



