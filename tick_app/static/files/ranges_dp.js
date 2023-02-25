document.addEventListener("DOMContentLoaded", function () {
  console.log("JS RUnning");
});

async function addMetric() {
  let metricVal = document.getElementById("metricAddRow").value;
  let nameVal = document.getElementById("nameAddRow").value;
  let sourceVal = document.getElementById("sourceAddRow").value;
  let minVal = document.getElementById("minAddRow").value;
  let maxVal = document.getElementById("maxAddRow").value;
  let belowVal = document.getElementById("belowAddRow").value;
  let equalVal = document.getElementById("equalAddRow").value;
  let betweenVal = document.getElementById("betweeenAddRow").value;
  let aboveVal = document.getElementById("aboveAddRow").value;

  try {
    const url = "http://127.0.0.1:8000/metric";
    const data = {
      
      metric: metricVal,
      name: nameVal,
      source: sourceVal,
      min: minVal,
      max: maxVal,
      below_min: belowVal,
      equal_min_max: equalVal,
      between_min_max: betweenVal,
      above_max: aboveVal,
    };

    const response = await fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    if (response.ok) {
      console.log("ok");
      // let user = await response.json();
      location.reload();

      // console.log("DATA", user);
      return user;
    } else {
      console.log("not ok");
      console.log("nahi mila",response);
    }

    // return res.json(); // parses JSON response into native JavaScript objects
  } catch (error) {
    console.log("error", error);
  }
}

function add_metric() {
  const tableRow = document.getElementById("metric-table");
  tableRow.innerHTML += `<tr>
  <td> <input name="metricUpdate" value='' id="metricAddRow"/></td>
  <td> <input name="nameUpdate" value='' id="nameAddRow"/></td>
  <td> <input name="sourceUpdate" value='' id="sourceAddRow"/></td>
  <td> <input name="minUpdate" value='' id="minAddRow"/></td>
  <td> <input name="maxUpdate" value='' id="maxAddRow"/></td>
  <td> <input name="belowUpdate" value='' id="belowAddRow"/></td>
  <td> <input name="equalUpdate" value='' id="equalAddRow"/></td>
  <td> <input name="betweeenUpdate" value='' id="betweeenAddRow"/></td>
  <td> <input name="aboveUpdate" value=''' id="aboveAddRow"/></td>
  <td style="border: None;" onclick="addMetric()">            
    <i class="fa fa-floppy-o" aria-hidden="true"></i> 
  </td>
  
  </tr>`;
}

async function getStrat() {
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  dropdown_met = document.getElementById("dropdown_metric").value;
  dropdown_nam = document.getElementById("dropdown_name").value;

  // if (dropdown_met == "null") {
  //   console.log(dropdown_met);
  // }
  
  let url = window.location.search;
  let id;
  let catogery="All"
  let catogery2="All"
  if(url){
    console.log("86url",url);
    // let id = url.substring(url.lastIndexOf("id=") + 1);
    // console.log(url);
    let nid = url.substring(url.lastIndexOf("id="));
    let nnid = nid.split("&")[0]
  
     id = nnid.split("=")[1]
    let cat=url.substring(url.lastIndexOf("category=")).split("=")[1];
     catogery=cat.split("&")[0];
    dropdown_met = catogery;
    // catogery2 = url.substring(url.lastIndexOf("category2=")).split("=")[1];
    catogery2 = url.substring(url.lastIndexOf("category2=")).split("=")[1].replaceAll("%20"," ")
// let cat2= url.substring(url.lastIndexOf("category2=")).split("=")[1]
// let cats2=cat2.split("%20")
// category2=cats2.toString().replace(","," ").replace(","," ").replace(","," ").replace(","," ")

    dropdown_nam=catogery2;
  
    console.log("aadarsh ", id , dropdown_met)
    console.log("pathak",id,dropdown_nam);
   
    
  }
  // console.log("86url",url);
  // // let id = url.substring(url.lastIndexOf("id=") + 1);
  // // console.log(url);
  // let nid = url.substring(url.lastIndexOf("id="));
  // let nnid = nid.split("&")[0]

  // let id = nnid.split("=")[1]
  // let cat=url.substring(url.lastIndexOf("category=")).split("=")[1]
  //  catogery=cat.split("&")[0]
  // dropdown_met = catogery
  // catogery2 = url.substring(url.lastIndexOf("category2=")).split("=")[1];
  // dropdown_nam=catogery2

  // console.log("aadarsh ", id , dropdown_met)
  // console.log("pathak",id,dropdown_nam);
  // // let catogery2 = url.substring(url.lastIndexOf("category2=")).split("=")[2];
  // // dropdown_nam = catogery2
  // // console.log("xaa",catogery2)
  else  {
    id = 1;
    // search_metric="All"

  
    // search_name=null

  }
if(dropdown_met==null){
  dropdown_met=null
}
if(dropdown_nam==null){
  // dropdown_nam="All"
  dropdown_nam=null

}
  var data = {
    search_metric: "All",

    search_name: "All",
    page: id,
  };
  try {
    const url = "http://127.0.0.1:8000/getmetric";

    if (dropdown_met == "null" && dropdown_nam == "null") {
      data = {
        search_metric: "All",
        search_name: "All",

        // search_name: "All",
        page: id,
      };
    } else if (dropdown_met == "null") {
      data = {
        // search_metric: "All",

        search_metric:"All",
        search_name: dropdown_nam,
        page: id,
      };
    } else if (dropdown_nam == "null") {
      data = {
        search_metric:dropdown_met,
        search_name: "All",
        page: id,
      };
    } 

    
    else {
      data = {
        search_metric: dropdown_met,
        search_name: dropdown_nam,
        page: id,
      };
    }

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    if (response.ok) {
      console.log("ok");
      let user = await response.json();
      document.getElementById("tableDiv").className = "";
      document.getElementById("spinner").className = "hideTable";
      return user;
    } else {
      console.log("not ok");
      console.log(response);
    }

    // return res.json(); // parses JSON response into native JavaScript objects
  } catch (error) {
    console.log("error", error);
  }
}

