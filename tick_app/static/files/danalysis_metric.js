document.addEventListener('DOMContentLoaded', function() {

    console.log("JS RUnning")

    


    //mean, SD and RSD

   
    
    
    const name_text=document.querySelector('#myInput');




    
    function deldata(){
    
      t_=document.getElementById("text").innerHTML.replace(/<[^>]*>/g, "|||");
      t_=t_.replace(/&amp;/,"&");
      console.log(t_);
      document.querySelector('#txt').value=t_;
      console.log(document.querySelector('#txt').value);
    }






   
    autocomplete(document.getElementById("myInput"));
    
    document.querySelector('#types').addEventListener("change", function() {
        const types=document.querySelector('#types').value;

        document.querySelector("#sc").innerHTML='<option> </option>';
        document.querySelector("#cat_").innerHTML='<option> </option>';
        document.querySelector(".metrics-html").innerHTML='';

        document.querySelector('#from').value='';

        document.querySelector('#to').value='';


        document.querySelector('#from-text').innerHTML='';

        document.querySelector('#to-text').innerHTML='';



        document.querySelector('#m-text-max').innerHTML='';
        document.querySelector("#m-text").innerHTML='';

        document.querySelector("#sc-text").innerHTML='';
        document.querySelector("#cat-text").innerHTML='';
      
  
        



        


        document.querySelector('#type-text').innerHTML="<span class='companies mr-2 ml-2'>"+types +"</span>";
        fetch(`/suggest_super/${types}`)
        .then(response=>response.json())
        .then(result=>{
            console.log(result);
            
            console.log('delay')
            var i;
            sc=document.querySelector('#sc');
            sc.innerHTML='<option> </option>'
            for (i = 0; i < result.length; i++) {
            sc.innerHTML += "<option>" + result[i] + "</option>";
            }

        })
    })  

        document.querySelector('#sc').addEventListener("change", function() {
         
            const types=document.querySelector('#types').value;
            const sc=document.querySelector('#sc').value;

            document.querySelector("#cat_").innerHTML='<option> </option>';
    
          

            document.querySelector("#cat-text").innerHTML='';

            document.querySelector(".metrics-html").innerHTML='';
            document.querySelector('#m-text-max').innerHTML='';
            document.querySelector("#m-text").innerHTML='';
  
     
    
            document.querySelector('#sc-text').innerHTML="<span class='companies mr-2 ml-2'>"+ sc +"</span>";

            fetch(`/suggest_category/${types}-${sc}`)
            .then(response=>response.json())
            .then(result=>{
                console.log(result);
                
                console.log('delay')
                var i;
                cat_=document.querySelector('#cat_');
                cat_.innerHTML='<option> </option>'
                for (i = 0; i < result.length; i++) {
                cat_.innerHTML += "<option>" + result[i] + "</option>";
                }
    
            })
        })


            document.querySelector('#cat_').addEventListener("change", function() {
                const types=document.querySelector('#types').value;
                const sc=document.querySelector('#sc').value;
                const cat=document.querySelector('#cat_').value;

                document.querySelector(".metrics-html").innerHTML='';
                document.querySelector('#m-text-max').innerHTML='';
                document.querySelector("#m-text").innerHTML='';

      
                


                


                console.log(document.querySelector('#cat-text').innerHTML);
                document.querySelector('#cat-text').innerHTML="<span class='companies mr-2 ml-2'>"+ cat +"</span>";
                fetch(`/suggest_metrics/${types}-${sc}-${cat}`)
                .then(response=>response.json())
                .then(result=>{
                    console.log(result);
                    
                    console.log('delay')
                    var i;
                    metrics=document.querySelector('.metrics-html');
               
                   
                    
                    window.metricoptions=result;  
                    for (i = 0; i < result.length; i++) {
                      console.log(result[i])

                    metrics.innerHTML += " <option class='.metricoptions'>" + result[i] + "</option> ";
                    }
                  
        
                       })

                       })  

                            
  
                           





                       


 
    });



  



