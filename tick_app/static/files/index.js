document.addEventListener('DOMContentLoaded', function () {
  document.querySelector("#file_import").style.display = "None";
  console.log("JS RUnning")
  document.querySelector('#api_title').style.fontWeight = "bold";

  replace_value();

  const name_text = document.querySelector('#myInput');

  autocomplete(document.getElementById("myInput"));


  console.log(document.querySelector('#file_m').innerHTML.length);

  if (document.querySelector('#file_m').innerHTML.length > 1) {

    display_file()
  }

  var delayInMilliseconds = 5000; //1 second

  setTimeout(function () {
    //your code to be executed after 5 second
    document.querySelector('#file_m').remove();

  }, delayInMilliseconds);






});

function display_api() {
  document.querySelector("#file_import").style.display = "None";
  document.querySelector("#api_call").style.display = "block";
  document.querySelector('#api_title').style.fontWeight = "bold";
  document.querySelector('#file_title').style.fontWeight = "normal";

}

function display_file() {
  document.querySelector("#api_call").style.display = "None";
  document.querySelector("#file_import").style.display = "block";
  document.querySelector('#api_title').style.fontWeight = "normal";
  document.querySelector('#file_title').style.fontWeight = "bold";

}


async function fetch_sector_by_exchange() {
  const exchangeVal = document.getElementById("exchangeFilter").value
  try {
    const url = "http://127.0.0.1:8000/getSectorByExchange";
    body = { "exchange": exchangeVal }
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });
    if (response.ok) {
      console.log("ok");
      let resp = await response.json();
      // console.log(document.getElementById("exchange").value)
      $('#sectorFilter').children().remove()
      let optAll = document.createElement("option");
      optAll.value = "All"; //or i, depending on what you need to do
      optAll.innerHTML = "All";
      $('#sectorFilter').append(optAll);
      for (let i = 0; i < resp.sectors.length; i++) {
        let opt = document.createElement("option");
        opt.value = resp.sectors[i].sector; //or i, depending on what you need to do
        opt.innerHTML = resp.sectors[i].sector;
        $('#sectorFilter').append(opt); //Chuck it into the dom here if you want
      }
      return;
    } else {
      console.log("not ok");
      console.log(response);
      setError(response.message);
    }
    // return res.json(); // parses JSON response into native JavaScript objects
  } catch (error) {
    console.log("error", error);
  }
}

async function fetch_industry_by_exchange_and_sector() {
  let exchangeVal = document.getElementById("exchangeFilter").value
  let sectorVal = document.getElementById("sectorFilter").value
  let body = ""
  try {
    const url = "http://127.0.0.1:8000/getIndustryByExchangeSector";
    if ((exchangeVal != null && exchangeVal != "All") && (sectorVal != null && sectorVal != "All")) {
      body = {
        "exchange": exchangeVal,
        "sector": sectorVal
      }
    } else if (exchangeVal != null && exchangeVal != "All") {
      body = {
        "exchange": exchangeVal,
        "sector": "All"
      }
    } else if (sectorVal != null && sectorVal != "All") {
      body = {
        "sector": sectorVal,
        "exchange": "All"
      }
    } else {
      body = {
        "sector": "All",
        "exchange": "All"
      }
    }
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });
    if (response.ok) {
      console.log("ok");
      let resp = await response.json();
      // console.log(document.getElementById("exchange").value)
      $('#industryFilter').children().remove()
      let optAll = document.createElement("option");
      optAll.value = "All"; //or i, depending on what you need to do
      optAll.innerHTML = "All";
      $('#industryFilter').append(optAll);
      for (let i = 0; i < resp.industries.length; i++) {
        let opt = document.createElement("option");
        opt.value = resp.industries[i].industry; //or i, depending on what you need to do
        opt.innerHTML = resp.industries[i].industry;
        $('#industryFilter').append(opt); //Chuck it into the dom here if you want
      }
      return;
    } else {
      console.log("not ok");
      console.log(response);
      setError(response.message);
    }
    // return res.json(); // parses JSON response into native JavaScript objects
  } catch (error) {
    console.log("error", error);
  }
}

