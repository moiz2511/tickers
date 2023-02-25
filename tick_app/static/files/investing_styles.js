document.addEventListener("DOMContentLoaded", function () {
  console.log("JS RUnning");
});

async function addInvestingStyle() {
  console.log("add InvestingStyle Function Triggered")
  let styleVal = document.getElementById("addRowStyle").value;
  let mentorVal = document.getElementById("addRowMentor").value;
  let strategyNameVal = document.getElementById("addRowStrategyName").value;
  let sourceVal = document.getElementById("addRowSource").value;
  let videoUrlVal = document.getElementById("addRowVideoUrl").value;
  console.log("Data Log Metric")
  console.log(styleVal, mentorVal, strategyNameVal, sourceVal, videoUrlVal);
  console.log("Data Log Metric Done")
  try {
    const url = "http://127.0.0.1:8000/context/investingStyle";
    const data = {
      style: styleVal,
      mentor: mentorVal,
      strategy_name: strategyNameVal,
      source: sourceVal,
      video_url: videoUrlVal
    };
    console.log(data)

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      let user = await response.json();
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
  const tableRow = document.getElementById("investing-style-table");
  tableRow.innerHTML += `<tr>
    <td><input name="addRowStyle" id="addRowStyle" value=""/></td>
    <td><input name="addRowMentor" id="addRowMentor" value=""/></td>
    <td><input name="addRowStrategyName" id="addRowStrategyName" value=""/></td>
    <td><input name="addRowSource" id="addRowSource" value=""/></td>
    <td><input name="addRowVideoUrl" id="addRowVideoUrl" value=""/></td>
    <td class="hidden-icon" style="border: None;" data-id='stratagey-row-' onclick="addInvestingStyle()">
      <i class="fa fa-save" aria-hidden="true"></i> 
      </td>
    </tr>`;
}


async function getStrat() {
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  styleFilter = document.getElementById("styleFilter").value;
  mentorFilter = document.getElementById("mentorFilter").value;

  let url = window.location.search;
  let id;
  if (url) {
    let nid = url.substring(url.lastIndexOf("page="));
    let nnid = nid.split("&")[0]
    id = nnid.split("=")[1]
    let cat = url.substring(url.lastIndexOf("style=")).split("=")[1];
    styleFilter = cat.split("&")[0];
    mentorFilter = url.substring(url.lastIndexOf("mentor=")).split("=")[1].replaceAll("%20", " ")
  }
  else {
    id = 1;
  }
  var data = {
    style: null,
    mentor: null,
    page: id,
  };
  try {
    const url = "http://127.0.0.1:8000/context/investingStyle/get";

    if (styleFilter == "null" && mentorFilter == "null") {
      data = {
        style: null,
        mentor: null,

        // search_name: "All",
        page: id,
      };
    } else if (styleFilter == "null") {
      data = {
        // search_metric: "All",

        style: null,
        mentor: mentorFilter,
        page: id,
      };
    } else if (mentorFilter == "null") {
      data = {
        style: styleFilter,
        mentor: null,
        page: id,
      };
    }
    else {
      data = {
        style: styleFilter,
        mentor: mentorFilter,
        page: id,
      };
    }
    // url =  url //+ "?page=1&style=All&mentor=All"
    const response = await fetch(url, {
      method: "POST",
      headers: {
        // "Accept": "application/json",
        'Content-Type': 'application/json',
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
    const url = "http://127.0.0.1:8000/context/investingStyle";

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

async function getMentorsByStyleDropDown(style) {
  try {
    console.log(style)
    const url = "http://127.0.0.1:8000/context/mentorsByStyle";
    body = {"style": style}
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
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
    const url = "http://127.0.0.1:8000/context/investingStyle/delete";
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
  let styleVal = document.getElementById("investingStyleUpdateID").value;
  let mentorVal = document.getElementById("mentorUpdateID").value;
  let strategyNameVal = document.getElementById("strategyNameUpdateID").value;
  let sourceVal = document.getElementById("sourceUpdateID").value;
  let videoUrlVal = document.getElementById("videoUrlUpdateID").value;
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  try {
    const url = "http://127.0.0.1:8000/context/investingStyle/edit";
    const data = {
      id: el,
      style: styleVal,
      mentor: mentorVal,
      strategy_name: strategyNameVal,
      source: sourceVal,
      video_url: videoUrlVal
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