async function getDropDown() {
  try {
    const url = "http://127.0.0.1:8000/getmetric";

    const response = await fetch(url, {
      method: "GET",
    });
    if (response.ok) {
      console.log("ok");
      let user = await response.json();
      console.log("USER", user);
      return user;
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

async function del(el) {
  console.log(el);

  try {
    const url = "http://127.0.0.1:8000/deletemetric";
    const data = {
      metric_id: el,
    };

    const response = await fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    if (response.ok) {
      console.log("ok");
      // let user = await response.json();
      location.reload();

      // console.log("DATA", user);
      return user;
    } else {
      console.log("not ok");
      console.log(response);
    }

    // return res.json(); // parses JSON response into native JavaScript objects
  } catch (error) {
    console.log("error", error);
  }
  // console.log(el.getAttribute("data-id"));
  // rowid = el.getAttribute("data-id");
  // document.querySelector("#metric_add").value = "del-metric" + rowid;
}

async function save_row(el) {
  console.log(el);

  let metricVal = document.getElementById("metricUpdateID").value;
  let nameVal = document.getElementById("nameUpdateID").value;
  let sourceVal = document.getElementById("sourceUpdateID").value;
  let minVal = document.getElementById("minUpdateID").value;
  let maxVal = document.getElementById("maxUpdateID").value;
  let belowVal = document.getElementById("belowUpdateID").value;
  let equalVal = document.getElementById("equalUpdateID").value;
  let betweenVal = document.getElementById("betweeenUpdateID").value;
  let aboveVal = document.getElementById("aboveUpdateID").value;

  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  try {
    const url = "http://127.0.0.1:8000/editmetric";
    const data = {
      metric_id: el,
      new_metric: metricVal,
      new_name: nameVal,
      new_source: sourceVal,
      new_min: minVal,
      new_max: maxVal,
      new_below_min: belowVal,
      new_equal_min_max: equalVal,
      new_between_min_max: betweenVal,
      new_above_max: aboveVal,
    };
    const response = await fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    if (response.ok) {
      console.log("ok");
      // let user = await response.json();
      location.reload();
      document.getElementById("tableDiv").className = "";
      document.getElementById("spinner").className = "hideTable";

      // console.log("DATA", user);
      return user;
    } else {
      console.log("not ok");
      document.getElementById("tableDiv").className = "";
      document.getElementById("spinner").className = "hideTable";
      console.log(response);
      let minErr = document.getElementById("minUpdateID");

      minErr.value = "Please enter a valid number";
      minErr.className = "error";
      let maxErr = document.getElementById("maxUpdateID");

      maxErr.value = "Please enter a valid number";
      maxErr.className = "error";
    }
  } catch (error) {
    console.log("error", error);
  }
}