async function fetch_companies_by_exchange_sector_and_industry() {
  let exchangeVal = document.getElementById("exchangeFilter").value
  let sectorVal = document.getElementById("sectorFilter").value
  let industryVal = document.getElementById("industryFilter").value
  let body = ""
  try {
    const url = "http://127.0.0.1:8000/getCompaniesByExchangeSectorIndustry";
    if ((exchangeVal != null && exchangeVal != "All") && (sectorVal != null && sectorVal != "All") && (industryVal != null && industryVal != "All")) {
      body = {
        "exchange": exchangeVal,
        "sector": sectorVal,
        "industry": industryVal,
      }
    } else if ((exchangeVal != null && exchangeVal != "All") && (sectorVal != null && sectorVal != "All")) {
      body = {
        "exchange": exchangeVal,
        "sector": sectorVal,
        "industry": "All",
      }
    } else if ((exchangeVal != null && exchangeVal != "All") && (industryVal != null && industryVal != "All")) {
      body = {
        "sector": "All",
        "exchange": exchangeVal,
        "industry": industryVal,
      }
    } else if ((sectorVal != null && sectorVal != "All") && (industryVal != null && industryVal != "All")) {
      body = {
        "sector": sectorVal,
        "exchange": "All",
        "industry": industryVal,
      }
    } else if (exchangeVal != null && exchangeVal != "All") {
      body = {
        "sector": "All",
        "exchange": exchangeVal,
        "industry": "All",
      }
    } else if (industryVal != null && industryVal != "All") {
      body = {
        "sector": "All",
        "exchange": "All",
        "industry": industryVal,
      }
    } else if (sectorVal != null && sectorVal != "All") {
      body = {
        "sector": sectorVal,
        "exchange": "All",
        "industry": "All",
      }
    } else {
      body = {
        "sector": "All",
        "exchange": "All",
        "industry": "All",
      }
    }
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });
    if (response.ok) {
      console.log("ok");
      let resp = await response.json();
      // console.log($('#companiesFilter').getElementsByClassName("inner show"))
      $('#companiesFilter').children().remove()
      // let optAll = document.createElement("option");
      // optAll.value = "All"; //or i, depending on what you need to do
      // optAll.innerHTML = "All";
      // $('#companiesFilter').append(optAll);
      // for (let i = 0; i < resp.companies.length; i++) {
      //   let opt = document.createElement("option");
      //   // opt.value = resp.companies[i].company_name; //or i, depending on what you need to do
      //   opt.innerHTML = resp.companies[i].company_name;
      //   $('#companiesFilter').append(opt); //Chuck it into the dom here if you want
      // }
      // $('#companiesFilter').selectpicker('rebuild');

      var ul = document.getElementById("companiesFilter"); // moved this out of the loop for a bit of performance optimization.
    
      $.each(resp.companies, function(i, v) {
          var li = document.createElement("option");
          var linkText = document.createTextNode(v.company_name);
          li.appendChild(linkText);
          ul.appendChild(li);
      })

      $('.selectpicker').selectpicker('refresh');

      console.log("Companies Filter Updated!")
      console.log($('#companiesFilter').children())
      return;
    } else {
      console.log("not ok");
      console.log(response);
      setError(response.message);
    }
    // return res.json(); // parses JSON response into native JavaScript objects
  } catch (error) {
    console.log("error", error);
  }
}

function edit_file(el) {

  element = el.parentNode;
  element.style.display = "None";

  element.nextElementSibling.style.display = "table-row";





}

function save_data(el) {

  var data = el.getAttribute("data-id");
  console.log(data);
  document.querySelector('#txt-area').innerHTML = data + "\n";


  element = el.parentNode;
  prev_element = element.previousElementSibling
  prev_element = prev_element.innerHTML.replace(/<[^>]*>/g, "").replace(/\s\s+/g, '  ');
  console.log(prev_element);
  //document.querySelector('#txt-area').innerHTML+=prev_element + '\n';
  childrens = element.children


  var arrayLength = childrens.length;
  values = []
  for (var i = 0; i < arrayLength - 1; i++) {
    console.log(childrens[i].firstElementChild.value);
    values.push(childrens[i].firstElementChild.value);
    //Do something
  }


  for (var i = 0; i < values.length; i++) {
    console.log(values[i]);
    document.querySelector('#txt-area').innerHTML += values[i] + '  ';


    //Do something
  }




  console.log(document.querySelector('#txt-area').value);

}









function remove(el) {
  var element = el;

  text_ = (element.parentNode.innerHTML.replace(/<[^>]*>/g, ""));
  text_ = text_.replace(/\s+$/, "");
  text_ = text_.replace(/&amp;/, "&");
  reptxt = new RegExp(text_, 'g');
  console.log(reptxt);
  document.querySelector('#txt').value = document.querySelector('#txt').value.replace(reptxt, "");


  console.log(document.querySelector('#txt').value);

  element.parentNode.remove();
}

function replace_value() {
  headings = document.querySelectorAll('th')
  table = document.querySelector("#hide-row")
  year = table.children[1].innerHTML;

  console.log(headings)
  for (i = 0; i < headings.length; i++) {
    console.log(headings[i].innerHTML)
    if (headings[i].innerHTML.replace(/\s/g, '') == 'value1'.replace(/\s/g, '')) {
      console.log("yes")
      headings[i].innerHTML = parseInt(year) - 1
    }
    else if (headings[i].innerHTML.replace(/\s/g, '') == 'value2'.replace(/\s/g, '')) {
      headings[i].innerHTML = year
    }
  }
}

function deldata() {
  document.getElementById("api_call").className = "hideContent";
  document.getElementById("spinner").className = "spinner-border";
  document.getElementById("onSubmitMessage").className = "";
  t_ = document.getElementById("text").innerHTML.replace(/<[^>]*>/g, "|||");
  t_ = t_.replace(/&amp;/, "&");
  console.log(t_);
  document.querySelector('#txt').value = t_;
  console.log(document.querySelector('#txt').value);
}

function autocomplete(inp) {


  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function (e) {
    fetch(`/suggest/${inp.value}`)
      .then(response => response.json())
      .then(result => {
        console.log(result);
        window.arr = result
        console.log('delay')



        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false; }
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
            b.addEventListener("click", function (e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              t = document.getElementById("text")
              txt = document.getElementById("txt")
              if (t.children.length < 5) {
                t.innerHTML += "<span class=' companies mr-2'>" + this.getElementsByTagName("input")[0].value + " <i class='ml-2 fa fa-times-circle' onclick='remove(this)'></i> </span>"
                txt.value += this.getElementsByTagName("input")[0].value + "\n"
                console.log(txt.value);
                inp.value = '';
              }
              else {
                m = document.getElementById("max")
                inp.value = '';
                m.innerHTML = "Maximim number of companies reached."
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
  inp.addEventListener("keydown", function (e) {
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
