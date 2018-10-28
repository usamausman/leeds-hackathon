<?php

$servername = "localhost:3306";
$username = "phpmyadmin";
$password = "root";
$database = "homeless";

$conn = mysqli_connect($servername, $username, $password, $database);
$sql = "SELECT name, accountNumber, birthDate, bankBranch FROM coreData WHERE State='3'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  while($row = $result->fetch_assoc()) {
    $name = $row["name"];
    $account = $row["accountNumber"];
    $birth = $row["birthDate"];
    $bank = $row["bankBranch"];
    break;
}}
$sql2 = "UPDATE coreData SET State = NULL, Error = '0' where State='3'";
$conn->query($sql2);

$html = <<<EOL
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>[wisestep]</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" type="text/css" media="screen" href="style.css" />
</head>

<body>
  <header>
    <img src="logo.svg" />
    <h1>[wisestep]</h1>
  </header>
  <section>
    <div class="info">
      <div class="basic">
        <img src="logo96.png" />
        <p>$name</p>
      </div>
      <div class="data">
        <div class="keys">
          <p>Date of Birth</p>
          <p>Account Number</p>
          <p>Mailing Address</p>
        </div>
        <div class="values">
          <p>$birth</p>
          <p>$account</p>
          <p>$bank</p>
        </div>
      </div>
    </div>
  </section>
</body>

</html>
EOL;

echo $html;

?>