function suggestranges(){
  console.log("ranges clicked")
  metricvalues=document.querySelectorAll(".smetrics")
  console.log(metricvalues)
  metrics=[]
  
  ranges=document.querySelector('.ranges-html');
  ranges_data=ranges.innerHTML.replace( /(<([^>]+)>)/ig, '').trim();
  console.log(ranges_data)
  ranges_data=ranges_data.replace(/\s\s+/g, ' ');
  for (let i=0; i<metricvalues.length; i++){
    console.log(metricvalues[i].innerHTML.replace( /(<([^>]+)>)/ig, '').trim())
    metrics.push(metricvalues[i].innerHTML.replace( /(<([^>]+)>)/ig, '').trim())
  }
  console.log(metrics.toString())
  metricsvalues=metrics.toString()
  fetch(`/suggest_ranges/${metricsvalues}`)
  .then(response=>response.json())
  .then(result=>{
      console.log(result);
      window.rangevalues=result;  
      
      console.log('delay')
      var i;
      result_string=result.join(" ")
      console.log(result_string)
      console.log(ranges_data)

      if (ranges_data!=result_string){
      
      ranges.innerHTML='';
  
      for (i = 0; i < result.length; i++) {
        console.log(result[i])
        console.log(ranges)
      

      ranges.innerHTML += " <option class='.rangeoption'>" + result[i] + "</option> ";
      }
    
    }
    else{
      console.log("equal")
    }
    })

};
    


function range(element){
  console.log("ranges running")


 
  m=document.querySelector("#m-ranges");



  value=element.value
  
 
  rangevalues=window.rangevalues
  console.log(rangevalues)
  for (let i = 0; i < rangevalues.length; i++) {
    console.log(i)
    console.log(rangevalues.length)
    console.log(rangevalues[i])
    console.log(value)

    if (rangevalues[i].includes(value)) 
    {
    
      console.log(rangevalues[i])
      if (m.children.length<5) {
        const sranges=document.querySelectorAll('.srange')
        const sranges_=['defaultValUe']
        
        for (let j=0; j<sranges.length; j++){
          sranges_.push(sranges[j].innerHTML.replace( /(<([^>]+)>)/ig, '').trim())
        }
        console.log(sranges_)
        console.log(value)
        if (sranges_.includes(value)){
          console.log('includes')
        }
        else{
          console.log("run else")
        

          document.querySelector('#m-ranges').innerHTML+="<span class='companies srange ml-2 mr-2'>"+value+"<i class='ml-2 fa fa-times-circle' onclick='removemet(this)'></i> </span>"

          console.log("this run")
      }  
      }
        else
        {
          document.querySelector("#m-ranges-max").innerHTML="<span class='companies mr-2'> Max nuumber of ranges reached. </span>";
        }



    }
    console.log("loop running")
  }
  element.value='';
    
}

   


