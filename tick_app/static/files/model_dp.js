document.addEventListener("DOMContentLoaded", function () {
  console.log("JS RUnning");
});

async function addModel() {
  let modelVal = document.getElementById("modelAddRow").value;
  let categoryVal = document.getElementById("categoryAddRow").value;
  let questionVal = document.getElementById("questionAddRow").value;
  let metricVal = document.getElementById("metricAddRow").value;
  let toolVal = document.getElementById("toolAddRow").value;
  let rangeVal = document.getElementById("rangeAddRow").value;
  let fromVal = document.getElementById("fromAddRow").value;
  let toVal = document.getElementById("toAddRow").value;
  let displayVal = document.getElementById("displayAddRow").value;

  try {
    const url = "http://127.0.0.1:8000/model";
    const data = {
      model: modelVal,
      category: categoryVal,
      question: questionVal,
      metric: metricVal,
      tool: toolVal,
      range: rangeVal,
      model_from: fromVal,
      model_to: toVal,
      display: displayVal,
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
}

function add_model() {
  const tableRow = document.getElementById("model-table");
  tableRow.innerHTML += `<tr>
    <td> <input name="modelUpdate" value='' id="modelAddRow"/></td>
    <td> <input name="categoryUpdate" value='' id="categoryAddRow"/></td>
    <td> <input name="questionUpdate" value='' id="questionAddRow"/></td>
    <td> <input name="metricUpdate" value='' id="metricAddRow"/></td>
    <td> <input name="toolUpdate" value='' id="toolAddRow"/></td>
    <td> <input name="rangeUpdate" value='' id="rangeAddRow"/></td>
    <td> <input name="fromUpdate" value='' id="fromAddRow"/></td>
    <td> <input name="toUpdate" value='' id="toAddRow"/></td>
    <td> <input name="displayUpdate" value=''' id="displayAddRow"/></td>
    <td style="border: None;" onclick="addModel()">            
      <i class="fa fa-floppy-o" aria-hidden="true"></i> 
    </td>
    
    </tr>`;
}

async function getModel() {
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  dropdown_mod = document.getElementById("dropdown_model").value;
  dropdown_cat = document.getElementById("dropdown_category").value;

  let url = window.location.search;
  let id;
  let catogery="All"
  let catogery2="All"
  console.log("########",id)
  if(url) {
    console.log("98", url);
    let nid = url.substring(url.lastIndexOf("id="));
    let nnid = nid.split("&")[0];
    id = nnid.split("=")[1];

    let cat = url.substring(url.lastIndexOf("category=")).split("=")[1];
    catogery = cat.split("&")[0];
    dropdown_mod = catogery;
    catogery2 = url.substring(url.lastIndexOf("category2=")).split("=")[1].replaceAll("%20"," ");
    dropdown_cat = catogery2;
    console.log("cat1", id, dropdown_mod);
    console.log("cat2", id, dropdown_cat);
    
  } 
  
  
  
  
  else if(!url){
    id = 1;
  }
console.log("jsid",id)

  if (dropdown_mod == null) {
    dropdown_mod = null;
  }
  if (dropdown_cat == null) {
    dropdown_cat = null;
  }

  var data = {
    search_model: "All",
    search_category: "All",
    page:id,
  };
  try {
    const url = "http://127.0.0.1:8000/getmodel";

    if (dropdown_mod == "null" && dropdown_cat == "null") {
      data = {
        search_model: "All",
        search_category: "All",
        page:id,
      };
    } else if (dropdown_mod == "null") {
      data = {
        search_model: "All",
        search_category: dropdown_cat,
        page:id,
      };
    } else if (dropdown_cat == "null") {
      data = {
        search_model: dropdown_mod,
        search_category: "All",
        page:id,
      };
    } else {
      data = {
        search_model: dropdown_mod,
        search_category: dropdown_cat,
        page:id,
      };
    }
console.log("netaggregateviewwork data",data);
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
    const url = "http://127.0.0.1:8000/getmodel";

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
    const url = "http://127.0.0.1:8000/deletemodel";
    const data = {
      model_id: el,
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

  let modelVal = document.getElementById("modelUpdateID").value;
  let categoryVal = document.getElementById("categoryUpdateID").value;
  let questionVal = document.getElementById("questionUpdateID").value;
  let metricVal = document.getElementById("metricUpdateID").value;
  let toolVal = document.getElementById("toolUpdateID").value;
  let rangeVal = document.getElementById("rangeUpdateID").value;
  let fromVal = document.getElementById("fromUpdateID").value;
  let toVal = document.getElementById("toUpdateID").value;
  let displayVal = document.getElementById("displayUpdateID").value;

  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  try {
    const url = "http://127.0.0.1:8000/editmodel";
    const data = {
      model_id: el,
      new_model: modelVal,
      new_category: categoryVal,
      new_question: questionVal,
      new_metric: metricVal,
      new_tool: toolVal,
      new_range: rangeVal,
      new_model_from: fromVal,
      new_model_to: toVal,
      new_display: displayVal,
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
    }
  } catch (error) {
    console.log("error", error);
  }
}
