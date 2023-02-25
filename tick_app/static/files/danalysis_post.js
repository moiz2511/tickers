document.addEventListener('DOMContentLoaded', function() {

    console.log("JS RUnning after post");



document.querySelector(".circle").addEventListener('click', function(){


console.log("clicked")

console.log(document.querySelectorAll(".percent"));

array_list=document.querySelectorAll(".percent")

rows=document.querySelectorAll(".metric_row").length;
var arrayLength = array_list.length;
for (var i = 0; i < arrayLength; i++) {
    console.log(array_list[i]);
   

  
   
            if (array_list[i].innerHTML.indexOf("M") == -1) {
            
                if (array_list[i].innerHTML.indexOf("%") == -1){
                    
                    number= parseFloat(array_list[i].innerHTML)
                    number= (number * 100).toFixed(2)
                    array_list[i].innerHTML= number + '%'

                }
                else{
                    number= parseFloat(array_list[i].innerHTML)
                    number= (number / 100).toFixed(2)
                    array_list[i].innerHTML= number 

                }
            }
        
    

   

  
}






})


document.querySelector('#bar').style.display='None'

document.querySelector('#c-text').innerHTML=' <span class="companies">'+ document.querySelector("#h-company").innerHTML +'</span>';

document.querySelector('#type-text').innerHTML=' <span class="companies">'+ document.querySelector("#h-type").innerHTML +'</span>';

document.querySelector('#sc-text').innerHTML=' <span class="companies">'+ document.querySelector("#h-sc").innerHTML +'</span>';

document.querySelector('#cat-text').innerHTML=' <span class="companies">'+ document.querySelector("#h-cat").innerHTML +'</span>';



document.querySelector('#m-text').innerHTML=' <span class="companies">'+ document.querySelector("#h-metrics").innerHTML +'</span>';

document.querySelector('#from-text').innerHTML=' <span class="companies">'+ document.querySelector("#h-from").innerHTML +'</span>';

document.querySelector('#to-text').innerHTML=' <span class="companies">'+ document.querySelector("#h-to").innerHTML +'</span>';

document.querySelector('#m-ranges').innerHTML=' <span class="companies">'+ document.querySelector("#h-ranges").innerHTML +'</span>';


document.querySelector('#slider').addEventListener('click', function(){
  
    console.log(document.querySelector('#checkbox').value);

    var isChecked=document.getElementById("checkbox").checked;
    console.log(isChecked);
    if (isChecked == true)
    {
        document.getElementById("bar").style.display = 'none';
        document.getElementById("line").style.display = 'block';
        console.log('yo')
    }
    else
    {
        document.getElementById("bar").style.display = 'block';
        document.getElementById("line").style.display = 'none';
        console.log("tyo")
    }
});


    
});