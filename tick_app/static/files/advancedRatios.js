document.addEventListener("DOMContentLoaded", function () {
  console.log("JS RUnning");
});

async function addMetric() {
  let measureVal = document.getElementById("addRowmeasure").value;
  let categoryVal = document.getElementById("addRowcategory").value;
  let metricVal = document.getElementById("addRowmetric").value;
  let codeVal = document.getElementById("addRowcode").value;
  let item1Val = document.getElementById("addRowitem1").value;
  let operator1Val = document.getElementById("addRowoperator1").value;
  let item2Val = document.getElementById("addRowitem2").value;
  let operator2Val = document.getElementById("addRowoperator2").value;
  let item3Val = document.getElementById("addRowitem3").value;
  let operator3Val = document.getElementById("addRowoperator3").value;
  let item4Val = document.getElementById("addRowitem4").value;
  let operator4Val = document.getElementById("addRowoperator4").value;
  let item5Val = document.getElementById("addRowitem5").value;

  try {
    const url = "http://127.0.0.1:8000/advanceratio";
    const data = {
      measure: measureVal,
      category: categoryVal,
      metric: metricVal,
      code: codeVal,
      item1: item1Val,
      operator1: operator1Val,
      item2: item2Val,
      operator2: operator2Val,
      item3: item3Val,
      operator3: operator3Val,
      item4: item4Val,
      operator4: operator4Val,
      item5: item5Val,
    };

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (response.ok) {
      console.log("ok");
      location.reload();

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

function add_metric(el) {
  const tableRow = document.getElementById("strategy-table");
  tableRow.innerHTML += `<tr>
      <td><input name="addRowmeasure" id="addRowmeasure" value=""/></td>
      <td><input name="addRowcategory" id="addRowcategory" value=""/></td>
      <td><input name="addRowmetric" id="addRowmetric" value=""/></td>
      <td><input name="addRowcode" id="addRowcode" value=""/></td>
      <td><input name="addRowitem1" id="addRowitem1" value=""/></td>
      <td><input name="addRowoperator1" id="addRowoperator1" value=""/></td>
      <td><input name="addRowitem2" id="addRowitem2" value=""/></td>
      <td><input name="addRowoperator2" id="addRowoperator2" value=""/></td>
      <td><input name="addRowitem3" id="addRowitem3" value=""/></td>
      <td><input name="addRowoperator3" id="addRowoperator3" value=""/></td>
      <td><input name="addRowitem4" id="addRowitem4" value=""/></td>
      <td><input name="addRowoperator4" id="addRowoperator4" value=""/></td>
      <td><input name="addRowitem5" id="addRowitem5" value=""/></td>

  
      <td class="hidden-icon" style="border: None;" data-id='stratagey-row-' onclick="addMetric()">
        <i class="fa fa-save" aria-hidden="true"></i> 
        </td>
        
      </tr>`;
}

async function getStrat() {
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  let url = window.location.search;
  let id = url.substring(url.lastIndexOf("=") + 1);
  console.log(url);

  if (!url) {
    id = 1;
  }

  var data = {
    page: id,
  };
  try {
    const url = "http://127.0.0.1:8000/getadvanceratio";

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
    const url = "http://127.0.0.1:8000/getstrategy";

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
    const url = "http://127.0.0.1:8000/deleteadvanceratio";
    const data = {
      id: el,
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

  //   let element = document.getElementById(rowId);
  //   let measureVal = document.getElementById(measureTdId).value;
  //   let categoryVal = document.getElementById(categoryTdId).value;
  let metricVal = document.getElementById("metricARUpdateID").value;
  let codeVal = document.getElementById("codeUpdateID").value;
  //   let item1Val = document.getElementById(item1TdId).value;
  //   let operator1Val = document.getElementById(operator1TdId).value;
  //   let item2Val = document.getElementById(item2TdId).value;
  //   let operator2Val = document.getElementById(operator2TdId).value;
  //   let item3Val = document.getElementById(item3TdId).value;
  //   let operator3Val = document.getElementById(operator3TdId).value;
  //   let item4Val = document.getElementById(item4TdId).value;
  //   let operator4Val = document.getElementById(operator4TdId).value;
  //   let item5Val = document.getElementById(item5TdId).value;
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  try {
    const url = "http://127.0.0.1:8000/editadvanceratio";
    const data = {
      id: el,
      new_metric: metricVal,
      new_code: codeVal,
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
