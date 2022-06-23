function create() {
  var n = document.getElementById("n").value;

  if (n > 0) {
    create_matrix(1, n, "a_matrix");
    create_matrix(1, n, "b_matrix");
    create_matrix(n, n, "l_matrix");

    document.getElementById("created_matrix").value = "true";
  } else {
    alert("Shoose N bigger than 0");
  }
}

function create_matrix(row, col, matrix_name) {
  var head;
  if (matrix_name == "scenarios")
    head = "type demands in first N celds and probability in the N+1 celd";
  else head = matrix_name;

  var table = '<table border="0">';

  table += head;
  table += "<tr><td></td>";
  for (j = 0; j < col; j++) {
    table += "<td>" + (j + 1) + "</td>";
  }
  table += "</tr>";

  for (i = 0; i < row; i++) {
    table += "<tr>";
    table += "<td>" + (i + 1) + "</td>";
    for (j = 0; j < col; j++) {
      if (i == j && matrix_name == "l_matrix") {
        table +=
          "<td>" +
          '<input type="text" required="true" readonly value="-1" size="1" name="' +
          matrix_name +
          i +
          j +
          '">' +
          "</td>";
      } else {
        table +=
          "<td>" +
          '<input type="text" required="true" value="-1" size="1" name="' +
          matrix_name +
          i +
          j +
          '">' +
          "</td>";
      }
    }
    table += "</tr>";
  }
  table += "</table>";
  document.getElementById(matrix_name).innerHTML = table;
}

function create_matrix_demands(matrix_name, row, col, param1, param2) {
  var head;
  if (matrix_name == "scenarios")
    head = "type demands in first N celds and probability in the N+1 celd";
  else head = matrix_name;

  var table = '<table border="0">';

  table += head;

  for (i = 0; i < row; i++) {
    table += "<tr>";

    for (j = 0; j < col; j++) {
      var placeholder = "";
      if (j == col - 1) placeholder = param2 + (i + 1);
      else placeholder = param1 + (i + 1) + (j + 1);
      table +=
        "<td>" +
        '<input type="text" required="true" size="1" placeholder="' +
        placeholder +
        '" name="' +
        placeholder +
        '">' +
        "</td>";
    }
    table += "</tr>";
  }
  table += "</table>";
  document.getElementById(matrix_name).innerHTML = table;
}

function clean_params() {
  document.getElementById("params").innerHTML = "";
}

function create_params() {
  clean_params();

  var variable = document.getElementById("variable").value;

  if (variable == "uniform") {
    params =
      '<input type="text" required="true" size="1" placeholder="a" name="params0">';
    params +=
      '<input type="text" required="true" size="1" placeholder="b" name="params1">';
    document.getElementById("params").innerHTML = params;
    document.getElementById("scenarios").innerHTML = "";
    document.getElementById("scenario_val").value = true;
  } else if (variable == "exponential") {
    params =
      '<input type="text" required="true" size="1" placeholder="lambda" name="params0">';
    document.getElementById("params").innerHTML = params;
    document.getElementById("scenarios").innerHTML = "";
    document.getElementById("scenario_val").value = true;
  } else if (variable == "gamma") {
    params =
      '<input type="text" required="true" size="1" placeholder="n" name="params0">';
    params +=
      '<input type="text" required="true" size="1" placeholder="lambda" name="params1">';
    document.getElementById("params").innerHTML = params;
    document.getElementById("scenarios").innerHTML = "";
    document.getElementById("scenario_val").value = true;
  } else if (variable == "normal") {
    params =
      '<input type="text" required="true" size="1" placeholder="miu" name="params0">';
    params +=
      '<input type="text" required="true" size="1" placeholder="O^2" name="params1">';
    document.getElementById("params").innerHTML = params;
    document.getElementById("scenarios").innerHTML = "";
    document.getElementById("scenario_val").value = true;
  } else if (variable == "binary") {
    params =
      '<input type="text" required="true" size="1" placeholder="n" name="params0">';
    params +=
      '<input type="text" size="1" placeholder="p" min="0" max="1" name="params1">';
    document.getElementById("params").innerHTML = params;
    document.getElementById("scenarios").innerHTML = "";
    document.getElementById("scenario_val").value = true;
  } else if (variable == "geometric") {
    params =
      '<input type="text" required="true" size="1" placeholder="p" min="0" max="1" name="params0">';
    document.getElementById("params").innerHTML = params;
    document.getElementById("scenarios").innerHTML = "";
    document.getElementById("scenario_val").value = true;
  } else if (variable == "scenarios") {
    params =
      '<input type="text" required="true" size="13" placeholder="number of scenarios" id="n_scenarios" name="n_scenarios">';
    params +=
      '<input type="button" required="true" id="btn_create_scenarios" value="create scenarios" onclick="create_scenarios(event)"/>';
    document.getElementById("params").innerHTML = params;
  }
}

function create_scenarios(event) {
  var n_scenarios = document.getElementById("n_scenarios").value;
  var n = document.getElementById("n").value;

  if (n_scenarios == "") {
    event.preventDefault();
    alert("Shoose a number bigger than 0 for scenarios");
    return false;
  }
  if (n == "") {
    event.preventDefault();
    alert("Shoose N bigger than 0");
    return false;
  }

  create_matrix_demands(
    "scenarios",
    parseInt(n_scenarios),
    parseInt(n) + 1,
    "d",
    "p"
  );
  document.getElementById("scenario_val").value = true;
}

function parse_data(event) {
  var variable = document.getElementById("variable").value;
  var created_matrix = document.getElementById("created_matrix").value;
  var scenario_val = document.getElementById("scenario_val").value;

  if (variable == "none") {
    event.preventDefault();
    alert("Set variable type");
    return false;
  } else if (created_matrix == "false") {
    event.preventDefault();
    alert("Create matrix A, B and L");
    return false;
  } else if (variable == "scenarios" && scenario_val == "false") {
    event.preventDefault();
    alert("Create scenarios");
    return false;
  }
}

function parse_data_from_excel() {
  document.getElementById("excel").value = "true";
  console.log("State of excel changed");
}
