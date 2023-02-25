document.addEventListener('DOMContentLoaded', function() {

    console.log("JS RUnning")
    




});


function add_metric(el){

    console.log("clicked");

    console.log(el);

    el.style.display="none";

    add_row=document.querySelector("#add-row")
    add_row.style.display= "table-row";

   


}


function edit(el){
    
    element=(el.parentNode);

    rowid= (el.getAttribute("data-id"));
    element.style.display="none";
 
  
    editrow=document.getElementById(rowid);
    editrow.style.display="table-row";
   

}

function del(el){



    console.log(el.getAttribute("data-id"));
    rowid=el.getAttribute("data-id");
    document.querySelector("#metric_add").value="del-metric"+rowid


}

function save_row(el){
    console.log(el.getAttribute("data-id"));
    rowid=(el.getAttribute("data-id"));
    s_measure=document.getElementById("measure-"+rowid).value;
    s_category=document.getElementById("category-"+rowid).value;
    s_metrics=document.getElementById("metric-"+rowid).value;
    s_code=document.getElementById("code-"+rowid).value;
    s_numerator=document.getElementById("numerator-"+rowid).value;
    s_denominator=document.getElementById("denominator-"+rowid).value;

    document.querySelector("#metric_add").value="add-new-metric"

    document.querySelector("#edit-metrics-txt").value=rowid+"|"+s_measure+"|"+s_category+"|"+s_metrics+"|"+s_code+"|"+s_numerator+"|"+s_denominator





}