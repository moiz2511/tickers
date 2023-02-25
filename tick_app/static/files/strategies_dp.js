document.addEventListener("DOMContentLoaded", function () {
  console.log("JS RUnning");
});

async function addMetric() {
  let strategyVal = document.getElementById("addRowStrategy").value;
  let metricVal = document.getElementById("addRowMetric").value;
  let operatorVal = document.getElementById("addRowOperator").value;
  let rangeVal = document.getElementById("addRowRange").value;

  console.log(strategyVal, metricVal, operatorVal, rangeVal);

  try {
    const url = "http://127.0.0.1:8000/strategy";
    const data = {
      strategy: strategyVal,
      metric: metricVal,
      operator: operatorVal,
      range: rangeVal,
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
    <td><input name="addRowStrategy" id="addRowStrategy" value=""/></td>
    <td><input name="addRowMetric" id="addRowMetric" value=""/></td>
    <td><input name="addRowOperator" id="addRowOperator" value=""/></td>
    <td><input name="addRowRange" id="addRowRange" value=""/></td>
    <td class="hidden-icon" style="border: None;" data-id='stratagey-row-' onclick="addMetric()">
      <i class="fa fa-save" aria-hidden="true"></i> 
      </td>
      
    </tr>`;
}

async function getStrat() {
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  d = document.getElementById("dropDownVal").value;
  let url = window.location.search;
  console.log("URL ", url);
  // console.log(url);
  let nid = url.substring(url.lastIndexOf("id="));
  console.log("nid", nid);
  let nnid = nid.split("&")[0]
  console.log("nnid", nnid)

  let id = nnid.split("=")[1]
  let catogery = url.substring(url.lastIndexOf("category=")).split("=")[1];
  d = catogery
  console.log("Mahendra ", id, catogery)
  if (!url) {
    id = 1;
  }
  console.log(id);
  if (d == null) {
    d = null;
  }
  var data = {
    search_strategy: null,
    page: id,
  };
  try {
    const url = "http://127.0.0.1:8000/getstrategy";
    if (d == "null") {
      data = {
        search_strategy: null,
        page: id,
      };
    } else {
      data = {
        search_strategy: d,
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
    const url = "http://127.0.0.1:8000/deletestrategy";
    const data = {
      strategy_id: el,
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
  let strategyVal = document.getElementById("strategyUpdateID").value;
  let metricVal = document.getElementById("metricUpdateID").value;
  let operatorVal = document.getElementById("operatorUpdateID").value;
  let rangeVal = document.getElementById("rangeUpdateID").value;
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  try {
    const url = "http://127.0.0.1:8000/editstrategy";
    const data = {
      strategy_id: el,
      new_strategy: strategyVal,
      new_metric: metricVal,
      new_operator: operatorVal,
      new_range: rangeVal,
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
      location.reload();
      document.getElementById("tableDiv").className = "";
      document.getElementById("spinner").className = "hideTable";
      return user;
    } else {
      console.log("not ok");
      document.getElementById("tableDiv").className = "";
      document.getElementById("spinner").className = "hideTable";
      console.log(response);
      let rangeVal = document.getElementById("rangeUpdateID");
      rangeVal.value = "Please enter a valid number";
      rangeVal.className = "error";
    }
  } catch (error) {
    console.log("error", error);
  }
}