function autocomplete(inp) {



       

    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {

      document.querySelector('#c-text').innerHTML='';

      document.querySelector('#type-text').innerHTML='';

document.querySelector('#sc-text').innerHTML='';

document.querySelector('#cat-text').innerHTML='';



document.querySelector('#m-text').innerHTML='';

document.querySelector('#from-text').innerHTML='';

document.querySelector('#to-text').innerHTML='';

       
 
        
    
    
    
    
    
    
       fetch(`/suggest/${inp.value}`)
       .then(response=>response.json())
       .then(result=>{
           console.log(result);
           window.arr=result
           console.log('delay')



        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            
            /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                t=document.getElementById("text")
                txt=document.getElementById("txt")
                if (t.children.length<5) {
                t.innerHTML += "<span class=' companies mr-2'>"  + this.getElementsByTagName("input")[0].value +" <i class='ml-2 fa fa-times-circle' onclick='remove(this)'></i> </span>" 
                txt.value+= this.getElementsByTagName("input")[0].value + "\n"
                console.log(txt.value);
                inp.value='';
              }
                else {
                  m=document.getElementById("max-text")
                  inp.value='';
                  m.innerHTML="<span class='companies'> Maximim number of companies reached. </span>"
                }
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}



function remove(el) {
  var element = el;
  
  text_=(element.parentNode.innerHTML.replace(/<[^>]*>/g, ""));
  text_=text_.replace(/\s+$/,"");
  text_=text_.replace(/&amp;/,"&");
  reptxt=new RegExp( text_, 'g' );
  console.log(reptxt);
  document.querySelector('#txt').value=document.querySelector('#txt').value.replace(reptxt,"");


  console.log( document.querySelector('#txt').value);
  

  element.parentNode.remove();
  m=document.getElementById("max-text")
  m.innerHTML='';
}

function removemet(el) {
  var element = el;
  
  // text_=(element.parentNode.innerHTML.replace(/<[^>]*>/g, ""));
  // text_=text_.replace(/\s+$/,"");
  // text_=text_.replace(/&amp;/,"&");
  // reptxt=new RegExp( text_, 'g' );
  // console.log(reptxt);
  // document.querySelector('#txt').value=document.querySelector('#txt').value.replace(reptxt,"");


  // console.log( document.querySelector('#txt').value);
  
  element.parentNode.remove();
  document.querySelector("#m-text-max").innerHTML='';

}


function multiselect(element){
  m=document.querySelector("#m-text");



  value=element.value
  console.log(value)
 
 
  const metricvalues=metricoptions
  console.log(metricvalues)
  

  
 
 

    if (metricvalues.includes(value)) 
    {
    
      
      if (m.children.length<5) {
        const sranges=document.querySelectorAll('.smetrics')
        const sranges_=['defaultValUe']
        
        for (i=0; i<sranges.length; i++){
          sranges_.push(sranges[i].innerHTML.replace( /(<([^>]+)>)/ig, '').trim())
        }
 
        if (sranges_.includes(value)){
          console.log('includes')
        }
        else
        {
          document.querySelector('#m-text').innerHTML+="<span class='companies smetrics ml-2 mr-2'>"+value+"<i class='ml-2 fa fa-times-circle' onclick='removemet(this)'></i> </span>"
        }
        }
        else
        {
          document.querySelector("#m-text-max").innerHTML="<span class='companies mr-2'> Max nuumber of metrics reached. </span>";
        }



    }
  
  element.value='';
 

}

function submitdata(){


  t_=document.getElementById("text").innerHTML.replace(/<[^>]*>/g, "|||");
  t_=t_.replace(/&amp;/,"&");
  console.log(t_);
  document.querySelector('#txt').value=t_;
  console.log(document.querySelector('#txt').value);


  m_=document.getElementById("m-text").innerHTML.replace(/<[^>]*>/g, "|||");
  m_=m_.replace(/&amp;/,"&");
  console.log(m_);
  document.querySelector('#txt-metrics').value=m_;
  console.log(document.querySelector('#txt-metrics').value);


  r_=document.getElementById("m-ranges").innerHTML.replace(/<[^>]*>/g, "|||");
  r_=r_.replace(/&amp;/,"&");
  console.log(m_);
  document.querySelector('#range-metrics').value=r_;
  console.log(document.querySelector('#range-metrics').value);


}

function fromfunc(){

  el=document.querySelector("#from");
  document.querySelector("#from-text").innerHTML="<span class='companies'>"+el.value +"</span>"
}

function tofunc(){
  el=document.querySelector("#to");
  document.querySelector("#to-text").innerHTML="<span class='companies'>"+el.value +"</span>"
}

function resetdata(){



document.querySelector('#c-text').innerHTML='';
document.querySelector('#type-text').innerHTML='';

document.querySelector('#sc-text').innerHTML='';

document.querySelector('#cat-text').innerHTML='';



document.querySelector('#m-text').innerHTML='';

document.querySelector('#from-text').innerHTML='';

document.querySelector('#to-text').innerHTML='';

document.querySelector('#text').innerHTML='';

document.querySelector('#types').value='';

document.querySelector('#sc').innerHTML='';

document.querySelector('#cat_').innerHTML='';


document.querySelector(".metrics-html").innerHTML='';

document.querySelector('#m-ranges').innerHTML='';

document.querySelector('#m-ranges-max').innerHTML='';

document.querySelector('#m-text-max').innerHTML='';

document.querySelector('#from').value='';

document.querySelector('#to').value='';


document.querySelector('#from-text').innerHTML='';

document.querySelector('#to-text').innerHTML='';



document.querySelector('#m-text-max').innerHTML='';







}

function exportTableToExcel(tableID, filename = ''){
  var downloadLink;
  var dataType = 'application/vnd.ms-excel';
  var tableSelect = document.getElementById(tableID);
  var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');
  
  // Specify file name
  filename = filename?filename+'.xls':'excel_data.xls';
  
  // Create download link element
  downloadLink = document.createElement("a");
  
  document.body.appendChild(downloadLink);
  
  if(navigator.msSaveOrOpenBlob){
      var blob = new Blob(['\ufeff', tableHTML], {
          type: dataType
      });
      navigator.msSaveOrOpenBlob( blob, filename);
  }else{
      // Create a link to the file
      downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
  
      // Setting the file name
      downloadLink.download = filename;
      
      //triggering the function
      downloadLink.click();
  }
}