document.addEventListener("DOMContentLoaded", function () {
  console.log("JS Aadarsh");
});

async function addModel() {
  let viewVal = document.getElementById("viewAddRow").value;
  let nameVal = document.getElementById("nameAddRow").value;
  let itmVal = document.getElementById("item1AddRow").value;
  let op1Val = document.getElementById("operator1AddRow").value;
  let itm2Val = document.getElementById("item2AddRow").value;
  let op2Val = document.getElementById("operator2AddRow").value;
  let itm3Val = document.getElementById("item3AddRow").value;
  let op3Val = document.getElementById("operator3AddRow").value;
  let itm4Val = document.getElementById("item4AddRow").value;
  let opr4Val = document.getElementById("operator4AddRow").value;
  let itm5Val = document.getElementById("item5AddRow").value;

  try {
    const url = `http://127.0.0.1:8000/aggregateview`;
    const data = {
      
      view: viewVal,
    name: nameVal,
    item1: itmVal,
      operator1: op1Val,
      item2: itm2Val,
      operator2: op2Val,
    item3: itm3Val,
      operator3: op3Val,
      item4: itm4Val,
      operator4:opr4Val,
      item5:itm5Val,
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

      console.log("DATA", user);
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
async function handleApidown()
{
  var data=await getDropDown()

  const{dropdown_view,dropdown_item,dropdown_operator}=data
  const droppp=document.getElementById("viewAddRow")
 
   for (let i = 0; i < dropdown_view.length; i++) {
     let opt = document.createElement("option");
     opt.value = dropdown_view[i]; //or i, depending on what you need to do
     opt.innerHTML = dropdown_view[i]; 
     $('#viewAddRow').append(opt); //Chuck it into the dom here if you want
  } 
  const dropItem1=document.getElementById("item1Addrow")
  for (let i = 0; i < dropdown_item.length; i++) {
    let opt = document.createElement("option");
    opt.value = dropdown_item[i]; //or i, depending on what you need to do
    opt.innerHTML = dropdown_item[i]; 
    $('#item1AddRow').append(opt); //Chuck it into the dom here if you want
 } 
 const dropOperator=document.getElementById("operator1AddRow")
 for (let i = 0; i < dropdown_operator.length; i++) {
  let opt = document.createElement("option");
  opt.value = dropdown_operator[i]; //or i, depending on what you need to do
  opt.innerHTML = dropdown_operator[i]; 
  $('#operator1AddRow').append(opt); //Chuck it into the dom here if you want
} 
const dropItem2=document.getElementById("item2Addrow")
  for (let i = 0; i < dropdown_item.length; i++) {
    let opt = document.createElement("option");
    opt.value = dropdown_item[i]; //or i, depending on what you need to do
    opt.innerHTML = dropdown_item[i]; 
    $('#item2AddRow').append(opt); //Chuck it into the dom here if you want
 } 
 const dropOperator2=document.getElementById("operator2AddRow")
 for (let i = 0; i < dropdown_operator.length; i++) {
  let opt = document.createElement("option");
  opt.value = dropdown_operator[i]; //or i, depending on what you need to do
  opt.innerHTML = dropdown_operator[i]; 
  $('#operator2AddRow').append(opt); //Chuck it into the dom here if you want
} 
const dropItem3=document.getElementById("item3Addrow")
  for (let i = 0; i < dropdown_item.length; i++) {
    let opt = document.createElement("option");
    opt.value = dropdown_item[i]; //or i, depending on what you need to do
    opt.innerHTML = dropdown_item[i]; 
    $('#item3AddRow').append(opt); //Chuck it into the dom here if you want
 } 
 const dropOperator3=document.getElementById("operator3AddRow")
 for (let i = 0; i < dropdown_operator.length; i++) {
  let opt = document.createElement("option");
  opt.value = dropdown_operator[i]; //or i, depending on what you need to do
  opt.innerHTML = dropdown_operator[i]; 
  $('#operator3AddRow').append(opt); //Chuck it into the dom here if you want
} 
const dropItem4=document.getElementById("item4Addrow")
  for (let i = 0; i < dropdown_item.length; i++) {
    let opt = document.createElement("option");
    opt.value = dropdown_item[i]; //or i, depending on what you need to do
    opt.innerHTML = dropdown_item[i]; 
    $('#item4AddRow').append(opt); //Chuck it into the dom here if you want
 } 
 const dropOperator4=document.getElementById("operator4AddRow")
 for (let i = 0; i < dropdown_operator.length; i++) {
  let opt = document.createElement("option");
  opt.value = dropdown_operator[i]; //or i, depending on what you need to do
  opt.innerHTML = dropdown_operator[i]; 
  $('#operator4AddRow').append(opt); //Chuck it into the dom here if you want
} 
const dropItem5=document.getElementById("item5Addrow")
  for (let i = 0; i < dropdown_item.length; i++) {
    let opt = document.createElement("option");
    opt.value = dropdown_item[i]; //or i, depending on what you need to do
    opt.innerHTML = dropdown_item[i]; 
    $('#item5AddRow').append(opt); //Chuck it into the dom here if you want
 } 
 
}
async function add_model() {
  
  const tableRow = document.getElementById("model-table");
  
  handleApidown()
  tableRow.innerHTML += `<tr>
    <td>
      <select id="viewAddRow" name="viewUpdate">
    <option value="null">All</option>
  </select></td>
  
      <td> <input name="nameUpdate" value='' id="nameAddRow"/></td>
      <td> <select name="item1Update"  id="item1AddRow">
      <option value="null" autocomplete="true">All</option>
      </select></td>
      <td> <select name="opertor1Update" id="operator1AddRow">
      <option value="null">All</option>
      </select>
      </td>
      <td>
      <select id="item2AddRow" name="item2Update">
    <option value="null">All</option>
  </select></td>
      <td> <select name="opertor2Update" id="operator2AddRow">
      <option value="null">All</option>
      </select>
      </td>
      <td>
      <select id="item3AddRow" name="item3Update">
    <option value="null">All</option>
  </select></td>     
      <td> <select name="operator3Update"  id="operator3AddRow">
      <option value="null">All</option>
      </select></td>    
      <td>
      <select id="item4AddRow" name="item4Update">
    <option value="null">All</option>
  </select></td>   
      <td> <select name="operator4Update"  id="operator4AddRow">
      <option value="null">All</option>
      </select></td>    
      <td>
      <select id="item5AddRow" name="item5Update">
    <option value="null">All</option>
  </select></td>
      <td style="border: None;" onclick="addModel()">            
        <i class="fa fa-floppy-o" aria-hidden="true"></i> 
      </td>
      
      </tr>`;
}

async function getModel() {
  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  dropdown_vie = document.getElementById("dropdown_view").value;
  dropdown_itm = document.getElementById("dropdown_item").value;
  dropdown_oper = document.getElementById("dropdown_operator").value;


  let url=window.location.search;
  let id;
  let catogery="All";
  let catogery2="All";
  let catogery3="All";
console.log("yyyyyyyyyyyyyyyyy",id)



  if(url){
    console.log("urll",url)
    let nid=url.substring(url.lastIndexOf("id="))
    let nnid=nid.split("=")[1]
    id=nnid.split("&")[0]
    console.log("idddddd",id)
  
    let cat=url.substring(url.lastIndexOf("category=")).split("=")[1].split("&")[0]
catogery=cat;
    dropdown_vie=catogery;
     let cat2=url.substring(url.lastIndexOf("category2=")).split("=")[1].split("&")[0]
catogery2=cat2
dropdown_itm=catogery2
catogery3=url.substring(url.lastIndexOf("category3=")).split("=")[1]
dropdown_oper=catogery3 
console.log("cat",id,dropdown_vie)
console.log("cat2",id,dropdown_itm)
console.log("cat3",id,dropdown_oper)

}
else if(!url){
  id=1
}
  if (dropdown_vie == null) {
    dropdown_vie=null
  }
  if(dropdown_itm==null){
    dropdown_itm=null
  }
  if(dropdown_oper==null){
    dropdown_oper=null
  }

  
  var data = {
    search_view: "All",
    search_item: "All",
    search_operator:"All",
    page: id,
  };
  try {
    const url="http://127.0.0.1:8000/getaggregatedview"

    if (dropdown_vie == "null" && dropdown_itm== "null" && dropdown_oper=="null") {
      data = {
        search_view: "All",
        search_item: "All",
        search_operator:"All",
        page: id,
      };
    } else if (dropdown_vie== "null") {
      data = {
        search_view: "All",
        search_item: dropdown_itm,
        search_operator:dropdown_oper,
        page: id,
      };
    } else if (dropdown_itm== "null") {
      data = {
        search_view: dropdown_vie,
        search_item: "All",
        search_operator:dropdown_oper,
        page: id,
      };
    } 
    else if(dropdown_oper== "null"){
      data={
        search_view: dropdown_vie,
        search_item: dropdown_itm,
        search_operator:"All",
        page: id,
      }

    }else if(dropdown_vie=="null" && dropdown_itm=="null"){
      data={
        search_view:"All",
      search_item:"All" ,
      search_operator:dropdown_oper,
      page: id,
      }

    }
    
    
    else {
      data = {
        // search_view: dropdown_vie,
        // search_item: dropdown_itm,
        // search_operator:dropdown_oper,
        page: id,
      };
    }

    const response = await fetch(url, {
      //edittt
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
    const url = "http://127.0.0.1:8000/aggregatedrop";
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
    const url = "http://127.0.0.1:8000/deleteaggregateview";
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
  // console.log();

  let viewVal = document.getElementById("viewUpdateID").value;
  let nameVal = document.getElementById("nameUpdateID").value;
  let item1Val = document.getElementById("item1UpdateID").value;
  let operator1Val = document.getElementById("operator1UpdateID").value;
  let item2Val = document.getElementById("item2UpdateID").value;
  let operator2Val = document.getElementById("operator2UpdateID").value;
  let item3Val = document.getElementById("item3UpdateID").value;
  let operator3Val = document.getElementById("operator3UpdateID").value;
  let item4Val = document.getElementById("item4UpdateID").value;
  let operator4Val = document.getElementById("operator4UpdateID").value;
  let item5Val = document.getElementById("item5UpdateID").value;

  document.getElementById("tableDiv").className = "hideTable";
  document.getElementById("spinner").className = "spinner-border";
  try {
    const url = "http://127.0.0.1:8000/aggregateview";
    const data = {
      
      id:el,
      view: viewVal,
    name: nameVal,
    item1: item1Val,
      operator1: operator1Val,
      item2: item2Val,
      operator2: operator2Val,
    item3: item3Val,
      operator3: operator3Val,
      item4: item4Val,
      operator4:operator4Val,
      item5:item5Val,
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
