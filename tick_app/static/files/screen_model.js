document.addEventListener("DOMContentLoaded", function () {
  console.log("JS RUnning");
});

async function getStrat() {
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  screenModelFilter = document.getElementById("screenModelFilter").value;

  let url = window.location.search;
  let id;
  if (url) {
    let nid = url.substring(url.lastIndexOf("page="));
    let nnid = nid.split("&")[0]
    id = nnid.split("=")[1]
    let cat = url.substring(url.lastIndexOf("screenModel=")).split("=")[1];
    screenModelFilter = cat.split("&")[0].replaceAll("%20", " ");
  }
  else {
    id = 1;
  }
  var data = {
    search_strategy: null,
    page: id,
  };
  try {
    const url = "http://127.0.0.1:8000/getstrategy";

    if (screenModelFilter == "null") {
      data = {
        search_strategy: null,
        // search_name: "All",
        page: id,
      };
    }
    else {
      data = {
        search_strategy: screenModelFilter,
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
    body = { "style": style }
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

async function getScreenModelsByMentorDropDown(mentor) {
  try {
    console.log(mentor)
    const url = "http://127.0.0.1:8000/context/analysisModelsByMentor";
    body = { "mentor": mentor }
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

async function getCompaniesByMetricFilters(data) {
  try {
    const url = "http://127.0.0.1:8000/context/companies/filter";
    body = { "filters": data, "page": 1 }
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
